from abc import ABC, abstractmethod
import types
from flask import request
from marshmallow import Schema, fields

from easy_framework.model import BaseModelSql


class BaseSerializerSql(Schema):
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
