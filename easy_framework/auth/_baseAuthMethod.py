from abc import ABC, abstractmethod
import typing as t
from flask import current_app, request

from ..user.userManager import UserManager
from ..user.userModel import UserModel
from ..exception import AuthMissingError
from easy_framework._context import cache

if t.TYPE_CHECKING:
    from ..auth._authManager import AuthManager


class BaseAuthMethod(ABC):
    """
    Base abstract class for all the Authorization classes.
    The child from this class must be registered in the AuthManager child class
    The AuthManager child must be specified in the Flask config attribute
    """

    @property
    def token(self):
        """
        Attribute that store the token retrieved from the request's header
        Overwrite the `getTokenFromRequest` method if
        you want to retrieve the token from a different place, or
        in a different way
        """
        return self.getTokenFromRequest()

    @property
    def userModel(self) -> UserModel:
        """
        Get the default User Model where we will get the information after the token has been validated.
        """
        return cache.config.EASY_FRAMEWORK_USER_MODEL

    @property
    def authModel(self) -> UserModel:
        """
        Get the default Auth Model where we will set and get the user's session token
        """
        return cache.config.EASY_FRAMEWORK_AUTH_MODEL

    @property
    def authManager(self) -> "AuthManager":
        """
        Get the default Auth Manager.
        """
        return cache.config.EASY_FRAMEWORK_AUTH_MANAGER

    @abstractmethod
    def generateSession(self) -> str:
        """
        Abstract method that will generate/store
        the session token
        """
        return self.generateHashToken()

    @abstractmethod
    def generateHashToken(self) -> str:
        """
        abstract method that should create the hash token
        directly.
        """
        pass

    # The validateToken method should raise a registered error
    # such as ValidationError from easy_framework.exception
    # if the token is not valid, or return None if it is valid
    #
    # Overwrite the validateToken method and call super() if needed
    @abstractmethod
    def validateToken(self) -> None:
        """
        Abstract method that will validade the received token.
        It must return None if the token is valid, or raise
        and Flask registered error if the token is invalid
        """
        if self.token is None:
            raise AuthMissingError()

    @abstractmethod
    def getUserFromToken(self) -> str:
        """
        Abstract method that must retrieve and return the user's information after validating the token.
        """
        pass

    def getUserManager(self) -> UserManager:
        """
        Method that retrieves the UserManager class
        """
        return current_app.userManager

    def loadUser(self) -> None:
        """
        Main method that will return the user's information to
        the AuthManager's `load_user` method
        """

        self.getUserManager().load_user(self.getUserFromToken())

    def getTokenFromRequest(self) -> str:
        """
        Grab the token from the request.
        Overwrite this method if you want to retrieve
        the token from a different place, or
        in a different way
        """
        token = request.headers.get("Authorization")
        if token:
            if "bearer ".lower() in token.lower():
                token = token.split()[1]
            return token
