from flask import Flask, current_app

from easy_framework.user import UserModelMongo
from easy_framework.user import (AnonymousUser, UserMixin, UserModelMongo,
                                 current_user)


class TestCurrent_user():
    def authJson(self):
        return {
            'login': 'test',
            'password': 'test'
        }

    def test_request_with_existent_session_token_and_get_access_to_current_user_returning_an_userMixin_instance(self, flaskAppMongo: Flask):
        with flaskAppMongo.test_request_context('/', json=self.authJson()):
            user = UserModelMongo(
                login='test', password='test')
            user.save()
            token = current_app.authManager.auth_method.generateSession(user)
        with flaskAppMongo.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            assert isinstance(current_user, UserMixin)

    def test_request_with_non_existent_session_token_and_get_access_to_current_user_returning_an_Anonymous_instance(self, flaskAppMongo: Flask):
        with flaskAppMongo.test_request_context('/', json=self.authJson()):
            user = UserModelMongo(
                login='test', password='test')
            user.save()
            token = current_app.authManager.auth_method.generateHashToken()
        with flaskAppMongo.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            from easy_framework.user import current_user as test
            assert isinstance(current_user, AnonymousUser)
