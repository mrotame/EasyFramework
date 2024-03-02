from flask import Flask

from ._databaseMethodSql import DatabaseMethodSql
from ._databaseMethodMongo import DatabaseMethodMongo
from ._baseAuthMethod import BaseAuthMethod

from easy_framework._context import cache


class AuthManager:
    def __init__(self, flaskApp: Flask):
        """
        The AuthManager is responsible for managing the Authorization across
        the App.

        ### Parameters
        `flaskApp` The main flask application

        ### Flask Config Parameters:
        `EASY_FRAMEWORK_AUTH_METHOD` This parameter is the name of the method that
        will be used to manage the Auth system. Right now, the framework only support
        the database method, but in the future we plan to support the dbless JWT system

        ### Adding more methods.
            To implement a new method, create a child class from this one, and create a new function inside it.
            This name of the function must start with `auth_method_`. Ex: `auth_method_custom`.
            The new method must return a instancied `BaseAuthMethod` child class.

            After, you need to replace the `EASY_FRAMEWORK_AUTH_MANAGER` parameter in the Flask App config to specify the new Auth Manager class
        """

        self.app = flaskApp

    @property
    def auth_method(self) -> BaseAuthMethod:
        self.string_method = cache.config.EASY_FRAMEWORK_AUTH_METHOD
        try:
            return getattr(self, "auth_method_" + self.string_method)()
        except AttributeError:
            raise AttributeError(
                'auth method not found. Try: "database" or "jwt"(not implementes yet). If you are creating one, the auth method function must my called: "auth_method_myMethod"'
            )

    def auth_method_database_sql(self):
        """
        Default Auth system with SQL-DB token storer method
        """
        return DatabaseMethodSql()

    def auth_method_database_mongo(self):
        """
        Default Auth system with Mongodb token storer method
        """
        return DatabaseMethodMongo()

    def auth_method_jwt(self):
        """
        Default Auth system with DBless method
        """
        raise NotImplementedError

    def loadUser(self):
        """
        Method that will call the function loadUser from the auth method being used.
        """
        self.auth_method.loadUser()
