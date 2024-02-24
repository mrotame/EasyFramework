from ..model import BaseModelSql
import sqlalchemy as sa
from flask import current_app
from datetime import datetime

class AuthModel(BaseModelSql):
    '''
    Authorization SQL Model.
    After login the user, here's where the session token is stored.
    '''
    __tablename__ = 'FLASK_EASY_FRAMEWORK_SESSION'
    token = sa.Column(sa.String(256), nullable=False)
    user_id = sa.Column(sa.Integer, nullable=False)
    expiration_date = sa.Column(sa.DateTime, nullable=False)

    def save(self):
        '''
        Before saving the token, we need to add the expiration date based on the `EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION` attribute in the Flask's app config
        '''
        self.expiration_date=datetime.now()+current_app.config.get('EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION')
        return super().save()