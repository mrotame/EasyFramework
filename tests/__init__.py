import os
from unittest import TestCase as _TestCase
from dotenv import load_dotenv

load_dotenv()

from flask import Flask
import bson

from easy_framework import EasyFramework
from easy_framework.auth._authModelMongo import AuthModelMongo
from easy_framework.auth._authModel import AuthModel
from easy_framework.user import UserModelMongo
from easy_framework.user import UserModel
from easy_framework.database.sql import Sqldb
from easy_framework.database.mongo import Mongodb
from easy_framework._context import cache


def generate_objectid():
    return bson.ObjectId()


class TestCase(_TestCase):
    def get_flask_app_sql(self):
        return FlaskClient().flaskApp

    def get_flask_app_mongo(self):
        return FlaskClient().flaskAppMongo

    def get_sqldb(self) -> Sqldb:
        return cache.config.EASY_FRAMEWORK_DB_SQLDB

    def get_mongodb(self) -> Mongodb:
        return cache.config.EASY_FRAMEWORK_DB_MONGODB

    def setUp(self) -> None:
        self.get_flask_app_sql()
        cache.config.EASY_FRAMEWORK_DB_SQLDB.dbConfig.create_all()

    def tearDown(self) -> None:
        cache.config.EASY_FRAMEWORK_DB_SQLDB.dbConfig.close_all_sessions()
        cache.config.EASY_FRAMEWORK_DB_SQLDB.dbConfig.delete_all()
        cache.config.EASY_FRAMEWORK_DB_MONGODB.delete_all()


class FlaskClient:
    def __init__(self):
        self.db_dialect = os.environ.get("db_test_dialect")
        self.db_name = os.environ.get("db_test_name")
        self.host = os.environ.get("db_test_host")
        self.port = os.environ.get("db_test_port")
        self.username = os.environ.get("db_test_username")
        self.password = os.environ.get("db_test_password")

    @property
    def flaskApp(self) -> Flask:
        app = Flask(__name__)
        easy_framework = EasyFramework(app)

        app.client_name = "sql"
        cache.config.EASY_FRAMEWORK_ENVIRONMENT = "test"
        cache.config.EASY_FRAMEWORK_DB_TEST_SQL_DBNAME = self.db_name
        cache.config.EASY_FRAMEWORK_DB_TEST_SQL_DIALECT = self.db_dialect
        cache.config.EASY_FRAMEWORK_DB_TEST_SQL_PORT = self.port
        cache.config.EASY_FRAMEWORK_DB_TEST_SQL_URI = f"{self.host}"
        cache.config.EASY_FRAMEWORK_DB_TEST_SQL_USERNAME = self.username
        cache.config.EASY_FRAMEWORK_DB_TEST_SQL_PASSWORD = self.password
        cache.config.EASY_FRAMEWORK_DB_MONGO_ACTIVATE = True
        cache.config.EASY_FRAMEWORK_DB_TEST_SQL_CREATE_ALL = True

        cache.config.EASY_FRAMEWORK_DB_SQL_ACTIVATE = True
        cache.config.EASY_FRAMEWORK_AUTH_METHOD = "database_sql"
        cache.config.EASY_FRAMEWORK_AUTH_MODEL = AuthModel
        cache.config.EASY_FRAMEWORK_USER_MODEL = UserModel
        easy_framework.run_all_configs()
        return app

    @property
    def flaskAppMongo(self) -> Flask:
        app = Flask(__name__)
        easy_framework = EasyFramework(app)

        app.client_name = "mongo"
        cache.config.EASY_FRAMEWORK_DB_SQL_ACTIVATE = False
        cache.config.EASY_FRAMEWORK_AUTH_METHOD = "database_mongo"
        cache.config.EASY_FRAMEWORK_AUTH_MODEL = AuthModelMongo
        cache.config.EASY_FRAMEWORK_DB_MONGO_ACTIVATE = True
        cache.config.EASY_FRAMEWORK_USER_MODEL = UserModelMongo
        easy_framework.run_all_configs()
        return app

    def generate_user(
        self, flaskApp: Flask, login: str = "test", password="123"
    ) -> UserModelMongo:
        with flaskApp.test_request_context():
            if flaskApp.client_name == "sql":
                return UserModel(login=login, password=password).save()
            return UserModelMongo(login=login, password=password).save()

    def get_session(self, flaskApp: Flask, login, password) -> str:
        res = flaskApp.test_client().post(
            "/auth", json={"login": login, "password": password}
        )
        return res.get_json()["auth_token"]
