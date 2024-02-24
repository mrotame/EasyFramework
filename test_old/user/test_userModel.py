from easy_framework.auth import PasswordManager
from easy_framework.user import UserModel
from easy_framework.user import UserModelMongo
from flask import Flask


class TestUserModel():      
    def test_save_new_user_into_database_and_check_if_its_password_is_hashed(self, flaskApp: Flask):
        with flaskApp.app_context():
            newUser = UserModel(login='test',password='test123').save()
            assert newUser.password != 'test'

    def test_save_new_user_into_database_and_compare_password_with_hash(self, flaskApp: Flask):
        with flaskApp.app_context():
            newUser = UserModel(login='test',password='test123').save()
            assert PasswordManager().compare('test123', newUser.password)   

    def test_save_new_user_into_database_and_check_if_its_password_is_hashed(self, flaskAppMongo: Flask):
        with flaskAppMongo.app_context():
            newUser = UserModelMongo(login='test',password='test123').save()
            assert newUser.password != 'test'

    def test_save_new_user_into_database_and_compare_password_with_hash(self, flaskAppMongo: Flask):
        with flaskAppMongo.app_context():
            newUser = UserModelMongo(login='test',password='test123').save()
            assert PasswordManager().compare('test123', newUser.password)