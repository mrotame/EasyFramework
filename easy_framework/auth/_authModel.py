import typing as t
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from flask import current_app

from ..model import BaseModelSql
from easy_framework._context import cache


class AuthModel(BaseModelSql):
    """
    Authorization SQL Model.
    After login the user, here's where the session token is stored.
    """

    __tablename__ = "FLASK_EASY_FRAMEWORK_SESSION"
    token: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)
    user_id: orm.Mapped[int] = orm.mapped_column(nullable=False)
    expiration_date: orm.Mapped[t.Optional[datetime]] = orm.mapped_column(default=None)

    def save(self):
        """
        Before saving the token, we need to add the expiration date based on the `EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION` attribute in the Flask's app config
        """
        self.expiration_date = (
            datetime.now() + cache.config.EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION
        )
        return super().save()
