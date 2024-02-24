import pytest
from flask import Flask

from easy_framework.auth import BaseAuthMethod
from easy_framework.exception import InvalidSession
from easy_framework.user import UserModel
from easy_framework.validator import Login_required


class TestLogin_Required():
    def getView(self):
        class MyView():
            @Login_required()
            def test_func(cls):
                return 'testing_string'
        return MyView()

    def test_make_request_with_hedder_auth_and_get_no_errors(self, flaskApp: Flask):
        with flaskApp.test_request_context('/', json={'login': 'test', 'password': 'test123'}):
            user = UserModel(login='test', password='test123').save()
            authmethod: BaseAuthMethod = flaskApp.authManager.auth_method
            token = authmethod.generateSession(user)

        with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            assert self.getView().test_func() == 'testing_string'

    def test_make_request_with_heder_auth_not_in_database_and_get_no_errors(self, flaskApp: Flask):
        with flaskApp.test_request_context('/', json={'login': 'test', 'password': 'test123'}):
            UserModel(login='test', password='test123').save()
            authmethod: BaseAuthMethod = flaskApp.authManager.auth_method
            token = authmethod.generateHashToken()

        with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            with pytest.raises(InvalidSession) as e_info:
                res = self.getView().test_func()
                assert 440 in str(e_info.value)
