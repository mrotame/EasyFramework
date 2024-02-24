import secrets

from flask import request, current_app

from ._databaseMethodSql import DatabaseMethodSql
from ._authModelMongo import AuthModelMongo
from ..exception import ValidationError, InvalidCredentials
from easy_framework.user.userModelMongo import UserModelMongo

class DatabaseMethodMongo(DatabaseMethodSql):
    '''
    This class implements the Auth system using the default Mongo database system.
    '''

    def generateSession(self, user: UserModelMongo):
        '''
        Generates the session based on the user's information and save the token in the mongo database 
        in the Auth document
        '''
        token = self.generateHashToken()
        if user is None:
            raise InvalidCredentials('User not found or password is invalid')
        session = self.authModel(token=token, user_id=user.id)
        session.save()
        return token

    def getUserFromToken(self):
        '''
        Analyzes the Authorization token in the request headers and retreive the user linked to the session token
        '''
        if 'Authorization' in request.headers:
            token = self.token
            
            if 'Bearer '.lower() in token:
                token = token.split()[1]

            userModel = self.userModel
            token = self.authModel.get_one(token=token)
            if not token:
                return None

            user = userModel.get_one(id = token.user_id)

            return user
