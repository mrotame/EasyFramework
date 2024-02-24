from __future__ import annotations
import typing as t
import inspect
from abc import ABC, abstractmethod
import functools

from easy_framework._meta import GenericApiViewMeta

if t.TYPE_CHECKING:
    from easy_framework.view import GenericApiView

class BaseValidator(ABC):
    '''
    Base validator class, that needs to be inherited by all
    validator decorators.

    All validators must be used as decorators for the classes or viewtions you want to validate
    You can decorate the entire class if you want everything from it to be protected, or
    decorate a single method of a class if you want only some viewtionality or some http
    method to be protected (user can GET, but not POST to an endpoint for example)
    '''

    def __init__(self, *args, **kwargs) -> None:
        '''
        BaseValidator init. When overwriting this, always call super init passing the received parameters.

        # Usage
        - Validators can be used as decorators decorating functions, methods or entire classes

            ```
            @MyValidator(optionalArg1, optionalArg2=False)
            class MyClass:

                @MySecondValidator()
                def my_func_33():
                    ...
            ```
        - Validators can be used by direct call

            ```
            MyValidator(myFunc, optionalArg1, optionalArg2=True)
            ```
        
        - Validators also detect when the decorated/validated object
        is a GenericApiView instance, and auto-register the validator
        in the `validator_list` param letting the View to handle the
        validation process

        # Parameters

        - `view` - required when using direct call instead of decorator.
        If using the validator as decorator, ignore this parameter

        - `methods_to_validate` - is a list of HTTP methods which the validator should validate
        By default, POST is out of the list due to the data not existing yet.
        '''  
        
        lines = inspect.stack(context=2)[1].code_context
        decorated = any(line.strip().startswith('@') for line in lines)
        
        if decorated:
            self._run_as_decorator(*args, **kwargs)
        else:
            self._run_as_direct_call(*args, **kwargs)

    def _run_as_direct_call(self, *args, **kwargs):
        args = list(args)
        self.view = args.pop(0)
        self.validate(*args, **kwargs)

    def _run_as_decorator(self, *args, **kwargs):    
        self.methods_to_validate = kwargs.get('methods_to_validate', '*')
        
        kwargs.pop('methods_to_validate') if 'methods_to_validate' in kwargs else kwargs

        self.args = args
        self.kwargs = kwargs

    def __call__(self, view):
        '''
        Validator main logic. Here is where the decorator will be called
        Validator can decorates Easy Framework View classes, methods or functions.

        If we're decorating Easy Framework View classes, than we insert the validator as part of the `validator_list` attribute so the generic api view can handle the validation and return the view

        If we are decorating methods, functions or other classes, than we return the wrapper. The wrapper validates, execute the method / function and return the result
        
        '''
        
        self.view: GenericApiView = view
        
        def wrapper(*args, **kwargs):
            self.validate(*self.args, **self.kwargs)
            return self.view(*args, **kwargs)
            
        
        if isinstance(self.view, GenericApiViewMeta):
            self.register_validator_in_view()
            return self.view
        return wrapper

    @abstractmethod
    def validate(self, *args, **kwargs) -> None:
        '''
        Decorator init. logic will happend here. Make sure to raise a 
        flask registered error if the validation fails. 
        Only the raises are caught by the decorator. All returns will be ignored
        '''
        pass

    def view_is_instancied(self):
        if isinstance(self.view, type):
            return False
        return True
    
    def register_validator_in_view(self):
        if not hasattr(self.view, 'validator_list'):
            self.view.validator_list = {}

        if isinstance(self.view.validator_list, list):
            self.view.validator_list = {'*':self.view.validator_list}

        if isinstance(self.view.validator_list, property):
            self.view.validator_list = {}
        
        if self.methods_to_validate == '*':
            if '*' in self.view.validator_list:
                if not isinstance(self.view.validator_list, list):
                    self.view.validator_list['*'] = [self.view.validator_list['*']]
            else:
                self.view.validator_list['*'] = []

            self.view.validator_list['*'].append(functools.partial(lambda view: self.__class__(view, *self.args, **self.kwargs)))
            return
        
        if isinstance(self.methods_to_validate, list):
            for method in self.methods_to_validate:
                if method in self.view.validator_list:
                    if not isinstance(method, list):
                        self.view.validator_list[method] = [self.view.validator_list[method]]
                else:
                    self.view.validator_list[method] = []
                
                self.view.validator_list[method].append(functools.partial(lambda view: self.__class__(view, *self.args, **self.kwargs)))