from flask import request
from marshmallow import ValidationError

from tests import TestCase
from tests.classes import SerializerTestSql

class TestBaseSerializerSql(TestCase):
    def getMethodBasedSerializer(self):
        return SerializerTestSql()

    @property
    def post_json(self):
        return {
            'username': 'test',
            'password': 'test123',
            'age': 18,
            'name': 'Anna'
        }

    @property
    def patch_json(self):
        return {
            'username':'test2',
            'age': 19,
        }

    def test_load_post_serializer_with_full_json_and_get_no_errors(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.post_json, method='POST'):
            serializer = self.getMethodBasedSerializer()
            serializer.load(request.json)

    def test_load_post_serializer_with_partial_json_and_get_no_errors(self):
        json = self.post_json
        del json['age']
        del json['name']
        with self.get_flask_app_sql().test_request_context('/', json=json, method='POST'):
            serializer = self.getMethodBasedSerializer()
            serializer.load(request.json)

    def test_load_post_serializer_without_required_fields_and_catch_error(self):
        json = self.post_json
        del json['username']
        del json['password']
        with self.get_flask_app_sql().test_request_context('/', json=json, method='POST'):
            serializer = self.getMethodBasedSerializer()
            with self.assertRaises(ValidationError) as e_info:
                serializer.load(request.json)
            self.assertTrue('password' in str(e_info.exception))
            self.assertTrue('username' in str(e_info.exception))
            self.assertTrue('Missing data for required field' in str(e_info.exception))

    def test_load_update_serializer_without_required_field_and_get_no_errors(self):
        with self.get_flask_app_sql().test_request_context('/', json=self.patch_json, method='PATCH'):
            serializer = self.getMethodBasedSerializer()
            serializer.load(request.json)

    def test_load_update_serializer_without_required_field_and_catch_error(self):
        json = self.post_json
        del json['username']
        with self.get_flask_app_sql().test_request_context('/', json=json, method='POST'):
            serializer = self.getMethodBasedSerializer()
            with self.assertRaises(ValidationError) as e_info:
                serializer.load(request.json)
            self.assertTrue('username' in str(e_info.exception))
            self.assertTrue('Missing data for required field' in str(e_info.exception))