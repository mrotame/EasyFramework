import typing as t

from werkzeug.local import LocalProxy

from prodot import ProObject
from contextvars import ContextVar


ctx = ContextVar('easy_framework.app.cache', default=ProObject())

cache: ProObject = LocalProxy(ctx)
