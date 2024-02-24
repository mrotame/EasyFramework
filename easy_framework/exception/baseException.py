import typing as t
from abc import ABC, abstractmethod


class BaseException(ABC, Exception):
    '''
    The base exception class for all exceptions that will be registered
    in the flask app.

    Define the `status_code` attribute to return the correct response status code
    Define the `message` to return the correct message (string, Json, etc...) to the user
    '''

    @property
    @abstractmethod
    def status_code(self) -> int:
        '''
        The HTTP resposne's status code that will be showed to the requester
        '''
        pass

    @property
    @abstractmethod
    def message(self) -> str | t.Dict[str, any]:
        '''
        The HTTP resposne's message that will be showed to the requester
        '''
        pass

    @classmethod
    def getExceptionFunction(self, e: BaseException):
        return self.dispatch_exception(e)

    def dispatch_exception(self) -> t.Tuple[str | t.Dict[str, any], int]:
        return self.message, self.status_code
