import secrets

from flask import request, g

from ._baseAuthMethod import BaseAuthMethod
from ._authModel import AuthModel
from ..exception import ValidationError, InvalidCredentials
from easy_framework.user.userModel import UserModel

class DatabaseMethodSql(BaseAuthMethod):
    '''
    This class implements the Auth system using the default SQL database system.
    '''

    token_len = 256
    def generateSession(self, user: UserModel):
        '''
        Generates the session based on the user's information and save the token in the sql database 
        in the Auth table
        '''
        token = self.generateHashToken()
        if user is None:
            raise InvalidCredentials('User not found or password is invalid')
        session = self.authModel(token=token, user_id=user.id)
        session.save()
        return token

    def generateHashToken(self):
        '''
        Generates the hash token
        '''
        return secrets.token_hex(int(self.token_len/2))

    def getUserFromToken(self):
        '''
        Analyzes the Authorization token in the request headers and retreive the user linked to the session token
        '''
        
        if 'Authorization' in request.headers:
            
            token = self.token

            if 'Bearer '.lower() in self.token:
                token = token.split()[1]
            
            userModel = self.userModel
            user = userModel.get_one(self.authModel.token==token, userModel.id == self.authModel.user_id)
            
            return user

    def validateToken(self):
        '''
        Validate the token to check if it's valid.
        This function checks if the token exists, and if it is a string. 
        '''
        super().validateToken()
        if not isinstance(self.token, str):
            raise ValidationError('Invalid token type. Token is not a string', 498)
        if len(self.token) != self.token_len:
            raise ValidationError('Invalid token length', 498)