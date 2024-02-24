from flask import Flask
import pytest
from easy_framework.validator import Self_required

from test.easy_framework_conftest import FlaskClient
from easy_framework.exception import NotTheOwner, AuthMissingError
from easy_framework.view import GenericApiView
from easy_framework.model import BaseModelSql
from easy_framework.serializer import BaseSerializerSql
from easy_framework.model import BaseModelMongo
from easy_framework.serializer import BaseSerializerMongo
from mongoengine import fields as mo_fields

from marshmallow import fields as ma_fields
import sqlalchemy as sa

class ModelTestSql(BaseModelSql):
    __tablename__ = "ModelTestSql_self_required_validator_test"
    test = sa.String()

class SerializerTestSql(BaseSerializerSql):
    class Meta:
        test = ma_fields.String()


class MyViewSql(GenericApiView):
    routes = ['/test_self_required_validator']
    methods = ['GET', 'POST', 'PATCH', 'DELETE']
    serializer = SerializerTestSql
    model = ModelTestSql
    field_lookup = 'id'
    validator_list = [Self_required]
class ModelTestMongo(BaseModelMongo):
    __tablename__ = "ModelTestSql_self_required_validator_test"
    test = mo_fields.StringField()

class SerializerTestMongo(BaseSerializerMongo):
    class Meta:
        test = ma_fields.String()

class MyViewMongo(GenericApiView):
    routes = ['/test_self_required_validator']
    methods = ['GET', 'POST', 'PATCH', 'DELETE']
    serializer = SerializerTestMongo
    model = ModelTestMongo
    field_lookup = 'id'
    validator_list = [Self_required]
        
class TestSelfRequiredSql:
    def test_try_access_the_view_without_session_and_raises_error(self, flaskApp: Flask):
        with flaskApp.test_request_context():
            with pytest.raises(AuthMissingError) as exc_info:
                assert not MyViewSql().dispatch_request()

    def test_try_access_other_user_content_with_token_and_raises_error(self, flaskApp: Flask):
        client = FlaskClient()
        user = client.generate_user(flaskApp)
        user2 = client.generate_user(flaskApp, login='test2')
        token_user1 = client.get_session(flaskApp, user.login, '123')
        token_user2 = client.get_session(flaskApp, user2.login, '123')

        with flaskApp.test_request_context(headers={'Authorization':f'Bearer {token_user2}'}):
            user_2_ModelTestSql = ModelTestSql(test='testing with user 2').save()

        with flaskApp.test_request_context(headers={'Authorization':f'Bearer {token_user1}'}, query_string={'id':user_2_ModelTestSql.id}):
            with pytest.raises(NotTheOwner) as exc_info:
                assert not MyViewSql().dispatch_request()

    def test_try_access_self_content_with_token_and_get_200(self, flaskApp: Flask):
        client = FlaskClient()
        user = client.generate_user(flaskApp)
        token_user1 = client.get_session(flaskApp, user.login, '123')

        with flaskApp.test_request_context(headers={'Authorization':f'Bearer {token_user1}'}):
            user_1_ModelTestSql = ModelTestSql(test='testing with user 2').save()

        with flaskApp.test_request_context(headers={'Authorization':f'Bearer {token_user1}'}, query_string={'id':user_1_ModelTestSql.id}):
            assert MyViewSql().dispatch_request()

    def test_try_access_self_protected_view_with_post_and_get_200(self, flaskApp: Flask):
        client = FlaskClient()
        user = client.generate_user(flaskApp)
        token_user1 = client.get_session(flaskApp, user.login, '123')

        with flaskApp.test_request_context(method="POST", headers={'Authorization':f'Bearer {token_user1}'}, json={}):
            assert MyViewSql().dispatch_request()
class TestSelfRequiredMongo:
    def test_try_access_the_view_without_session_and_raises_error_mongo(self, flaskAppMongo: Flask):
        with flaskAppMongo.test_request_context():
            with pytest.raises(AuthMissingError) as exc_info:
                assert not MyViewMongo().dispatch_request()

    def test_try_access_other_user_content_with_token_and_raises_error_mongo(self, flaskAppMongo: Flask):
        client = FlaskClient()
        user = client.generate_user(flaskAppMongo)
        user2 = client.generate_user(flaskAppMongo, login='test2')
        token_user1 = client.get_session(flaskAppMongo, user.login, '123')
        token_user2 = client.get_session(flaskAppMongo, user2.login, '123')
        
        with flaskAppMongo.test_request_context(headers={'Authorization':f'Bearer {token_user2}'}):
            user_2_ModelTestMongo = ModelTestMongo(test='testing with user 2').save()
        
        with flaskAppMongo.test_request_context(headers={'Authorization':f'Bearer {token_user1}'}, query_string={'id':str(user_2_ModelTestMongo.id)}):
            with pytest.raises(NotTheOwner) as exc_info:
                assert not MyViewMongo().dispatch_request()

    def test_try_access_self_content_with_token_and_get_200_mongo(self, flaskAppMongo: Flask):
        client = FlaskClient()
        user = client.generate_user(flaskAppMongo)
        token_user1 = client.get_session(flaskAppMongo, user.login, '123')

        with flaskAppMongo.test_request_context(headers={'Authorization':f'Bearer {token_user1}'}):
            user_1_ModelTestMongo = ModelTestMongo(test='testing with user 2').save()

        with flaskAppMongo.test_request_context(headers={'Authorization':f'Bearer {token_user1}'}, query_string={'id':str(user_1_ModelTestMongo.id)}):
            
            assert MyViewMongo().dispatch_request()

    def test_try_access_self_protected_view_with_post_and_get_200_mongo(self, flaskAppMongo: Flask):
        client = FlaskClient()
        user = client.generate_user(flaskAppMongo)
        token_user1 = client.get_session(flaskAppMongo, user.login, '123')

        with flaskAppMongo.test_request_context(method="POST", headers={'Authorization':f'Bearer {token_user1}'}, json={}):
            assert MyViewMongo().dispatch_request()