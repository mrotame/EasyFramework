from pytest import fixture
from flask import Flask, request
from easy_framework.view import GenericApiView
from easy_framework.validator import BaseValidator
from easy_framework.exception import ValidationError
from ..testClasses import ModelTestSql, SerializerValidatorSql
from test.easy_framework_conftest import FlaskClient

class TestGenericApiViewValidator:
    class Validator1(BaseValidator):
        def validate(self):
            if not request.get_json().get('validate_1'):
                raise ValidationError('error message 1', 401)

    class Validator2(BaseValidator):
        def validate(self):
            if not request.get_json().get('validate_2'):
                raise ValidationError('error message 2', 402)
    @property
    def viewArray(self):
        class GenericViewArray(GenericApiView):
            routes=['/GenericViewArray']
            methods = ["POST", "GET", "PATCH", "DELETE"]
            model = ModelTestSql
            serializer = SerializerValidatorSql
            field_lookup = "name"
            validator_list = [self.Validator1, self.Validator2]
            auto_treat_request = False

            def post(self):
                return 'ok', 200
            
            def get(self):
                return 'ok', 200

        return GenericViewArray
    
    @property
    def viewDict(self):
        class GenericViewDict(GenericApiView):
            routes=['/GenericViewDict']
            methods = ["POST", "GET", "PATCH", "DELETE"]
            model = ModelTestSql
            serializer = SerializerValidatorSql
            field_lookup = "name"
            validator_list = {
                '*': [self.Validator1],
                'get': [self.Validator2],
                'POst': [self.Validator2]
            }
            auto_treat_request = False

            def post(self):
                return 'ok', 200
            
            def get(self):
                return 'ok', 200
            
            def patch(self):
                return 'ok', 200
            
        return GenericViewDict

    @fixture()
    def flaskApp(self)-> Flask:
        flaskApp = FlaskClient().flaskApp
        viewArray = self.viewArray
        viewDict = self.viewDict
        flaskApp = flaskApp

        flaskApp.add_url_rule(viewArray.routes[0], view_func=viewArray.as_view("GenericViewArray"))

        flaskApp.add_url_rule(viewDict.routes[0], view_func=viewDict.as_view("GenericViewDict"))

        return flaskApp

    def test_get_ArrayView_with_validation_info_on_json_and_receive_200(self, flaskApp: Flask):
        res = flaskApp.test_client().get('/GenericViewArray', json={'validate_1': True, 'validate_2': True})
        assert res.status_code == 200

    def test_post_ArrayView_with_validation_info_on_json_and_receive_200(self, flaskApp: Flask):
        res = flaskApp.test_client().get('/GenericViewArray', json={'validate_1': True, 'validate_2': True})
        assert res.status_code == 200

    def test_get_ArrayView_without_validation_info_on_json_and_receive_error(self, flaskApp: Flask):
        res = flaskApp.test_client().get('/GenericViewArray', json={})
        assert res.status_code != 200

    def test_post_ArrayView_without_validation_info_on_json_and_receive_error(self, flaskApp: Flask):
        res = flaskApp.test_client().post('/GenericViewArray', json={})
        assert res.status_code != 200

    def test_get_DictView_with_validation_info_on_json_and_receive_200(self, flaskApp: Flask):
        res = flaskApp.test_client().get('/GenericViewDict', json={'validate_1': True, 'validate_2': True})
        assert res.status_code == 200

    def test_post_DictView_with_validation_info_on_json_and_receive_200(self, flaskApp: Flask):
        res = flaskApp.test_client().post('/GenericViewDict', json={'validate_1': True, 'validate_2': True})
        assert res.status_code == 200

    def test_get_DictView_without_validation_info_on_json_and_receive_error(self, flaskApp: Flask):
        res = flaskApp.test_client().get('/GenericViewDict', json={})
        assert res.status_code != 200

    def test_get_DictView_with_validate_1_info_on_json_and_receive_error(self, flaskApp: Flask):
        res = flaskApp.test_client().get('/GenericViewDict', json={'validate_1': True})
        assert res.status_code != 200

    def test_get_DictView_with_validate_2_info_on_json_and_receive_error(self, flaskApp: Flask):
        res = flaskApp.test_client().get('/GenericViewDict', json={'validate_2': True})
        assert res.status_code != 200

    def test_post_DictView_without_validation_info_on_json_and_receive_error(self, flaskApp: Flask):
        res = flaskApp.test_client().post('/GenericViewDict', json={})
        assert res.status_code != 200

    def test_patch_DictView_with_validate_1_info_on_json_and_receive_200(self, flaskApp: Flask):
        res = flaskApp.test_client().patch('/GenericViewDict', json={'validate_1': True})
        assert res.status_code == 200

    def test_patch_DictView_without_validate_1_info_on_json_and_receive_error(self, flaskApp: Flask):
        res = flaskApp.test_client().patch('/GenericViewDict', json={})
        assert res.status_code != 200