from flask import Flask

from easy_framework.exception import AuthMissingError
from easy_framework.validator import BaseValidator
from easy_framework.view import GenericApiView
from tests import TestCase
from tests.classes import SerializerTestSql, ModelTestSql

class TestBaseValidator(TestCase):

    @property
    def flaskApp(self)-> Flask:
        return self.get_flask_app_sql()

    @property
    def trueValidatorTest(self):
        class TrueValidator(BaseValidator):
            def validate(self) -> bool:
                pass
        return TrueValidator

    @property
    def falseValidatorTest(self):
        class FalseValidator(BaseValidator):
            def validate(self) -> bool:
                raise AuthMissingError()
        return FalseValidator

    @property
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

    def test_validade_the_objective_function_and_return_true_with_a_valid_validator(self): 
        @self.trueValidatorTest()
        class _ObjectiveClass(self.ObjectiveClass):
            pass
        
        with self.flaskApp.test_request_context():
            _ObjectiveClass()._validate()

    def test_validade_the_objective_function_and_catch_exception_with_an_invalid_validator(self):
        @self.falseValidatorTest()
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.assertRaises(AuthMissingError) as exc_info:
            with self.flaskApp.test_request_context():
                _ObjectiveClass()._validate()
                self.assertIsInstance(exc_info, AuthMissingError)

    def test_validate_the_objective_function_with_decorator_with_params(self):
        @self.paramValidatorTest(False)
        class _ObjectiveClass(self.ObjectiveClass):
            pass
        with self.flaskApp.test_request_context():
            _ObjectiveClass()._validate()

    def test_validate_the_objective_function_with_decorator_with_params_and_catch_exception(self):
        @self.paramValidatorTest(True)
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.assertRaises(AuthMissingError) as exc_info:
            with self.flaskApp.test_request_context():
                _ObjectiveClass()._validate()
                self.assertIsInstance(exc_info is AuthMissingError)

    def test_validade_the_objective_function_with_internal_funciton_with_params_and_get_true_with_a_valid_validator(self):
        @self.paramValidatorTest(False)
        class _ObjectiveClass(self.ObjectiveClass):
            def __init__(self):
                pass

            def func(self, foo: bool, bar: str, eggs: int):
                return True
            
        _ObjectiveClass()._validate
        self.assertTrue(_ObjectiveClass().func(True, 'test', 100))

    def test_validade_the_objective_function_with_internal_funciton_with_params_and_validate_internal_params_with_a_valid_validator(self):
        @self.paramValidatorTest(False)
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

        self.assertEqual( func.foo, True)
        self.assertEqual( func.bar, 'test')
        self.assertEqual( func.eggs, 100)

    def test_validate_the_objective_function_by_calling_the_validator_directly(self):

        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.get_flask_app_sql().test_request_context():
            self.trueValidatorTest(_ObjectiveClass)

    def test_true_validate_the_objective_function_with_correct_HTTP_method_and_get_correct_result(self):
        
        @self.trueValidatorTest(methods_to_validate=['GET'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.get_flask_app_sql().test_request_context(method='GET'):
            _ObjectiveClass()._validate()

    def test_false_validate_the_objective_function_with_correct_HTTP_method_and_get_error(self):
        @self.falseValidatorTest(methods_to_validate=['GET'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.assertRaises(AuthMissingError) as exc_info:
            
            with self.get_flask_app_sql().test_request_context(method='GET'):
                _ObjectiveClass()._validate()
                self.assertIsInstance(exc_info, AuthMissingError)

    def test_true_validate_the_objective_function_with_wrong_HTTP_method_and_get_correct_result(self):
        
        @self.trueValidatorTest(methods_to_validate=['POST'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.get_flask_app_sql().test_request_context(method='GET'):
            _ObjectiveClass()._validate()

    def test_false_validate_the_objective_function_with_wrong_HTTP_method_and_get_error(self):
        @self.falseValidatorTest(methods_to_validate=['POST'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.get_flask_app_sql().test_request_context(method='GET'):
            _ObjectiveClass()._validate()
                
    def test_param_validate_the_objective_function_with_correct_http_method_and_false_shouldRaise(self):
        @self.paramValidatorTest(False, methods_to_validate=['GET'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.get_flask_app_sql().test_request_context(method='GET'):
            _ObjectiveClass()._validate()

    def test_param_validate_the_objective_function_with_correct_http_method_and_True_shouldRaise(self):
        @self.paramValidatorTest(True, methods_to_validate=['GET'])
        class _ObjectiveClass(self.ObjectiveClass):
            pass

        with self.assertRaises(AuthMissingError) as exc_info:
            with self.get_flask_app_sql().test_request_context(method='GET'):
                _ObjectiveClass()._validate()   
                self.assertIsInstance(exc_info, AuthMissingError)

    def test_decorate_function(self):
        @self.trueValidatorTest()
        def my_func():
            return True
        
        self.assertTrue(my_func())

    def test_decorate_function_with_false_validator_and_get_AuthMissingError(self):

        @self.falseValidatorTest()
        def my_func():
            return True
        
        with self.assertRaises(AuthMissingError) as exc_info:
            my_func()
            self.assertIsInstance(exc_info, AuthMissingError)

    def test_decorate_function_with_true_param_validator_and_get_AuthMissingError(self):

        @self.paramValidatorTest(True)
        def my_func():
            return True
        
        with self.assertRaises(AuthMissingError) as exc_info:
            my_func()
            self.assertIsInstance(exc_info, AuthMissingError)

    def test_decorate_method(self):
        class _Test:
            @self.trueValidatorTest()
            def my_func(self, a):
                return a
        
        self.assertEqual(_Test().my_func(100), 100)

    def test_decorate_method_with_false_validate_and_get_error(self):
        class _Test:
            @self.falseValidatorTest()
            def my_func(self):
                return True
        
        with self.assertRaises(AuthMissingError) as exc_info:
            _Test().my_func()
            self.assertIsInstance(exc_info, AuthMissingError)

    def test_true_validate_random_class(self):
        @self.trueValidatorTest()
        class RandomClass:
            def __new__(cls):
                return 100
            
        self.assertEqual(RandomClass(), 100)

    def test_false_validate_random_class_and_get_error(self):

        @self.falseValidatorTest()
        class RandomClass:
            def __new__(cls):
                return 100
            
        with self.assertRaises(AuthMissingError) as exc_info:
            self.assertNotEqual(RandomClass(), 100)
            self.assertIsInstance(exc_info, AuthMissingError)

    def test_true_validator_direct_call(self):
        class TestClass():
            pass

        self.assertTrue(self.trueValidatorTest(TestClass))

    def test_false_validator_direct_call(self):
        class TestClass():
            pass
        
        with self.assertRaises(AuthMissingError) as exc_info:
            self.falseValidatorTest(TestClass)

            self.assertIsInstance(exc_info, AuthMissingError)

    def test_false_param_validator_direct_call(self):
        class TestClass():
            pass
        
        self.assertTrue(self.paramValidatorTest(TestClass, False))

    def test_true_param_validator_direct_call(self):
        class TestClass():
            pass
        
        with self.assertRaises(AuthMissingError) as exc_info:
            self.paramValidatorTest(TestClass, True)
            self.assertIsInstance(exc_info, AuthMissingError)

    def test_mult_decorator_return_correct_function(self):

        @self.trueValidatorTest()
        @self.paramValidatorTest(False)
        def test():
            return "Hi"
        
        @self.paramValidatorTest(False)
        @self.trueValidatorTest()
        def test2():
            return "Hi"
        
        self.assertTrue(test(), 'Hi')
        self.assertTrue(test2(), 'Hi')

    def test_mult_decorator_with_validation_error_raises_exception(self):

        @self.trueValidatorTest()
        @self.paramValidatorTest(False)
        @self.falseValidatorTest()
        def test():
            return "Hi"
        
        @self.falseValidatorTest()
        @self.paramValidatorTest(False)
        @self.trueValidatorTest()
        def test2():
            return "Hi"
        
        @self.paramValidatorTest(True)
        @self.trueValidatorTest()
        def test3():
            return "Hi"
        
        with self.assertRaises(AuthMissingError) as exc_info1:
            test()
            self.assertIsInstance(exc_info1, AuthMissingError)
        
        with self.assertRaises(AuthMissingError) as exc_info2:
            test2() 
            self.assertIsInstance(exc_info2, AuthMissingError)

        with self.assertRaises(AuthMissingError) as exc_info3:
            test3() 
            self.assertIsInstance(exc_info3, AuthMissingError)