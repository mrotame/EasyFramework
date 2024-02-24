import pytest
from random import randint
from pytest import fixture

from easy_framework.exception import AuthMissingError
from easy_framework.validator import BaseValidator

from easy_framework.view import GenericApiView
from test.testClasses import SerializerTestSql, ModelTestSql
from test.easy_framework_conftest import FlaskClient

class TestBaseValidator():
    flaskApp = FlaskClient().get_flaskApp()

    @fixture
    def trueValidatorTest(self):
        class TrueValidator(BaseValidator):
            def validate(self) -> bool:
                pass
        return TrueValidator

    @fixture
    def falseValidatorTest(self):
        class FalseValidator(BaseValidator):
            def validate(self) -> bool:
                raise AuthMissingError()
        return FalseValidator

    @fixture
    def paramValidatorTest(self):
        class ParamValidator(BaseValidator):
            def validate(self, shouldRaise: bool) -> bool:
                if shouldRaise:
                    raise AuthMissingError()
        return ParamValidator

    class ObjectiveClass(GenericApiView):
        serializer = SerializerTestSql
        model = ModelTestSql
        field_lookup = 'id'
        methods = ['GET']
        routes = '/'

    def test_validade_the_objective_function_and_return_true_with_a_valid_validator(self, trueValidatorTest): 
        @trueValidatorTest()
        class _ObjectiveClass(self.ObjectiveClass):
            pass
        
        with self.flaskApp.test_request_context():
            _ObjectiveClass()._validate()

    def test_validade_the_objective_function_and_catch_exception_with_an_invalid_validator(self, falseValidatorTest):
        @falseValidatorTest()
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with pytest.raises(AuthMissingError) as exc_info:
            with self.flaskApp.test_request_context():
                _ObjectiveClass()._validate()
                assert exc_info is AuthMissingError

    def test_validate_the_objective_function_with_decorator_with_params(self, paramValidatorTest):
        @paramValidatorTest(False)
        class _ObjectiveClass(self.ObjectiveClass):
            pass
        with self.flaskApp.test_request_context():
            _ObjectiveClass()._validate()

    def test_validate_the_objective_function_with_decorator_with_params_and_catch_exception(self, paramValidatorTest):
        @paramValidatorTest(True)
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with pytest.raises(AuthMissingError) as exc_info:
            with self.flaskApp.test_request_context():
                _ObjectiveClass()._validate()
                assert exc_info is AuthMissingError

    def test_validade_the_objective_function_with_internal_funciton_with_params_and_get_true_with_a_valid_validator(self, paramValidatorTest):
        @paramValidatorTest(False)
        class _ObjectiveClass(self.ObjectiveClass):
            def __init__(self):
                pass

            def func(self, foo: bool, bar: str, eggs: int):
                return True
            
        _ObjectiveClass()._validate
        assert _ObjectiveClass().func(True, 'test', 100) is True

    def test_validade_the_objective_function_with_internal_funciton_with_params_and_validate_internal_params_with_a_valid_validator(self, paramValidatorTest):
        @paramValidatorTest(False)
        class _ObjectiveClass(self.ObjectiveClass):
            def __init__(self):
                pass

            def func(self, foo: bool, bar: str, eggs: int):
                self.foo = foo
                self.bar = bar
                self.eggs = eggs

        _ObjectiveClass()._validate
        func = _ObjectiveClass()
        func.func(True, 'test', 100)

        assert func.foo == True
        assert func.bar == 'test'
        assert func.eggs == 100

    def test_validate_the_objective_function_by_calling_the_validator_directly(self, trueValidatorTest):

        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with FlaskClient().get_flaskApp().test_request_context():
            trueValidatorTest(_ObjectiveClass)

    def test_true_validate_the_objective_function_with_correct_HTTP_method_and_get_correct_result(self, trueValidatorTest):
        
        @trueValidatorTest(methods_to_validate=['GET'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with FlaskClient().get_flaskApp().test_request_context(method='GET'):
            _ObjectiveClass()._validate()

    def test_false_validate_the_objective_function_with_correct_HTTP_method_and_get_error(self, falseValidatorTest):
        @falseValidatorTest(methods_to_validate=['GET'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with pytest.raises(AuthMissingError) as exc_info:
            
            with FlaskClient().get_flaskApp().test_request_context(method='GET'):
                _ObjectiveClass()._validate()
                assert exc_info is AuthMissingError

    def test_true_validate_the_objective_function_with_wrong_HTTP_method_and_get_correct_result(self, trueValidatorTest):
        
        @trueValidatorTest(methods_to_validate=['POST'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with FlaskClient().get_flaskApp().test_request_context(method='GET'):
            _ObjectiveClass()._validate()

    def test_false_validate_the_objective_function_with_wrong_HTTP_method_and_get_error(self, falseValidatorTest):
        @falseValidatorTest(methods_to_validate=['POST'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with FlaskClient().get_flaskApp().test_request_context(method='GET'):
            _ObjectiveClass()._validate()
                
    def test_param_validate_the_objective_function_with_correct_http_method_and_false_shouldRaise(self, paramValidatorTest):
        @paramValidatorTest(False, methods_to_validate=['GET'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with FlaskClient().get_flaskApp().test_request_context(method='GET'):
            _ObjectiveClass()._validate()

    def test_param_validate_the_objective_function_with_correct_http_method_and_True_shouldRaise(self, paramValidatorTest):
        @paramValidatorTest(True, methods_to_validate=['GET'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with pytest.raises(AuthMissingError) as exc_info:
            with FlaskClient().get_flaskApp().test_request_context(method='GET'):
                _ObjectiveClass()._validate()   
                assert exc_info is AuthMissingError

    def test_decorate_function(self, trueValidatorTest):
        @trueValidatorTest()
        def my_func():
            return True
        
        assert my_func()

    def test_decorate_function_with_false_validator_and_get_AuthMissingError(self, falseValidatorTest):

        @falseValidatorTest()
        def my_func():
            return True
        
        with pytest.raises(AuthMissingError) as exc_info:
            my_func()
            assert exc_info is AuthMissingError

    def test_decorate_function_with_true_param_validator_and_get_AuthMissingError(self, paramValidatorTest):

        @paramValidatorTest(True)
        def my_func():
            return True
        
        with pytest.raises(AuthMissingError) as exc_info:
            my_func()
            assert exc_info is AuthMissingError

    def test_decorate_method(self, trueValidatorTest):
        class _Test:
            @trueValidatorTest()
            def my_func(self, a):
                return a
        
        assert _Test().my_func(100) == 100

    def test_decorate_method_with_false_validate_and_get_error(self, falseValidatorTest):
        class _Test:
            @falseValidatorTest()
            def my_func(self):
                return True
        
        with pytest.raises(AuthMissingError) as exc_info:
            _Test().my_func()
            assert exc_info is AuthMissingError

    def test_true_validate_random_class(self, trueValidatorTest):
        @trueValidatorTest()
        class RandomClass:
            def __new__(cls):
                return 100
            
        assert RandomClass() == 100

    def test_false_validate_random_class_and_get_error(self, falseValidatorTest):

        @falseValidatorTest()
        class RandomClass:
            def __new__(cls):
                return 100
            
        with pytest.raises(AuthMissingError) as exc_info:
            assert RandomClass() != 100
            assert exc_info is AuthMissingError

    def test_true_validator_direct_call(self, trueValidatorTest):
        class TestClass():
            pass

        assert trueValidatorTest(TestClass)

    def test_false_validator_direct_call(self, falseValidatorTest):
        class TestClass():
            pass
        
        with pytest.raises(AuthMissingError) as exc_info:
            falseValidatorTest(TestClass)

            assert exc_info is AuthMissingError

    def test_false_param_validator_direct_call(self, paramValidatorTest):
        class TestClass():
            pass
        
        assert paramValidatorTest(TestClass, False)

    def test_true_param_validator_direct_call(self, paramValidatorTest):
        class TestClass():
            pass
        
        with pytest.raises(AuthMissingError) as exc_info:
            paramValidatorTest(TestClass, True)
            assert exc_info is AuthMissingError

    def test_mult_decorator_return_correct_function(self, trueValidatorTest, paramValidatorTest):

        @trueValidatorTest()
        @paramValidatorTest(False)
        def test():
            return "Hi"
        
        @paramValidatorTest(False)
        @trueValidatorTest()
        def test2():
            return "Hi"
        
        assert test() == 'Hi'
        assert test2() == 'Hi'

    def test_mult_decorator_with_validation_error_raises_exception(self, trueValidatorTest, paramValidatorTest, falseValidatorTest):

        @trueValidatorTest()
        @paramValidatorTest(False)
        @falseValidatorTest()
        def test():
            return "Hi"
        
        @falseValidatorTest()
        @paramValidatorTest(False)
        @trueValidatorTest()
        def test2():
            return "Hi"
        
        @paramValidatorTest(True)
        @trueValidatorTest()
        def test3():
            return "Hi"
        
        with pytest.raises(AuthMissingError) as exc_info1:
            test()
            assert exc_info1 is AuthMissingError
        
        with pytest.raises(AuthMissingError) as exc_info2:
            test2() 
            assert exc_info2 is AuthMissingError

        with pytest.raises(AuthMissingError) as exc_info3:
            test3() 
            assert exc_info3 is AuthMissingError