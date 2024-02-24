from __future__ import annotations
from typing import TYPE_CHECKING

from flask import current_app, g, has_request_context
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    from .userModel import UserModel
    from ..auth import AuthManager

current_user: UserModel = LocalProxy(lambda: __get_user())

def __get_user()->UserModel:
    if has_request_context():
        if 'user' not in g:
            authManager: AuthManager = current_app.authManager
            authManager.loadUser()
        return g.user
