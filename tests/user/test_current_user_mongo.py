from flask import current_app

from tests import TestCase
from easy_framework.user import UserModelMongo
from easy_framework.user import (
    AnonymousUser, 
    UserMixin, 
    UserModelMongo,
    current_user
)


class TestCurrent_user(TestCase):
    def authJson(self):
        return {
            'login': 'test',
            'password': 'test'
        }

    def test_request_with_existent_session_token_and_get_access_to_current_user_returning_an_userMixin_instance(self):
        with self.get_flask_app_mongo().test_request_context('/', json=self.authJson()):
            user = UserModelMongo(
                login='test', password='test')
            user.save()
            token = current_app.authManager.auth_method.generateSession(user)
        with self.get_flask_app_mongo().test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            self.assertIsInstance(current_user, UserMixin)
            pass

    def test_request_with_non_existent_session_token_and_get_access_to_current_user_returning_an_Anonymous_instance(self):
        with self.get_flask_app_mongo().test_request_context('/', json=self.authJson()):
            user = UserModelMongo(
                login='test', password='test')
            user.save()
            token = current_app.authManager.auth_method.generateHashToken()
        with self.get_flask_app_mongo().test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            self.assertIsInstance(current_user, AnonymousUser)
