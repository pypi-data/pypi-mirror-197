from contextvars import ContextVar  # noqa pycharm
from typing import Union

from kaiju_tools.services import RequestContext

__all__ = ['REQUEST_CONTEXT']


REQUEST_CONTEXT: ContextVar[Union[None, RequestContext]] = ContextVar('RequestContext', default=None)
