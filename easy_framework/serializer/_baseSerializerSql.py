from abc import abstractmethod
import types
from flask import request
from marshmallow import Schema, fields



class BaseSerializerSql(Schema):
    '''
    Base serializer class for SQL Models.

    This serializer use the marshmallow library
    to validate the data and convert it to a
    SQL Model class. You can combine one to many meta
    classes.

    ### Properties
    - class Meta():
        "
        The default meta class that works for all 
        request methods. Any marshmallow field declared here
        will be use regardless of the request method.
        "
    - classes GetMeta() | PutMeta() | DeleteMeta()...
        "
        for each other Meta class defined in the 
        serializer class, it will work for its respective 
        request method. Specific methods classes does support
        all existent HTTP request methods
        EG. GetMeta will run only for GET request
        "
    '''

    @abstractmethod
    def Meta():
        class Meta:
            pass
        return Meta

    class MainMeta():
        id = fields.Integer(dump_only=True)
        created_at = fields.DateTime(dump_only=True)
        updated_at = fields.DateTime(dump_only=True)
        deleted = fields.Integer(dump_only=True)

    def __new__(cls, *args, **kwargs):
        cls = cls.selectMeta(cls)
        return super().__new__(cls, *args, **kwargs)

    def selectMeta(cls):
        look_for = request.method.capitalize()+'Meta'
        try:
            requestedMeta = getattr(cls,look_for)
            return types.new_class(str(cls.__name__), (cls, cls.MainMeta, requestedMeta), dict())
        except AttributeError:
            return types.new_class(str(cls.__name__), (cls, cls.MainMeta, cls.Meta), dict())
