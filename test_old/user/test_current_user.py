from flask import Flask, current_app
from pytest import fixture

from easy_framework.user import (AnonymousUser, UserMixin, UserModel,
                                 current_user)


class TestCurrent_user():
    @fixture
    def userModel(self, flaskApp: Flask):
        return flaskApp.config.get('EASY_FRAMEWORK_USER_MODEL')

    def authJson(self):
        return {
            'login': 'test',
            'password': 'test'
        }

    def test_request_with_existent_session_token_and_get_access_to_current_user_returning_an_userMixin_instance(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = current_app.authManager.auth_method.generateSession(user)
        with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            assert isinstance(current_user, UserMixin)

    def test_request_with_non_existent_session_token_and_get_access_to_current_user_returning_an_Anonymous_instance(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = current_app.authManager.auth_method.generateHashToken()
        with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            assert isinstance(current_user, AnonymousUser)
