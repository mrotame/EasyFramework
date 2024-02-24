import bson

from flask import Flask
from pytest import fixture

from easy_framework import EasyFramework

from easy_framework.auth. _authModelMongo import AuthModelMongo
from easy_framework.user import UserModelMongo
from easy_framework.user import UserModel

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
    
    def generate_user(self, flaskApp: Flask, login: str = 'test', password='123'):
        with flaskApp.test_request_context():
            if flaskApp.client_name == 'sql':
                return UserModel(login=login, password=password).save()
            return UserModelMongo(login=login, password=password).save()
        
    def get_session(self, flaskApp: Flask, login, password):
        res = flaskApp.test_client().post('/auth', json={'login': login, 'password': password})
        return res.get_json()['auth_token']
    
class UserTestSql:
    flaskApp: Flask
    user: UserModel
    token: str
    def __init__(self, flaskApp: Flask, login: str, password: str):
        self.flaskApp = flaskApp
        self.user = self.create_user(flaskApp, login, password)
        self.token = self.login_user(flaskApp, login, password)

    def create_user(self, flaskApp: Flask, login: str, password: str)-> UserModel:
        with flaskApp.app_context():
            user = UserModel(login=login, password=password).save()
        return user

    def login_user(self, flaskApp: Flask, login:str, password:str)-> str:
        res = flaskApp.test_client().post('/auth',json={'login':login,'password':password})
        return res.get_json()['auth_token']

class UserTestMongo:
    flaskApp: Flask
    user: UserModelMongo
    token: str
    def __init__(self, flaskApp: Flask, login: str, password: str):
        self.flaskApp = flaskApp
        self.user = self.create_user(flaskApp, login, password)
        self.token = self.login_user(flaskApp, login, password)

    def create_user(self, flaskApp: Flask, login: str, password: str)-> UserModel:
        with flaskApp.app_context():
            user = UserModelMongo(login=login, password=password).save()
        return user

    def login_user(self, flaskApp: Flask, login:str, password:str)-> str:
        res = flaskApp.test_client().post('/auth',json={'login':login,'password':password})
        return res.get_json()['auth_token']

@fixture(scope="session")
def flaskApp():
    return FlaskClient().flaskApp

@fixture(scope='session')
def flaskAppMongo():
    return FlaskClient().flaskAppMongo

@fixture()
def sqldb(flaskApp:Flask):
    return flaskApp.config['EASY_FRAMEWORK_DB_SQLDB']

@fixture()
def mongodb(flaskAppMongo:Flask):
    return flaskAppMongo.config['EASY_FRAMEWORK_DB_MONGODB']
    
@fixture(autouse=True)
def easy_framework_between_tests(flaskApp: Flask, flaskAppMongo: Flask):
    flaskApp.config['EASY_FRAMEWORK_DB_SQLDB'].dbConfig.create_all()
    yield
    flaskApp.config['EASY_FRAMEWORK_DB_SQLDB'].dbConfig.close_all_sessions()
    flaskApp.config['EASY_FRAMEWORK_DB_SQLDB'].dbConfig.delete_all()
    flaskApp.config['EASY_FRAMEWORK_DB_MONGODB'].delete_all()
    flaskAppMongo.config['EASY_FRAMEWORK_DB_MONGODB'].delete_all()

def generate_objectid():
    return bson.ObjectId()