from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from easy_framework.model import BaseModelSql
from .userMixin import UserMixin
from flask import current_app


class UserModel(BaseModelSql, UserMixin):
    __tablename__ = 'FLASK_EASY_FRAMEWORK_USER'
    
    login: orm.Mapped[str]  = orm.mapped_column(sa.String(60), unique=True)
    password: orm.Mapped[str] = orm.mapped_column(sa.String(255))

    @property
    def passwordManager(self):
        return current_app.config.get('EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER')()

    def save(self):
        self.password = self.passwordManager.hash(self.password).decode()
        return super().save()
