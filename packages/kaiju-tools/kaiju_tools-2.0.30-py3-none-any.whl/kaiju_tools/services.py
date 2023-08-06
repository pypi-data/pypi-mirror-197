import abc
import logging
from datetime import datetime
from enum import Enum
from typing import Union, Iterable, List, Type, Optional, TypedDict, FrozenSet, TypeVar
from uuid import UUID

from aiohttp.web import Application

from kaiju_tools.logging.types import Adapter
from kaiju_tools.class_registry import AbstractClassRegistry
from kaiju_tools.serialization import Serializable

__all__ = [
    'App',
    'Service',
    'ContextableService',
    'ServiceClassRegistry',
    'service_class_registry',
    'RequestContext',
    'Session',
    'Scope',
    'SCOPE_MAP',
    'ServiceConfigurationError',
    'ServiceContextManager',
]


class Scope(Enum):
    """Permission scope for application methods."""

    SYSTEM = 0
    USER = 100
    GUEST = 1000


SCOPE_MAP = {Scope.SYSTEM: 'system', Scope.USER: 'user'}


class Session(Serializable):
    """User session data."""

    __slots__ = ('id', 'h_agent', 'user_id', 'expires', 'permissions', 'data', 'created', '_stored', '_changed')

    def __init__(
        self,
        *,
        id: str,  # noqa
        h_agent: bytes,
        user_id: Optional[UUID],
        expires: int,
        permissions: FrozenSet[str],
        data: dict,
        created: datetime,
        _stored: bool,
        _changed: bool,
        _loaded: bool,
    ):
        """Initialize.

        :param id:
        :param h_agent:
        :param user_id:
        :param expires:
        :param permissions:
        :param data:
        :param created:
        :param _stored:
        :param _changed:
        :param _loaded:
        """
        self.id = id
        self.h_agent = h_agent
        self.user_id = user_id
        self.expires = expires
        self.permissions = frozenset(permissions)
        self.data = data
        self.created = created
        self._stored = _stored
        self._changed = _changed
        self._loaded = _loaded

    def __getitem__(self, item):
        return self.data.get(item)

    def __setitem__(self, key, value):
        self.update({key: value})

    @property
    def scope(self) -> Scope:
        """Base user scope."""
        if SCOPE_MAP[Scope.SYSTEM] in self.permissions:
            return Scope.SYSTEM
        elif SCOPE_MAP[Scope.USER] in self.permissions:
            return Scope.USER
        else:
            return Scope.GUEST

    @property
    def stored(self) -> bool:
        """Session should be stored."""
        return self._stored

    @property
    def changed(self) -> bool:
        """Session has changed."""
        return self._changed

    @property
    def loaded(self) -> bool:
        """Session has been loaded from db."""
        return self._loaded

    def update(self, data: dict):
        """Update session data."""
        self.data.update(data)
        self._changed = True

    def clear(self):
        """Clear all session data."""
        self.data.clear()
        self._changed = True

    def repr(self) -> dict:
        """Get object representation."""
        return {slot: getattr(self, slot) for slot in self.__slots__ if not slot.startswith('_')}


class RequestContext(TypedDict):
    """Request context stored for the request chain."""

    correlation_id: str
    session_id: Optional[str]
    request_deadline: Optional[int]


class ServiceConfig(TypedDict, total=False):
    cls: str
    name: str
    enabled: bool
    required: bool
    settings: dict


class App(Application):
    """Web application interface."""

    id: str
    name: str
    version: str
    env: str
    debug: bool
    loglevel: str
    logger: logging.Logger
    services: 'ServiceContextManager'
    settings: dict

    def get_context(self) -> RequestContext:
        ...

    def get_session(self) -> Optional[Session]:
        ...


class Service(abc.ABC):
    """Base service class."""

    service_name = None  #: you may define a custom service name here

    def __init__(self, app: App = None, logger=None):
        """Initialize.

        :param app: aiohttp web application
        :param logger: a logger instance (None for default)
        """
        self.app = app
        self._logger_ctx = self._get_logger_ctx()
        if logger is None:
            if app:
                logger = logging.getLogger(self.app.name)
            else:
                logger = logging.getLogger('root')
        self.logger = Adapter(logger.getChild(self._get_logger_name()), self._logger_ctx)

    def _get_logger_name(self) -> str:
        name = getattr(self, 'service_name', None)
        if not name:
            name = self.__class__.__name__
        return name

    @staticmethod
    def _get_logger_ctx() -> dict:
        return {}

    @staticmethod
    def _get_parent_logger(app, logger):
        if app is not None and logger is None:
            return app.logger
        else:
            return logger

    def discover_service(
        self,
        name: Union[str, 'Service', None],
        cls: Union[Union[str, Type], Iterable[Union[str, Type]]] = None,
        required=True,
    ):
        """Discover a service using specified name and/or service class.

        :param name: specify a service name or service instance (in latter case
            it will be returned as is)
            False means that nothing will be returned, i.e. service will be disabled
        :param cls: specify service class. If name wasn't specified, then the first
            service matching given class will be returned. If name and class
            both were specified, then the type check will be performed on a newly
            discovered service
        :param required: means that an exception will rise if service doesn't exist
            otherwise in this case None will be returned
        """
        if name is False and not required:
            return
        elif isinstance(name, Service):
            return name
        else:
            return self.app.services.discover_service(name=name, cls=cls, required=required)


class ContextableService(Service):
    """A service which must be asynchronously initialized after it was created."""

    async def init(self):
        """Define your asynchronous initialization here."""

    async def close(self):
        """Define your asynchronous de-initialization here."""

    @property
    def closed(self) -> bool:
        """Must return True if `close()` procedure has been successfully executed."""
        return False

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


Contextable = ContextableService


class ServiceConfigurationError(RuntimeError):
    """An error during services configuration or initialization."""


class ServiceNotAvailableError(KeyError):
    """Service with such name doesn't exist."""


class ServiceClassRegistry(AbstractClassRegistry):
    """Class registry for service classes."""

    base_classes = [Service]


service_class_registry = ServiceClassRegistry(raise_if_exists=False)  #: default service class registry object

_Service = TypeVar('_Service', bound=Service)


class ServiceContextManager(ContextableService):
    """Services manager."""

    service_name = 'srv'

    def __init__(
        self,
        app: App,
        settings: List[Union[ServiceConfig, str]],
        class_registry: ServiceClassRegistry = service_class_registry,
        logger=None,
    ):
        """Initialize."""
        super().__init__(app=app, logger=logger)
        self._settings = settings
        self._registry = class_registry
        self._required = set()
        self._running_services = []
        self._services = {}

    async def init(self):
        self._create_services()
        for name, service in self._services.items():
            try:
                await self.start_service(name)
            except Exception as exc:
                if name in self._required:
                    await self.close()
                    raise
                else:
                    self.logger.error('Error initializing service "%s": %s', name, exc, exc_info=exc)

    async def close(self):
        for name in self._running_services[::-1]:
            await self.terminate_service(name)
        self._running_services.clear()

    async def start_service(self, name: str) -> None:
        """Start an idle service."""
        service = self._services[name]
        if name in self._running_services:
            return
        if isinstance(service, ContextableService):
            self.logger.info('Starting service "%s".', service.service_name)
            await service.init()
            self._running_services.append(name)

    async def terminate_service(self, name: str) -> None:
        """Terminate a running service."""
        service = self._services[name]
        if name not in self._running_services:
            return
        if isinstance(service, ContextableService):
            self.logger.info('Closing service "%s".', service.service_name)
            try:
                await service.close()
            except Exception as exc:
                self.logger.error('Error closing service  "%s": %s', name, exc, exc_info=exc)
        self._running_services.remove(name)

    async def cleanup_context(self, app):
        """Get aiohttp cleanup context."""
        await self.init()
        yield
        await self.close()

    def __getattr__(self, item):
        return self._services[item]

    def __getitem__(self, item):
        return self._services[item]

    def __contains__(self, item):
        return item in self._services

    def items(self):
        return self._services.items()

    def discover_service(
        self,
        name: Union[str, _Service] = None,
        cls: Type[_Service] = None,
        required: bool = True,
    ) -> Optional[_Service]:
        """Discover a service using specified name and/or service class.

        :param name: specify a service name or service instance (in latter case
            it will be returned as is)
        :param cls: specify service class or a list of classes. If name wasn't specified,
            then the first service matching given class will be returned. If name and class
            both were specified, then the type check will be performed on a newly
            discovered service. If multiple classes are provided they will be checked in
            priority order one by one.
        :param required: means that an exception will rise if service doesn't exist
            otherwise in this case None will be returned
        """
        if isinstance(name, Service):
            return name

        if name and name in self._services:
            service = self._services[name]
            if not isinstance(service, cls):
                raise ValueError('Service class mismatch.')
            return service

        service = next((service for service in self._services.values() if isinstance(service, cls)), None)
        if service:
            return service
        elif required:
            raise ValueError('Service not found.')

    def _create_services(self) -> None:
        self._services.clear()
        for settings in self._settings:
            if type(settings) is str:
                settings = ServiceConfig(cls=settings)
            if settings.get('enabled', True):
                cls = self._registry[settings['cls']]
                name = settings.get('name', getattr(cls, 'service_name', None))
                if not name:
                    name = cls.__name__
                if name in self._services:
                    raise ServiceConfigurationError('Service with name "%s" already registered.' % name)
                service = cls(app=self.app, **settings.get('settings', {}), logger=self.logger)
                self._services[name] = service
                if settings.get('required', True):
                    self._required.add(name)
