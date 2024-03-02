import typing as t

from . import BaseException
from ..decorators import register_api_exception


@register_api_exception
class ValidationError(BaseException):
    message = None
    status_code = None

    def __init__(self, message: dict[str, t.Any], status_code: int) -> None:
        self.message = message
        self.status_code = status_code


@register_api_exception
class AuthMissingError(BaseException):
    message: t.Dict[str, t.Any] = {"msg": "Authorization Header is Missing"}
    status_code: int = 401


@register_api_exception
class InvalidSession(BaseException):
    message: t.Dict[str, t.Any] = {"msg": "Session token invalid or expired."}
    status_code: int = 401


@register_api_exception
class Unauthorized(BaseException):
    message: t.Dict[str, t.Any] = {"msg": "User does not have permission"}
    status_code: int = 401


@register_api_exception
class InvalidCredentials(BaseException):
    message: t.Dict[str, t.Any] = {"msg": "Error. Invalid credentials."}
    status_code: int = 401

    def __init__(self, message: t.Dict[str, t.Any] | dict[str, any] = None) -> None:
        if message:
            self.message = message


@register_api_exception
class NotTheOwner(BaseException):
    message: t.Dict[str, t.Any] = {"msg": "User does not have permission"}
    status_code: int = 401
