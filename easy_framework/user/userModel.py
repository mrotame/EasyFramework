from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm
from flask import current_app

from easy_framework.model import BaseModelSql
from easy_framework._context import cache
from .userMixin import UserMixin


class UserModel(BaseModelSql, UserMixin):
    __tablename__ = "FLASK_EASY_FRAMEWORK_USER"

    login: orm.Mapped[str] = orm.mapped_column(sa.String(60), unique=True)
    password: orm.Mapped[str] = orm.mapped_column(sa.String(255))

    @property
    def passwordManager(self):
        return cache.config.EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER()

    def save(self):
        self.password = self.passwordManager.hash(self.password).decode()
        return super().save()
