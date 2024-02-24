from unittest import TestCase as _TestCase

from flask import Flask
import bson

from easy_framework import EasyFramework
from easy_framework.auth. _authModelMongo import AuthModelMongo
from easy_framework.user import UserModelMongo
from easy_framework.user import UserModel
from easy_framework.database.sql import Sqldb
from easy_framework.database.mongo import Mongodb

def generate_objectid():
    return bson.ObjectId()

class TestCase(_TestCase):
    def get_flask_app_sql(self):
        return FlaskClient().flaskApp

    def get_flask_app_mongo(self):
        return FlaskClient().flaskAppMongo
    
    def get_sqldb(self)-> Sqldb:
        return self.get_flask_app_sql().config['EASY_FRAMEWORK_DB_SQLDB']

    def get_mongodb(self)-> Mongodb:
        return self.get_flask_app_mongo().config['EASY_FRAMEWORK_DB_MONGODB']

    def setUp(self) -> None:
        self.get_flask_app_sql().config['EASY_FRAMEWORK_DB_SQLDB'].dbConfig.create_all()

    def tearDown(self) -> None:
        self.get_flask_app_sql().config['EASY_FRAMEWORK_DB_SQLDB'].dbConfig.close_all_sessions()
        self.get_flask_app_sql().config['EASY_FRAMEWORK_DB_SQLDB'].dbConfig.delete_all()
        self.get_flask_app_sql().config['EASY_FRAMEWORK_DB_MONGODB'].delete_all()
        self.get_flask_app_mongo().config['EASY_FRAMEWORK_DB_MONGODB'].delete_all()


class FlaskClient:
    def __init__(self):
        self.flaskApp = self.get_flaskApp()
        self.flaskAppMongo = self.get_flaskAppMongo()

    def get_flaskApp(self)-> Flask:
        app = Flask(__name__)
        app.client_name = 'sql'
        app.config['EASY_FRAMEWORK_DB_SQL_DBNAME'] = 'testdb.db'
        app.config['EASY_FRAMEWORK_DB_SQL_URI'] = '/'
        app.config['EASY_FRAMEWORK_DB_MONGO_ACTIVATE'] = True
        app.config['EASY_FRAMEWORK_DB_SQL_CREATE_ALL'] = True
        EasyFramework(app)
        return app
    
    def get_flaskAppMongo(self)-> Flask:
        app = Flask(__name__)
        app.client_name = 'mongo'
        app.config['EASY_FRAMEWORK_DB_SQL_ACTIVATE'] = False
        app.config['EASY_FRAMEWORK_AUTH_METHOD'] = 'database_mongo'
        app.config['EASY_FRAMEWORK_AUTH_MODEL'] = AuthModelMongo
        app.config['EASY_FRAMEWORK_DB_MONGO_ACTIVATE'] = True
        app.config['EASY_FRAMEWORK_USER_MODEL'] = UserModelMongo
        
        EasyFramework(app)
        return app
    
    def generate_user(
            self, 
            flaskApp: Flask, 
            login: str = 'test', 
            password='123'
    )-> UserModelMongo:
        with flaskApp.test_request_context():
            if flaskApp.client_name == 'sql':
                return UserModel(login=login, password=password).save()
            return UserModelMongo(login=login, password=password).save()
        
    def get_session(self, flaskApp: Flask, login, password)-> str:
        res = flaskApp.test_client().post('/auth', json={'login': login, 'password': password})
        return res.get_json()['auth_token']
    

