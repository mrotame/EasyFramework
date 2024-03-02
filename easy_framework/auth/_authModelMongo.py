from ..model import BaseModelMongo
from mongoengine import fields
from flask import current_app
from datetime import datetime

from easy_framework._context import cache


class AuthModelMongo(BaseModelMongo):
    """
    Authorization Mongo Model.
    After login the user, here's where the session token is stored.
    """

    collection_name = "FLASK_EASY_FRAMEWORK_SESSION"
    meta = {"collection": collection_name}
    token = fields.StringField(required=True)
    user_id = fields.ObjectIdField(required=True)
    expiration_date = fields.DateTimeField(required=False)

    def save(self):
        """
        Before saving the token, we need to add the expiration date based on the `EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION` attribute in the Flask's app config
        """
        self.expiration_date = (
            datetime.now() + cache.config.EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION
        )
        return super().save()
