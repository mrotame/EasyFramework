from easy_framework.auth import PasswordManager
from easy_framework.user import UserModel
from easy_framework.user import UserModelMongo
from tests import TestCase


class TestUserModel(TestCase):
    def test_save_new_user_into_sql_database_and_check_if_its_password_is_hashed(self):
        with self.get_flask_app_sql().app_context():
            newUser = UserModel(login='test',password='test123').save()
            self.assertNotEqual(newUser.password, 'test')

    def test_save_new_user_into_sql_database_and_compare_password_with_hash(self):
        with self.get_flask_app_sql().app_context():
            newUser = UserModel(login='test',password='test123').save()
            self.assertTrue(PasswordManager().compare('test123', newUser.password))

    def test_save_new_user_into_database_and_check_if_its_password_is_hashed(self):
        with self.get_flask_app_mongo().app_context():
            newUser = UserModelMongo(login='test',password='test123').save()
            self.assertNotEqual(newUser.password, 'test')

    def test_save_new_user_into_database_and_compare_password_with_hash(self):
        with self.get_flask_app_mongo().app_context():
            newUser = UserModelMongo(login='test',password='test123').save()
            self.assertTrue(PasswordManager().compare('test123', newUser.password))