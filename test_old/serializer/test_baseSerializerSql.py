from flask import Flask, request
import pytest
from marshmallow import ValidationError
from ..testClasses import SerializerTestSql

class TestBaseSerializerSql:
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

    def test_load_post_serializer_with_full_json_and_get_no_errors(self, flaskApp: Flask):
        with flaskApp.test_request_context('/', json=self.post_json, method='POST'):
            serializer = self.getMethodBasedSerializer()
            serializer.load(request.json)

    def test_load_post_serializer_with_partial_json_and_get_no_errors(self, flaskApp: Flask):
        json = self.post_json
        del json['age']
        del json['name']
        with flaskApp.test_request_context('/', json=json, method='POST'):
            serializer = self.getMethodBasedSerializer()
            serializer.load(request.json)

    def test_load_post_serializer_without_required_fields_and_catch_error(self, flaskApp: Flask):
        json = self.post_json
        del json['username']
        del json['password']
        with flaskApp.test_request_context('/', json=json, method='POST'):
            serializer = self.getMethodBasedSerializer()
            with pytest.raises(ValidationError) as e_info:
                serializer.load(request.json)
            assert 'password' in str(e_info)
            assert 'username' in str(e_info)
            assert 'Missing data for required field' in str(e_info)

    def test_load_update_serializer_without_required_field_and_get_no_errors(self, flaskApp: Flask):
        with flaskApp.test_request_context('/', json=self.patch_json, method='PATCH'):
            serializer = self.getMethodBasedSerializer()
            serializer.load(request.json)

    def test_load_update_serializer_without_required_field_and_catch_error(self, flaskApp: Flask):
        json = self.post_json
        del json['username']
        with flaskApp.test_request_context('/', json=json, method='POST'):
            serializer = self.getMethodBasedSerializer()
            with pytest.raises(ValidationError) as e_info:
                serializer.load(request.json)
            assert 'username' in str(e_info)
            assert 'Missing data for required field' in str(e_info)