import typing as t
from abc import ABC, abstractmethod
from typing import Dict, List, Literal

from flask import request
from flask.views import View as FlaskView
from marshmallow import ValidationError as MarshmallowValidationError
from werkzeug.datastructures import ImmutableMultiDict

from easy_framework.exception.apiExceptions import ValidationError
from easy_framework.serializer import BaseSerializerSql
from easy_framework.validator._baseValidator import BaseValidator
from easy_framework.user.utils import current_user
from easy_framework._meta import GenericApiViewMeta

from easy_framework.model._baseModelSql import BaseModelSql


class GenericApiView(ABC, FlaskView, metaclass=GenericApiViewMeta):
    """
    The GenericApiView is the class to go for the default CRUD basic view.
    It will link the Model, the Serializer and the Endpoint to automaticly manage
    the CRUD section for the selected model
    """

    field_lookup_method: t.Literal["path", "request"] = "request"
    """
    The place where the field_lookup should be.
    - `path` the path parameter in the url
    - `request` query string (for GET methods) or json (for all other methods)
    """

    @property
    @abstractmethod
    def routes(self) -> List[str]:
        """
        List of all url rules that should be registered
        at the flask app.
        """

    @property
    @abstractmethod
    def methods(self) -> List[str]:
        """
        The methods should keep the list of the allowed request methods
        for this view
        """
        pass

    @property
    @abstractmethod
    def model(self) -> BaseModelSql:
        """
        The model class related to this view
        """
        pass

    @property
    @abstractmethod
    def serializer(self) -> BaseSerializerSql:
        """
        The serializer class related to the model of this view
        """
        pass

    @property
    @abstractmethod
    def field_lookup(self) -> t.Union[str, t.Any]:
        """
        The field that should be looked at in both the request and the database
        (normaly the ID)
        """
        pass

    @property
    def validator_list(
        self,
    ) -> t.Union[List[BaseValidator], t.Dict[str, t.List[BaseValidator]]]:
        """
        ### List
        List of Validators for validate entire class instead
        of using as decorators for single functions. This validators will run for every HTTP method.

        ### Dict
        A dict containing a list of validators per http Method.

        Ex:
        {
            "get": [validator_1, validator_2],
            "post": [validator_x]
            "*": [validator_y, validator_z]
        }
        Notice that the validators in the `*` key will be included
        for all methods as well. So a `post` method will run validators validator_x, validator_y and validator_z
        """
        return []

    @property
    def auto_treat_request(self) -> bool:
        """
        If True, the entire View will use the default
        auto_{http_method} to manage the CRUD.

        Set this property to False if you want to use the common MethodView methods.
        """
        return True

    @property
    def validate_request(self) -> bool:
        """
        If True, the request will be validated according to the
        serializer.
        """
        return True

    def validations(self, *args, **kwargs):
        """
        This field should be overwritten to validate the data as needed
        than it should raises an flask registered exception in case
        the validation fails.
        """
        pass

    field_lookup_value: any = None
    """
    The field_lookup_value will be the value of the `field_lookup` in the
    request json. This field is filled automatically.
    Manually modifying it can cause bugs.
    """

    def auto_get(self, *args, **kwargs):
        """
        This method will search and return the found data (acording to the serializer and the lookup_field)

        Will be used intead of the get function if the
        auto_treat_request is set to True.
        """
        if self.field_lookup_value:
            return self.getSingleEntity()
        else:
            return self.getAllEntities()

    def auto_post(self, *args, **kwargs):
        """
        This method will insert the received data into the database (acording to the serializer and the lookup_field)

        Will be used intead of the get function if the
        auto_treat_request is set to True.
        """
        return self.createEntity()

    def auto_patch(self, *args, **kwargs):
        """
        This method will search the modify the received data (acording to the serializer and the lookup_field)

        Will be used intead of the get function if the
        auto_treat_request is set to True.
        """
        return self.updateEntity()

    def auto_delete(self, *args, **kwargs):
        """
        This method will search and delete the data (acording to the serializer and the lookup_field)

        Will be used intead of the get function if the
        auto_treat_request is set to True.
        """
        return self.deleteEntity("soft")

    def set_field_lookup_value(self) -> any:
        """
        Search the request for the lookup_field and keep it's value
        """
        if self.field_lookup_method == "request":
            self.field_lookup_value = request.args.get(self.field_lookup)

        elif self.field_lookup_method == "path":
            self.field_lookup_value = self.path_params.get(self.field_lookup)

    def __init__(self):
        self.serializer = self.serializer()
        if self.field_lookup_method == "request":
            self.set_field_lookup_value()

    def get_serializer(self) -> BaseSerializerSql:
        """
        Return the serializer function
        """
        return self.serializer

    def dispatch_request(self, *args: t.List, **kwargs: t.Dict):
        """
        Entry point for the View.
        It will look the request method, check if the auto_treat_request is set to True or not
        and return the correct method as response

        path params and query string params can both be accessed by
        self or by request

        ### Path params
        - `self.path_params`
        - `request.params`

        ### Query string params
        - `self.querystring_params`
        - `request.args`
        """
        self.path_params = kwargs
        self.querystring_params = request.args
        self.args = args

        request.params = ImmutableMultiDict(kwargs)

        if self.field_lookup_method == "path":
            self.set_field_lookup_value()

        self._validate(*args, **kwargs)

        method = request.method
        if self.auto_treat_request:
            method = "auto_" + method
        return getattr(self, str(method).lower())()

    def _validate(self, *args, **kwargs):

        if self.validate_request:
            self.validateRequest()

        if self.validator_list:
            self.validateValidators()

        self.validations()

    def getSingleEntity(self) -> Dict[str, any]:
        """
        It will return a single entity from the database (normaly the lookup_field_value is defined)
        """
        model = self.model.get_one(**{self.field_lookup: self.field_lookup_value})
        return self.get_serializer().dump(model)

    def getAllEntities(self) -> List[Dict[str, any]]:
        """
        It will return all entities from the database (normaly if there is no lookup_field in the request)
        """
        model: BaseModelSql = self.model()
        res = model.get_many()
        return self.get_serializer().dump(res, many=True)

    def getOwnedEntities(self) -> List[Dict[str, any]]:
        """
        It will return all entities owned by the user from the database (normaly if there is no lookup_field in the request)
        """
        model: BaseModelSql = self.model()
        res = model.get_many(_owner_id=current_user.id)
        return self.get_serializer().dump(res, many=True)

    def createEntity(self) -> Dict[str, any]:
        """
        Create a new entity using the received request schema, and save in the database
        """
        json_data = request.get_json()
        try:
            serialized_data = self.get_serializer().load(json_data)
        except MarshmallowValidationError as e:
            return e.messages, 422
        model: BaseModelSql = self.model(**serialized_data)
        model.save()

        return self.get_serializer().dump(model), 201

    def updateEntity(self, **kwargs) -> Dict[str, any]:
        """
        find the entity by using the field_lookup, and update it's data
        """
        json_data = request.get_json()
        try:
            serialized_data = self.get_serializer().load(json_data)
        except MarshmallowValidationError as e:
            return e.messages, 422

        model: BaseModelSql = self.model().get_one(
            **{self.field_lookup: self.field_lookup_value}
        )

        for item in serialized_data:
            if hasattr(model, item):
                setattr(model, item, serialized_data[item])

        model.update()
        return self.get_serializer().dump(model), 204

    def deleteEntity(
        self, deleteMethod: Literal["soft", "hard"], *args, **kwargs
    ) -> Dict[str, any]:
        """
        find the entity by using the field_lookup, and delete it

        ## Parameters
        * `deleteMethod` The delete method parameter can be 'soft' or 'hard'.
        If hard, it will be deleted permanently from the database
        If soft, it will the `delete` field will be set to True. It will not be delete from the Database
        but it will not be showing in the requests anymore.
        """
        model: BaseModelSql = self.model.get_one(
            **{self.field_lookup: self.field_lookup_value}
        )
        if not model:
            return "impossible delete: entity not found", 404
        if deleteMethod == "hard":
            return model.delete(deleteMethod)

        model._deleted = True
        model.update()
        return "", 204

    def validateRequest(self):
        """
        validate the request according to the serializer
        """
        if request.method in ["GET", "DELETE"]:
            return {}
        try:
            return self.get_serializer().load(request.get_json())
        except MarshmallowValidationError as e:
            raise ValidationError(e.messages, 422)

    def validateValidators(self):
        """
        Class that runs all validators in self `validator_list` attribute
        """

        def run_validator(validator: BaseValidator):
            validator = validator(self)

        if isinstance(self.validator_list, list):
            for validator in self.validator_list:
                run_validator(validator)
        elif isinstance(self.validator_list, dict):
            self.validator_list = {k.lower(): v for k, v in self.validator_list.items()}
            for validator in [
                *[i for i in self.validator_list.get("*", [])],
                *[i for i in self.validator_list.get(request.method.lower(), [])],
            ]:
                run_validator(validator)
