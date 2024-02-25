import typing as t

from mongoengine import fields as mo_fields
from marshmallow import fields as ma_fields
import sqlalchemy as sa
from sqlalchemy import orm

from easy_framework.validator import Self_required
from easy_framework.exception import NotTheOwner, AuthMissingError
from easy_framework.view import GenericApiView
from easy_framework.model import BaseModelSql
from easy_framework.serializer import BaseSerializerSql
from easy_framework.model import BaseModelMongo
from easy_framework.serializer import BaseSerializerMongo
from tests import TestCase
from tests import FlaskClient

class ModelTestSql(BaseModelSql):
    __tablename__ = "ModelTestSql_self_required_validator_test"
    test: orm.Mapped[t.Optional[str]] = orm.mapped_column(default=None)

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
        
class TestSelfRequiredSql(TestCase):

    def test_try_access_the_view_without_session_and_raises_error(self):
        with self.get_flask_app_sql().test_request_context():
            with self.assertRaises(AuthMissingError) as exc_info:
                self.assertFalse(MyViewSql().dispatch_request())

    def test_try_access_other_user_content_with_token_and_raises_error(self):
        client = FlaskClient()
        user = client.generate_user(self.get_flask_app_sql())
        user2 = client.generate_user(self.get_flask_app_sql(), login='test2')
        token_user1 = client.get_session(self.get_flask_app_sql(), user.login, '123')
        token_user2 = client.get_session(self.get_flask_app_sql(), user2.login, '123')

        with self.get_flask_app_sql().test_request_context(headers={'Authorization':f'Bearer {token_user2}'}):
            user_2_ModelTestSql = ModelTestSql(test='testing with user 2').save()

        with self.get_flask_app_sql().test_request_context(headers={'Authorization':f'Bearer {token_user1}'}, query_string={'id':user_2_ModelTestSql.id}):
            with self.assertRaises(NotTheOwner) as exc_info:
                self.assertFalse(MyViewSql().dispatch_request())

    def test_try_access_self_content_with_token_and_get_200(self):
        client = FlaskClient()
        user = client.generate_user(self.get_flask_app_sql())
        token_user1 = client.get_session(self.get_flask_app_sql(), user.login, '123')

        with self.get_flask_app_sql().test_request_context(headers={'Authorization':f'Bearer {token_user1}'}):
            user_1_ModelTestSql = ModelTestSql(test='testing with user 2').save()

        with self.get_flask_app_sql().test_request_context(headers={'Authorization':f'Bearer {token_user1}'}, query_string={'id':user_1_ModelTestSql.id}):
            self.assertTrue( MyViewSql().dispatch_request())

    def test_try_access_self_protected_view_with_post_and_get_200(self):
        client = FlaskClient()
        user = client.generate_user(self.get_flask_app_sql())
        token_user1 = client.get_session(self.get_flask_app_sql(), user.login, '123')

        with self.get_flask_app_sql().test_request_context(method="POST", headers={'Authorization':f'Bearer {token_user1}'}, json={}):
            self.assertTrue(MyViewSql().dispatch_request())

class TestSelfRequiredMongo(TestCase):
    def test_try_access_the_view_without_session_and_raises_error_mongo(self):
        with self.get_flask_app_mongo().test_request_context():
            with self.assertRaises(AuthMissingError) as exc_info:
                self.assertFalse(MyViewMongo().dispatch_request())

    def test_try_access_other_user_content_with_token_and_raises_error_mongo(self):
        client = FlaskClient()
        user = client.generate_user(self.get_flask_app_mongo())
        user2 = client.generate_user(self.get_flask_app_mongo(), login='test2')
        token_user1 = client.get_session(self.get_flask_app_mongo(), user.login, '123')
        token_user2 = client.get_session(self.get_flask_app_mongo(), user2.login, '123')
        
        with self.get_flask_app_mongo().test_request_context(headers={'Authorization':f'Bearer {token_user2}'}):
            user_2_ModelTestMongo = ModelTestMongo(test='testing with user 2').save()
        
        with self.get_flask_app_mongo().test_request_context(headers={'Authorization':f'Bearer {token_user1}'}, query_string={'id':str(user_2_ModelTestMongo.id)}):
            with self.assertRaises(NotTheOwner) as exc_info:
                self.assertFalse(MyViewMongo().dispatch_request())

    def test_try_access_self_content_with_token_and_get_200_mongo(self):
        client = FlaskClient()
        user = client.generate_user(self.get_flask_app_mongo())
        token_user1 = client.get_session(self.get_flask_app_mongo(), user.login, '123')

        with self.get_flask_app_mongo().test_request_context(headers={'Authorization':f'Bearer {token_user1}'}):
            user_1_ModelTestMongo = ModelTestMongo(test='testing with user 2').save()

        with self.get_flask_app_mongo().test_request_context(headers={'Authorization':f'Bearer {token_user1}'}, query_string={'id':str(user_1_ModelTestMongo.id)}):
            
            self.assertTrue(MyViewMongo().dispatch_request())

    def test_try_access_self_protected_view_with_post_and_get_200_mongo(self):
        client = FlaskClient()
        user = client.generate_user(self.get_flask_app_mongo())
        token_user1 = client.get_session(self.get_flask_app_mongo(), user.login, '123')

        with self.get_flask_app_mongo().test_request_context(method="POST", headers={'Authorization':f'Bearer {token_user1}'}, json={}):
            self.assertTrue(MyViewMongo().dispatch_request())