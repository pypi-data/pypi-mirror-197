import asyncio
import os
import warnings
from binascii import b2a_hex
from fnmatch import fnmatch
from functools import cached_property
from textwrap import dedent
from time import time
from typing import List, Union, TypedDict, Callable, Dict, Optional, Tuple

import fastjsonschema  # noqa pycharm?

from kaiju_tools.rpc.abc import AbstractRPCCompatible
from kaiju_tools.rpc.etc import JSONRPCHeaders
from kaiju_tools.rpc.sessions import BaseSessionService
from kaiju_tools.rpc.jsonrpc import (
    RPCRequest,
    RPCError,
    RPCResponse,
    RequestTimeout,
    InvalidRequest,
    InvalidParams,
    InternalError,
    AbortedByServer,
    MethodNotFound,
    PermissionDenied,
)
from kaiju_tools.functions import timeout
from kaiju_tools.exceptions import APIException
from kaiju_tools.services import ContextableService, RequestContext, Session, Scope
from kaiju_tools.jsonschema import compile_schema
from .context import REQUEST_CONTEXT, REQUEST_SESSION

__all__ = ['RequestHeaders', 'MethodInfo', 'JSONRPCServer']


class _Aborted(APIException):
    pass


class RequestHeaders(TypedDict):
    """Request headers acknowledged by the server."""

    correlation_id: str
    request_deadline: int
    abort_on_error: bool


class MethodInfo(TypedDict):
    """Stored method data."""

    f: Callable
    service_name: str
    permission: Scope
    validator: Callable


class JSONRPCServer(ContextableService, AbstractRPCCompatible):
    """A simple JSON RPC interface with method execution and management tasks."""

    service_name = 'rpc'
    _permission_levels = {
        AbstractRPCCompatible.PermissionKeys.GLOBAL_SYSTEM_PERMISSION: Scope.SYSTEM,
        AbstractRPCCompatible.PermissionKeys.GLOBAL_USER_PERMISSION: Scope.USER,
        AbstractRPCCompatible.PermissionKeys.GLOBAL_GUEST_PERMISSION: Scope.GUEST,
    }

    def __init__(
        self,
        app,
        *,
        session_service: BaseSessionService = None,
        max_parallel_tasks: int = 64,
        default_request_time: int = 120,
        max_request_time: int = 600,
        enable_permissions: bool = True,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param session_service: session backend
        :param max_parallel_tasks: max number of tasks in the loop
        :param default_request_time: (s)
        :param max_request_time: (s)
        :param enable_permissions: enable perm checks in requests
        :param logger:
        """
        ContextableService.__init__(self, app=app, logger=logger)
        self._sessions = session_service
        self._max_parallel_tasks = max(1, int(max_parallel_tasks))
        self._default_request_time = max(1, int(default_request_time))
        self._max_request_time = max(self._default_request_time, int(max_request_time))
        self._enable_permissions = enable_permissions
        self._debug = self.app.debug
        self._counter = self._max_parallel_tasks
        self._not_full = asyncio.Event()
        self._not_full.set()
        self._empty = asyncio.Event()
        self._empty.set()
        self._methods: Dict[str, MethodInfo] = {}

    async def init(self):
        self.logger.info('Starting.')
        if not self._enable_permissions:
            warnings.warn('Server permissions are disabled.')
        self._counter = self._max_parallel_tasks
        self._empty.set()
        self._not_full.set()
        self._sessions = self.discover_service(self._sessions, cls=BaseSessionService, required=False)
        for service_name, service in self.app.services.items():
            if isinstance(service, AbstractRPCCompatible):
                self.register_service(service_name, service)
        await super().init()

    async def close(self):
        await self._empty.wait()
        await super().close()

    @property
    def routes(self):
        return {'routes': self.get_routes, 'info': self.get_info}

    @property
    def permissions(self):
        return {
            'routes': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
            'info': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
        }

    async def get_info(self) -> dict:
        """Get all currently running tasks."""
        tasks = asyncio.all_tasks(asyncio.get_running_loop())
        t = int(time())
        return {
            'total_tasks': len(tasks),
            'rpc_tasks': self._max_parallel_tasks - self._counter,
            'server_time': int(time()),
            'max_tasks': self._max_parallel_tasks,
            'max_timeout': self._max_request_time,
            'default_timeout': self._default_request_time,
            'enable_permissions': self._enable_permissions,
            'tasks': [
                {
                    'correlation_id': task.get_name().replace('rpc ', '', 1),
                    'time_elapsed': t - task.started,  # noqa (added at call)
                    'time_left': task.deadline - task.started,  # noqa (added at call)
                }
                for task in tasks
                if task.get_name().startswith('rpc ')
            ],
        }

    async def get_routes(self) -> list:
        """Get all RPC routes (you are here)."""
        return self.registered_routes

    @cached_property
    def registered_routes(self):
        session = self.get_session()
        routes = [
            {
                'route': route,
                'permission': method['permission'].name,
                'info': dedent(method['f'].__doc__.split('\n')[0]) if method['f'].__doc__ else None,
            }
            for route, method in self._methods.items()
            if method['permission'].value >= session.scope.value
        ]
        routes.sort(key=lambda o: o['route'])
        return routes

    def register_service(self, service_name: str, service: AbstractRPCCompatible) -> None:
        """Register an RPC compatible service and its methods."""
        if not isinstance(service, AbstractRPCCompatible):
            raise TypeError('Service must be rpc compatible.')
        permissions = service.permissions
        validators = service.validators
        for route, f in service.routes.items():
            full_name = f'{service_name}.{route}'
            validator = validators.get(route, None)
            route_perm = AbstractRPCCompatible.PermissionKeys.GLOBAL_SYSTEM_PERMISSION
            for pattern, perm in permissions.items():
                if fnmatch(route, pattern):
                    route_perm = perm
            if validator:
                validator = compile_schema(validator)
            method = MethodInfo(
                f=f, permission=self._permission_levels[route_perm], validator=validator, service_name=service_name
            )
            self._methods[full_name] = method

    async def call(
        self,
        body: Union[List, Dict],
        headers: dict = None,
        session: Session = None,
        nowait: bool = False,
        scope: Scope = Scope.SYSTEM,
    ) -> asyncio.Task:
        """Call a server command.

        :param body: request body
        :param headers: request headers (optional)
        :param session: client session object
        :param scope: user scope
        :param nowait: do not wait for the result
        """
        headers = self._get_request_headers(headers)
        if type(body) in {list, tuple}:
            coro = self._execute_batch(
                body,
                request_deadline=headers['request_deadline'],
                abort_on_error=headers['abort_on_error'],
                session=session,
                scope=scope,
                correlation_id=headers['correlation_id'],
            )
        else:
            coro = self._execute_single(
                body,
                request_deadline=headers['request_deadline'],
                session=session,
                scope=scope,
                correlation_id=headers['correlation_id'],
            )
        self._counter -= 1
        if not self._not_full.is_set():
            await self._not_full.wait()
        task = asyncio.create_task(coro)
        task.set_name(f'rpc {headers["correlation_id"]}')
        setattr(task, 'deadline', headers['request_deadline'])
        setattr(task, 'started', int(time()))
        task.add_done_callback(self._request_done_cb)
        if self._empty.is_set():
            self._empty.clear()
        if self._counter <= 0:
            self._counter = 0
            self._not_full.clear()
        if nowait:
            return task
        else:
            return await task  # noqa compatibility reasons

    @staticmethod
    def _parse_number_value(value, min_val, max_val, default) -> int:
        if not value:
            return default
        try:
            value = int(value)
        except Exception:  # noqa
            return default
        return min(max(min_val, value), max_val)

    @staticmethod
    def _parse_boolean_value(value, default) -> bool:
        if not value:
            return default
        return value.lower() == 'true'

    def _get_request_headers(self, headers: Union[dict, None]) -> RequestHeaders:
        if headers is None:
            headers = {}
        request_deadline = headers.get(JSONRPCHeaders.REQUEST_DEADLINE_HEADER)
        t0 = int(time())
        if request_deadline:
            request_deadline = self._parse_number_value(request_deadline, 0, t0 + self._max_request_time, 0)
        else:
            request_timeout = self._parse_number_value(
                headers.get(JSONRPCHeaders.REQUEST_TIMEOUT_HEADER),
                1,
                self._max_request_time,
                self._default_request_time,
            )
            request_deadline = t0 + request_timeout + 1
        return RequestHeaders(
            correlation_id=headers.get(JSONRPCHeaders.CORRELATION_ID_HEADER, b2a_hex(os.urandom(4)).decode()),
            request_deadline=request_deadline,
            abort_on_error=self._parse_boolean_value(headers.get(JSONRPCHeaders.ABORT_ON_ERROR), False),
        )

    async def _execute_single(
        self,
        body,
        request_deadline: int,
        session: Optional[Session],
        scope: Scope,
        correlation_id: Optional[str],
    ) -> Tuple[dict, Union[RPCResponse, RPCError]]:
        ctx = RequestContext(
            session_id=session.id if session else None,
            request_deadline=request_deadline,
            correlation_id=correlation_id,
        )
        REQUEST_SESSION.set(session)
        REQUEST_CONTEXT.set(ctx)
        self.logger.info(
            '->', request=body, request_deadline=request_deadline, scope=scope, session_id=ctx['session_id']
        )
        try:
            async with timeout(request_deadline - time()):
                result = await self._execute_request(body, id_=0, session=session, scope=scope)
                session = self.get_session()
        except asyncio.TimeoutError:
            result = RequestTimeout()
        if self._sessions and session and session.stored and session.changed:
            await self._sessions.save_session(session)
        self.logger.info('<-', response=result)
        return self._get_response_headers(correlation_id, session), result

    @staticmethod
    def _get_response_headers(correlation_id: str, session: Optional[Session]) -> dict:
        headers = {}
        if correlation_id:
            headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = correlation_id
        if session and session.stored and (session.changed or session.loaded):
            headers[JSONRPCHeaders.SESSION_ID_HEADER] = session.id
        return headers

    async def _execute_batch(
        self,
        request: List[dict],
        request_deadline: int,
        abort_on_error: bool,
        session: Optional[Session],
        scope: Scope,
        correlation_id: Optional[str],
    ) -> Tuple[dict, List[Union[RPCResponse, RPCError]]]:
        """Execute multiple coroutine functions."""
        ctx = RequestContext(
            session_id=session.id if session else None,
            request_deadline=request_deadline,
            correlation_id=correlation_id,
        )
        REQUEST_SESSION.set(session)
        REQUEST_CONTEXT.set(ctx)
        _request = [request[0]]
        self.logger.info(
            '->', request=_request, request_deadline=request_deadline, scope=scope, session_id=ctx['session_id']
        )
        results = []
        for n, row in enumerate(request):
            try:
                async with timeout(request_deadline - time()):
                    result = await self._execute_request(row, id_=n, session=session, scope=scope)
                    if abort_on_error and isinstance(result, RPCError):
                        raise _Aborted
            except _Aborted:
                results.extend((AbortedByServer(id=id_) for id_ in range(n, len(request))))
                break
            except asyncio.TimeoutError:
                results.extend((RequestTimeout(id=id_) for id_ in range(n, len(request))))
                break
            else:
                results.append(result)

        self.logger.info('<-', response=[results[0]])
        session = self.get_session()
        if self._sessions and session and session.stored and session.changed:
            await self._sessions.save_session(session)
        return self._get_response_headers(correlation_id, session), results

    async def _execute_request(
        self, request: dict, id_, session: Optional[Session], scope: Scope
    ) -> Union[RPCResponse, RPCError]:
        if type(request) is not dict:
            raise InvalidRequest(id=id_, message='Request body must be a JSONRPC object.')
        if 'id' not in request:
            request['id'] = id_
        try:
            request = RPCRequest(**request)
            id_ = request.id
        except Exception as exc:
            return InvalidRequest(id=id_, base_exc=exc, debug=self._debug, message=str(exc))
        if request.params is None:
            params = {}
        elif type(request.params) is dict:
            params = request.params
        else:
            return InvalidParams(id=id_, message='Request params must be either a mapping or null.')
        try:
            method = self._methods[request.method]
        except KeyError:
            return MethodNotFound(id=id_, data={'method': request.method})
        if method['validator']:
            try:
                params = method['validator'](params)
            except fastjsonschema.JsonSchemaException as exc:
                return InvalidParams(id=id_, message=str(exc), base_exc=exc)
        if self._enable_permissions and scope != Scope.SYSTEM:
            if all(
                (
                    method['permission'].value < scope.value,
                    session and request.method not in session.permissions,
                    session and method['service_name'] not in session.permissions,
                )
            ):
                return PermissionDenied(id=id_, data={'method': request.method})
        try:
            coro = method['f'](**params)
        except Exception as exc:
            return InvalidParams(id=request.id, base_exc=exc, message=str(exc))
        try:
            result = await coro
            return RPCResponse(id=id_, result=result)
        except asyncio.TimeoutError:
            return RequestTimeout(id=id_)
        except APIException as exc:
            return RPCError.from_api_exception(id_, exc, debug=self._debug)
        except Exception as exc:
            self.logger.info('RPC error.', exc_info=exc)
            return InternalError(id=id_, base_exc=exc, debug=self._debug)

    def _request_done_cb(self, task: asyncio.Task) -> None:
        """Increment the counter when a request is finished."""
        self._counter += 1
        if self._counter >= self._max_parallel_tasks:
            self._counter = self._max_parallel_tasks
            self._empty.set()
        if not self._not_full.is_set():
            self._not_full.set()
        exc = task.exception()
        if exc:
            self.logger.error('Execution error.', exc_info=exc)
