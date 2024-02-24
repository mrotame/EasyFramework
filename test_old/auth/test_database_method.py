import pytest
from flask import Flask, g
from pytest import fixture

from easy_framework.auth import AuthModel
from easy_framework.auth import AuthModelMongo
from easy_framework.auth import DatabaseMethodSql
from easy_framework.auth import DatabaseMethodMongo
from easy_framework.exception.apiExceptions import InvalidCredentials
from easy_framework.user.userModel import UserModel
from easy_framework.user.userModelMongo import UserModelMongo
from easy_framework.user.userMixin import AnonymousUser, UserMixin

class TestDatabaseMethod():
    def authJson(self):
        return {
            'login': 'test',
            'password': 'test'
        }

    @fixture
    def userModel(self, flaskApp: Flask):
        return flaskApp.config.get('EASY_FRAMEWORK_USER_MODEL')
    
    @fixture
    def userModelMongo(self, flaskApp: Flask):
        return UserModelMongo

    def test_generate_hash_token(self, flaskApp: Flask):
        with flaskApp.test_request_context('/', json=self.authJson()):
            assert len(DatabaseMethodSql().generateHashToken()) >= 128

    def test_request_a_new_token_with_no_user_registered_and_get_404(self, flaskApp: Flask):
        with flaskApp.test_request_context('/', json=self.authJson()):
            with pytest.raises(InvalidCredentials) as exc_info:
                DatabaseMethodSql().generateSession(None)
                assert type(exc_info.value) is InvalidCredentials

    def test_request_a_new_token_and_get_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(login='test', password='test').save()
            assert (t := DatabaseMethodSql().generateSession(user)
                    ) is not None and type(t) is str
            
    def test_request_a_new_token_and_get_token_using_mongo_model(self, flaskAppMongo: Flask, userModelMongo: UserModelMongo):
        with flaskAppMongo.test_request_context('/', json=self.authJson()):
            user = userModelMongo(login='test', password='test').save()
            assert (t := DatabaseMethodMongo().generateSession(user)
                    ) is not None and type(t) is str

    def test_request_a_new_token_and_check_token_in_database(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethodSql().generateSession(user)
            tokenModel: AuthModel = AuthModel.get_one(AuthModel.token == token)
            assert tokenModel is not None
            assert tokenModel.user_id == user.id

    def test_request_a_new_token_and_check_token_in_database_mongo(self, flaskAppMongo: Flask, userModelMongo: UserModelMongo):
        with flaskAppMongo.test_request_context('/', json=self.authJson()):
            user = userModelMongo(
                login='test', password='test')
            user.save()
            token = DatabaseMethodMongo().generateSession(user)
            tokenModel: AuthModelMongo = AuthModelMongo.get_one(AuthModel.token == token)
            assert tokenModel is not None
            assert tokenModel.user_id == user.id

    def test_check_an_existent_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethodSql().generateSession(user)
            with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
                DatabaseMethodSql().loadUser()
                assert g.user is not None

    def test_check_an_existent_token_mongo(self, flaskAppMongo: Flask, userModelMongo: UserModelMongo):
        with flaskAppMongo.test_request_context('/', json=self.authJson()):
            user = userModelMongo(
                login='test', password='test')
            user.save()
            token = DatabaseMethodMongo().generateSession(user)
            with flaskAppMongo.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
                DatabaseMethodMongo().loadUser()
                assert g.user is not None

    def test_check_an_nonexistent_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethodSql().generateHashToken()
        with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethodSql().loadUser()
            assert isinstance(g.user, AnonymousUser)

    def test_check_an_nonexistent_token_mongo(self, flaskAppMongo: Flask, userModelMongo: UserModelMongo):
        with flaskAppMongo.test_request_context('/', json=self.authJson()):
            user = userModelMongo(
                login='test', password='test')
            user.save()
            token = DatabaseMethodMongo().generateHashToken()
        with flaskAppMongo.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethodMongo().loadUser()
            assert isinstance(g.user, AnonymousUser)

    def test_get_user_from_existent_token(self, flaskApp: Flask, userModel: UserModel):
        with flaskApp.test_request_context('/', json=self.authJson()):
            user = userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethodSql().generateSession(user)
        with flaskApp.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethodSql().loadUser()
            assert isinstance(g.user, UserMixin)

    def test_get_user_from_existent_token_mongo(self, flaskAppMongo: Flask, userModelMongo: UserModelMongo):
        with flaskAppMongo.test_request_context('/', json=self.authJson()):
            user = userModelMongo(
                login='test', password='test')
            user.save()
            token = DatabaseMethodMongo().generateSession(user)
        with flaskAppMongo.test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethodMongo().loadUser()
            assert isinstance(g.user, UserMixin)

