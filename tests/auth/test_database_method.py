import typing as t
from flask import g

from tests import TestCase
from easy_framework.auth import AuthModel
from easy_framework.auth import AuthModelMongo
from easy_framework.auth import DatabaseMethodSql
from easy_framework.auth import DatabaseMethodMongo
from easy_framework.exception.apiExceptions import InvalidCredentials
from easy_framework.user.userModel import UserModel
from easy_framework.user.userModelMongo import UserModelMongo
from easy_framework.user.userMixin import AnonymousUser, UserMixin


class TestDatabaseMethod(TestCase):
    def authJson(self):
        return {
            'login': 'test',
            'password': 'test'
        }
    
    @property
    def userModel(self)-> t.Type[UserModel]:
        return self.get_flask_app_sql().config.get('EASY_FRAMEWORK_USER_MODEL')
    
    @property
    def userModelMongo(self)-> t.Type[UserModelMongo]:
        return UserModelMongo
    
    def test_generate_hash_token(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.authJson()):
            
            self.assertGreaterEqual(len(DatabaseMethodSql().generateHashToken()), 128)

    def test_request_a_new_token_with_no_user_registered_and_get_404(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.authJson()):
            with self.assertRaises(InvalidCredentials) as exc_info:
                DatabaseMethodSql().generateSession(None)
                
                self.assertIsInstance(exc_info.value, InvalidCredentials)

    def test_request_a_new_token_and_get_token(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.authJson()):
            user = self.userModel(login='test', password='test').save()
            token = DatabaseMethodSql().generateSession(user)
            
            self.assertIsNotNone(token)
            self.assertIsInstance(token, str)
            
    def test_request_a_new_token_and_get_token_using_mongo_model(self):
        with self.get_flask_app_mongo().test_request_context('/', json=self.authJson()):
            user = self.userModelMongo(login='test', password='test').save()
            token = DatabaseMethodMongo().generateSession(user)
            
            self.assertIsNotNone(token)
            self.assertIsInstance(token, str)

    def test_request_a_new_token_and_check_token_in_database(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.authJson()):
            user = self.userModel(
                login='test', 
                password='test'
            )
            user.save()
            token = DatabaseMethodSql().generateSession(user)
            tokenModel: AuthModel = AuthModel.get_one(AuthModel.token == token)

            self.assertIsNotNone(tokenModel)
            self.assertEqual(tokenModel.user_id, user.id)

    def test_request_a_new_token_and_check_token_in_database_mongo(self):
        with self.get_flask_app_mongo().test_request_context('/', json=self.authJson()):
            user = self.userModelMongo(
                login='test', 
                password='test'
            )
            user.save()
            token = DatabaseMethodMongo().generateSession(user)
            tokenModel: AuthModelMongo = AuthModelMongo.get_one(AuthModel.token == token)
            
            self.assertIsNotNone(tokenModel)
            self.assertEqual(tokenModel.user_id, user.id)

    def test_check_an_existent_token(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.authJson()):
            user = self.userModel(
                login='test', 
                password='test'
            )
            user.save()
            token = DatabaseMethodSql().generateSession(user)
            with self.get_flask_app_sql().test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
                DatabaseMethodSql().loadUser()

                self.assertIsNotNone(g.user)

    def test_check_an_existent_token_mongo(self):
        with self.get_flask_app_mongo().test_request_context('/', json=self.authJson()):
            user = self.userModelMongo(
                login='test', 
                password='test'
            )
            user.save()
            token = DatabaseMethodMongo().generateSession(user)
            with self.get_flask_app_mongo().test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
                DatabaseMethodMongo().loadUser()

                self.assertIsNotNone(g.user)

    def test_check_an_nonexistent_token(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.authJson()):
            user = self.userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethodSql().generateHashToken()
        with self.get_flask_app_sql().test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethodSql().loadUser()

            self.assertIsInstance(g.user, AnonymousUser)

    def test_check_an_nonexistent_token_mongo(self):
        with self.get_flask_app_mongo().test_request_context('/', json=self.authJson()):
            user = self.userModelMongo(
                login='test', password='test')
            user.save()
            token = DatabaseMethodMongo().generateHashToken()
        with self.get_flask_app_mongo().test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethodMongo().loadUser()

            self.assertIsInstance(g.user, AnonymousUser)

    def test_get_user_from_existent_token(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.authJson()):
            user = self.userModel(
                login='test', password='test')
            user.save()
            token = DatabaseMethodSql().generateSession(user)
        with self.get_flask_app_sql().test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethodSql().loadUser()

            self.assertIsInstance(g.user, UserMixin)

    def test_get_user_from_existent_token_mongo(self):
        with self.get_flask_app_mongo().test_request_context('/', json=self.authJson()):
            user = self.userModelMongo(
                login='test', password='test')
            user.save()
            token = DatabaseMethodMongo().generateSession(user)
        with self.get_flask_app_mongo().test_request_context('/', headers={'Authorization': f'Bearer {token}'}):
            DatabaseMethodMongo().loadUser()
            
            self.assertIsInstance(g.user, UserMixin)