import typing as t
from datetime import datetime

from flask import Flask
import sqlalchemy as sa
from sqlalchemy import orm
import marshmallow as mar
import mongoengine as mon


from easy_framework.user.userMixin import UserMixin
from easy_framework.user.utils import current_user
from easy_framework.model import BaseModelSql
from easy_framework.serializer import BaseSerializerSql
from easy_framework.model import BaseModelMongo
from easy_framework.serializer import BaseSerializerMongo
from easy_framework.user import UserModelMongo
from easy_framework.user import UserModel

class UserTestSql:
    flaskApp: Flask
    user: UserModel
    token: str
    def __init__(self, flaskApp: Flask, login: str, password: str):
        self.flaskApp = flaskApp
        self.user = self.create_user(flaskApp, login, password)
        self.token = self.login_user(flaskApp, login, password)

    def create_user(self, flaskApp: Flask, login: str, password: str)-> UserModel:
        with flaskApp.app_context():
            user = UserModel(login=login, password=password).save()
        return user

    def login_user(self, flaskApp: Flask, login:str, password:str)-> str:
        res = flaskApp.test_client().post('/auth',json={'login':login,'password':password})
        return res.get_json()['auth_token']


class UserTestMongo:
    flaskApp: Flask
    user: UserModelMongo
    token: str
    def __init__(self, flaskApp: Flask, login: str, password: str):
        self.flaskApp = flaskApp
        self.user = self.create_user(flaskApp, login, password)
        self.token = self.login_user(flaskApp, login, password)

    def create_user(self, flaskApp: Flask, login: str, password: str)-> UserModel:
        with flaskApp.app_context():
            user = UserModelMongo(login=login, password=password).save()
        return user

    def login_user(self, flaskApp: Flask, login:str, password:str)-> str:
        res = flaskApp.test_client().post('/auth',json={'login':login,'password':password})
        return res.get_json()['auth_token']
    

class ModelTestSql(BaseModelSql):
    __tablename__ = 'TestModelSql'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, default=None)
    _owner_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(nullable=True, insert_default=lambda: current_user.id if isinstance(current_user, UserMixin) else None, default=None)
    username: orm.Mapped[t.Optional[str]] = orm.mapped_column(default=None)
    password: orm.Mapped[t.Optional[str]] = orm.mapped_column(default=None)
    test_datetime: orm.Mapped[datetime] = orm.mapped_column(default=datetime.now())
    age: orm.Mapped[t.Optional[int]] = orm.mapped_column(default=None)
    name: orm.Mapped[t.Optional[str]] = orm.mapped_column(default=None)
    info: orm.Mapped[t.Optional[str]] = orm.mapped_column(default=None)
    desc: orm.Mapped[t.Optional[str]] = orm.mapped_column(default=None)


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
    __tablename__ = 'TestModelMongo'
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