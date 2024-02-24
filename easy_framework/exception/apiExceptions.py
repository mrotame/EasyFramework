import typing as t

from . import BaseException
from easy_framework._context import cache
from ..decorators import register_api_exception

@register_api_exception
class ValidationError(BaseException):
    message = None
    status_code = None

    def __init__(self, message: str | dict[str, any], status_code: int) -> None:
        self.message = message
        self.status_code = status_code


@register_api_exception
class AuthMissingError(BaseException):
    message: str = 'Authorization Header is Missing'
    status_code: int = 401


@register_api_exception
class InvalidSession(BaseException):
    message: str = 'Session token invalid or expired.'
    status_code: int = 401


@register_api_exception
class Unauthorized(BaseException):
    message: str = "User does not have permission"
    status_code: int = 401


@register_api_exception
class InvalidCredentials(BaseException):
    message: str = None
    status_code: int = 401

    def __init__(self, message: str | dict[str, any]) -> None:
        self.message = message


@register_api_exception
class NotTheOwner(BaseException):
    message: str = "User does not have permission"
    status_code: int = 401