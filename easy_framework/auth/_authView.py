from flask import current_app, request
import typing as t
from easy_framework.view import GenericApiView

from ..user import UserModel
from . import AuthManager
from . import AuthModel
from . import AuthSerializer
from ..exception import InvalidCredentials

if t.TYPE_CHECKING:
    from . import PasswordManager


class AuthView(GenericApiView):
    '''
    Default view responsible for login the user.
    Replace this default view by changing the attribute
    `FLASK_EASY_FRAMWORK_AUTH_DEFAULT_VIEW` in the Flask's app config, and passing a default GenericApiView child
    '''

    field_lookup = None
    serializer: AuthSerializer = AuthSerializer
    model = AuthModel
    methods=['POST']
    routes=['/auth']
    name='FLASK_EASY_FRAMWORK_AUTH_DEFAULT_VIEW'
    auto_treat_request=False

    def post(self):
        '''
        The user login process by using the Post HTTP method
        '''
        serialized_data = self.get_serializer().load(request.get_json())
        userModel: UserModel = current_app.config.get('EASY_FRAMEWORK_USER_MODEL')
        user: UserModel = userModel.get_one(**{'login': serialized_data['login']})
        passwordManager = self.serializer.getPasswordManager
        
        if user is None or passwordManager.compare(serialized_data['password'], user.password) is not True:
            raise InvalidCredentials('Invalid login or password')

        token = current_app.authManager.auth_method.generateSession(user)
        return {'auth_token': token}, 200
