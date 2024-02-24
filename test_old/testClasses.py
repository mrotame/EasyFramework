from datetime import datetime

import sqlalchemy as sa
import marshmallow as mar

import mongoengine as mon

from easy_framework.model import BaseModelSql
from easy_framework.serializer import BaseSerializerSql
from easy_framework.model import BaseModelMongo
from easy_framework.serializer import BaseSerializerMongo

class ModelTestSql(BaseModelSql):
    __tablename__ = 'TestModel'
    username = sa.Column(sa.String)
    password = sa.Column(sa.String)
    test_datetime = sa.Column(sa.DateTime, default=datetime.now())
    age = sa.Column(sa.Integer)
    name = sa.Column(sa.String)
    info = sa.Column(sa.String)
    desc = sa.Column(sa.String)

class SerializerTestSql(BaseSerializerSql):
    class Meta:
        username = mar.fields.String()
        password = mar.fields.String(load_only=True)
        age = mar.fields.Integer()
        name = mar.fields.String()
        desc = mar.fields.String()

    class PostMeta(Meta):
        username = mar.fields.String(required=True)
        password = mar.fields.String(required=True, load_only=True)
        name = mar.fields.String()
        desc = mar.fields.String()

class ModelTestMongo(BaseModelMongo):
    username = mon.fields.StringField()
    password = mon.fields.StringField()
    name = mon.fields.StringField()
    desc = mon.fields.StringField()

class SerializerTestMongo(BaseSerializerMongo, SerializerTestSql):
    pass

class SerializerValidatorSql(BaseSerializerSql):
    class Meta():
        validate_1 = mar.fields.Boolean()
        validate_2 = mar.fields.Boolean()


