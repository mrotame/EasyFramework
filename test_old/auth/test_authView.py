from flask import Flask
from easy_framework.auth import AuthView
import pytest
from easy_framework.exception.apiExceptions import InvalidCredentials

class TestAuthView():
    def url(self):
        return AuthView.routes[0]

    def authJson(self):
        return {'login':'test','password':'test'}

    def getUserModel(self, flaskApp:Flask):
        return flaskApp.config.get('EASY_FRAMEWORK_USER_MODEL')

    def test_request_login_without_registered_user_and_get_invalidCredentialsException(self, flaskApp: Flask):
        with flaskApp.test_request_context(self.url(), json=self.authJson()):
            with pytest.raises(InvalidCredentials) as exc_info:
                AuthView().post()
                assert type(exc_info.value) is InvalidCredentials

    def test_request_login_and_get_token(self, flaskApp: Flask):
        with flaskApp.test_request_context():
            self.getUserModel(flaskApp)(login='test', password='test').save()
            res = flaskApp.test_client().post(self.url(),json=self.authJson())
            assert res.status_code == 200
            assert 'auth_token' in res.get_json()
            assert type(res.get_json().get('auth_token')) is str