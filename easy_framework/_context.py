from __future__ import annotations
import typing as t


from werkzeug.local import LocalProxy

from contextvars import ContextVar
from prodot import ProObject


ctx = ContextVar("easy_framework.app.cache", default=ProObject())

cache: CacheType = LocalProxy(ctx)


if t.TYPE_CHECKING:
    from easy_framework.config import Config
    from flask import Flask
    from pathlib import Path

    class CacheType:
        app: Flask
        api_exception_list: t.List

        config: Config
        root_dir: Path
