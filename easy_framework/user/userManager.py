import typing as t

from flask import Flask, g

from .userMixin import AnonymousUser
from .userModel import UserModel
from .utils import current_user

from easy_framework._context import cache


class UserManager:
    """
    Class responsible for managing and retrieving the users.

    ### Parameters
    * `flaskApp` Flask application client.
    """

    def __init__(self, flaskApp: Flask) -> None:
        self.app = flaskApp

    @property
    def user_model(self) -> UserModel:
        """
        Property that returns the user model defined in the flask app config
        """
        return cache.config.EASY_FRAMEWORK_USER_MODEL

    @property
    @classmethod
    def user(self):
        """
        Return the current_user that must be a user or an AnonymousUser
        """
        return current_user

    def load_user(self, user) -> None:
        """
        Loads the user into flask.g attribute
        """
        if user is not None:
            g.user = user
        else:
            g.user = AnonymousUser()
