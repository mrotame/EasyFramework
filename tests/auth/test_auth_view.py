from flask import Flask

from tests import TestCase
from easy_framework.auth import AuthView
from easy_framework.exception.apiExceptions import InvalidCredentials
from easy_framework._context import cache


class TestAuthView(TestCase):
    def url(self):
        return AuthView.routes[0]

    def authJson(self):
        return {"login": "test", "password": "test"}

    def getUserModel(self):
        return cache.config.EASY_FRAMEWORK_USER_MODEL

    def test_request_login_without_registered_user_and_get_invalidCredentialsException(
        self,
    ):
        with self.get_flask_app_sql().test_request_context(
            self.url(), json=self.authJson()
        ):
            with self.assertRaises(InvalidCredentials) as exc_info:
                AuthView().post()
                self.assertIsInstance(exc_info.value, InvalidCredentials)

    def test_request_login_and_get_token(self):
        flask_app = self.get_flask_app_sql()
        with flask_app.test_request_context():
            self.getUserModel()(login="test", password="test").save()
            res = flask_app.test_client().post(self.url(), json=self.authJson())
            self.assertEqual(res.status_code, 200)
            self.assertTrue("auth_token" in res.get_json())
            self.assertIsInstance(res.get_json().get("auth_token"), str)
