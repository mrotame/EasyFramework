from __future__ import annotations
import typing as t
from abc import ABC, abstractmethod

import bson

from easy_framework.user.utils import current_user
from easy_framework.user.userMixin import UserMixin
from mongoengine import Document
from mongoengine import fields


class BaseModelMongo(Document):
    meta = {"abstract": True}

    id: bson.ObjectId
    _deleted = fields.BooleanField(required=True, default=False)
    _owner_id = fields.DynamicField(default=lambda: current_user.id if isinstance(current_user, UserMixin) else "")

    @classmethod
    def get_one(cls, *args, **kwargs)-> t.Self:
        if args:
            res: t.Self = cls.objects(*args, **{"_deleted":False}).first()
        else: 
            res: t.Self = cls.objects(**{**kwargs, '_deleted':False}).first()
        return res
    
    @classmethod
    def get_many(cls: t.Type[t.Self], *args, **kwargs)-> t.List[t.Self]:
        return cls.objects(*args, **{**kwargs, '_deleted':False})
    
    def update(self)-> t.Self:
        self.save()

    def save(self, *args, **kwargs)-> t.Self:
        return super().save(*args, **kwargs)

    def delete(self, method='soft'):
        if method == 'hard':
            self.hard_delete_procedure()
        else:
            self.soft_delete_procedure()
        return self
    
    def hard_delete_procedure(self):
        super().delete()

    def soft_delete_procedure(self):
        self._deleted = True
        self.update()

