from flask import current_app

from easy_framework.serializer import BaseSerializerSql, fields
from easy_framework.auth._password import PasswordManager
from easy_framework._context import cache


class AuthSerializer(BaseSerializerSql):
    """
    Default Marshmellow's serializer for the Auth Model and View.
    Used for login only. Not for retrieve the session token
    """

    @property
    def getPasswordManager(self) -> PasswordManager:
        """
        Attribute that returns the PasswordManager responsible
        for checking and validating the passwords, case necessary
        """
        return cache.config.EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER()

    class Meta:
        """
        Meta for all HTTP methods (except Post).
        Password is not required in this case
        """

        login = fields.Str()
        password = fields.Str(load_only=True)

    class PostMeta(Meta):
        """
        Meta for post HTTP method (login method).
        Password is required in this case
        """

        login = fields.Str(required=True)
        password = fields.Str(required=True, load_only=True)
