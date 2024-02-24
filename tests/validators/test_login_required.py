from flask import Flask

from easy_framework.auth import BaseAuthMethod
from easy_framework.exception import InvalidSession
from easy_framework.user import UserModel
from easy_framework.validator import Login_required
from tests import TestCase

class TestLogin_Required(TestCase):
    @property
    def flaskApp (self)-> Flask:
        return self.get_flask_app_sql()
    
    def getView(self):
        class MyView():
            @Login_required()
            def test_func(cls):
                return 'testing_string'
        return MyView()

    def test_make_request_with_hedder_auth_and_get_no_errors(self):
        with self.flaskApp.test_request_context('/', json={'login': 'test', 'password': 'test123'}):
            user = UserModel(login='test', password='test123').save()
            authmethod: BaseAuthMethod = self.flaskApp.authManager.auth_method
            token = authmethod.generateSession(user)

        with self.flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            assert self.getView().test_func() == 'testing_string'

    def test_make_request_with_heder_auth_not_in_database_and_get_no_errors(self):
        with self.flaskApp.test_request_context('/', json={'login': 'test', 'password': 'test123'}):
            UserModel(login='test', password='test123').save()
            authmethod: BaseAuthMethod = self.flaskApp.authManager.auth_method
            token = authmethod.generateHashToken()

        with self.flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            with self.assertRaises(InvalidSession) as e_info:
                self.getView().test_func()
                assert 440 in str(e_info.exception.value)
