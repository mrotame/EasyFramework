from flask import request, current_app
from easy_framework.exception import InvalidSession
from easy_framework.exception import AuthMissingError
from easy_framework.user import current_user
from ._baseValidator import BaseValidator

class Login_required(BaseValidator):
    def validate(self):
        self.checkTokenInRequest()
        self.validateToken()
        self.checkUser()

    def checkTokenInRequest(self):
        if 'Authorization' not in request.headers:
            raise AuthMissingError()

    def validateToken(self):
        current_app.authManager.auth_method.validateToken()

    def checkUser(self):
        if current_user.is_authenticated is True:
            return True
        raise InvalidSession()