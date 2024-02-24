from __future__ import annotations
import typing as t

from flask import Flask

from easy_framework.view import GenericApiView
from easy_framework._context import cache

@t.overload
def register_view(view: GenericApiView):
    pass

@t.overload
def register_view(view: GenericApiView, flaskApp: Flask):
    pass


def register_view(view: GenericApiView, flaskApp: Flask = None):
    if not flaskApp:
        flaskApp: Flask = cache.app
    
    for route in view.routes:
        view_id = view.__name__+'.'+ route
        flaskApp.add_url_rule(route, view_id, view.as_view(view_id))