from datetime import datetime, timedelta

from flask import Flask

from easy_framework.auth import AuthModel
from easy_framework.auth import AuthModelMongo
from test.easy_framework_conftest import generate_objectid
from test.view import test_genericApiView_validator


class TestAuthModel():
    def test_insert_new_session_and_check_it_values(self, flaskApp: Flask):
        with flaskApp.test_request_context():
            session = AuthModel(user_id=1, token='123').save()
            assert session.user_id == 1
            assert session.token == '123'
            assert type(session.expiration_date) is datetime

    def test_insert_new_session_and_check_its_expiration_datetime(self, flaskApp: Flask):
        with flaskApp.test_request_context():
            session = AuthModel(user_id=1, token='123').save()
            assert session.expiration_date > datetime.now()
            assert session.expiration_date < datetime.now() + flaskApp.config.get('EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION')

    def test_insert_new_session_and_check_it_values_mongo(self, flaskAppMongo: Flask):
        with flaskAppMongo.test_request_context():
            _id = generate_objectid()
            session = AuthModelMongo(user_id=_id, token='123').save()
            assert session.user_id == _id
            assert session.token == '123'
            assert type(session.expiration_date) is datetime

    def test_insert_new_session_and_check_its_expiration_datetime_mongo(self, flaskAppMongo: Flask):
        with flaskAppMongo.test_request_context():
            _id = generate_objectid()
            session = AuthModelMongo(user_id=_id, token='123').save()
            assert session.expiration_date > datetime.now()
            assert session.expiration_date < datetime.now() + flaskAppMongo.config.get('EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION')