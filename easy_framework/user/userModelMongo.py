from mongoengine import fields
from flask import current_app

from .userMixin import UserMixin
from easy_framework.model import BaseModelMongo
from easy_framework._context import cache


class UserModelMongo(UserMixin, BaseModelMongo):
    meta = {"collection_name": "FLASK_EASY_FRAMEWORK_USER", "allow_inheritance": True}
    login = fields.StringField(required=True)
    password = fields.BinaryField(required=True)
    _owner_id = None

    @property
    def passwordManager(self):
        return cache.config.EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER()

    def save(self):
        self.password = self.passwordManager.hash(self.password)
        return super().save()
