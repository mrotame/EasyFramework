import typing as t
from datetime import timedelta
from pathlib import Path
import os
from flask import Flask

from .auth import AuthManager
from .auth import AuthView
from .database.sql import Sqldb
from .database.mongo import Mongodb
from .auth._authModel import AuthModel
from .user.userManager import UserManager
from .user.userModel import UserModel
from .auth import PasswordManager
from easy_framework._context import cache
from .view._viewHandler import ViewHandler


class EasyFramework():
    '''
    Easy framework.

    ### Description
    The easy framework has the objective of creating flask APIs easier.
    By managing a lot of things like databases, authentication, models, views, etc
    The user can achieve more, doing less.

    # Parameters
    * `flaskApp` The flask application client. Ex: 

    ```
    app = Flask(__name__)
    EasyFramework(app)
    ```
    '''

    exceptionList: t.List[BaseException] = cache.api_exception_list

    def __init__(self, flaskApp: Flask) -> None:
        self.app = flaskApp
        
        self.setupCache()
        self.setDefaultConfig()
        self.database_register()
        self.exceptions_register()
        self.authView_register()
        self.userManager_register()
        self.authManager_register()
        self.passwordManager_register()
        self.auto_import_view()

    def setupCache(self):
        cache.app = self.app
        cache.root_dir = Path(os.path.dirname(os.path.dirname(__file__)))

    def setDefaultConfig(self):
        # ----- EASY FRAMEWORK BASIC CONFIGS -----
        
        # ----- SQL DATABASE CONFIG -----
        self.app.config.setdefault('EASY_FRAMEWORK_DB_SQL_ACTIVATE', True)
        self.app.config.setdefault('EASY_FRAMEWORK_DB_SQL_DIALECT', 'sqlite')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_SQL_URI', '/')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_SQL_PORT', '')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_SQL_DBNAME', 'sqlite.db')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_SQL_USERNAME', '')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_SQL_PASSWORD', '')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_SQL_CREATE_ALL', False)

        # ----- MONGO DATABASE CONFIG -----
        self.app.config.setdefault('EASY_FRAMEWORK_DB_MONGO_ACTIVATE', False)
        self.app.config.setdefault('EASY_FRAMEWORK_DB_MONGO_URI', '127.0.0.1')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_MONGO_PORT', '27017')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_MONGO_DBNAME', 'test')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_MONGO_USERNAME', 'admin')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_MONGO_PASSWORD', 'admin')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_MONGO_AUTHMECHANISM', 'SCRAM-SHA-256')
        self.app.config.setdefault('EASY_FRAMEWORK_DB_MONGO_AUTHSOURCE', 'admin')

        # ----- AUTH MODULE CONFIG -----
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_VIEW', AuthView)
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_MANAGER', AuthManager)
        self.app.config.setdefault(
            'EASY_FRAMEWORK_AUTH_VIEW_AUTO_REGISTER', True) # Set this to false if you want EasyFramework to not manage the Auth system
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_METHOD', 'database_sql')
        self.app.config.setdefault(
            'EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION', timedelta(days=1))
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER', PasswordManager)
        self.app.config.setdefault('EASY_FRAMEWORK_AUTH_MODEL', AuthModel)
        
        # ----- USER CONFIG -----
        self.app.config.setdefault('EASY_FRAMEWORK_USER_MODEL', UserModel)
        self.app.config.setdefault('EASY_FRAMEWORK_USER_MANAGER', UserManager)

        # ---- VIEW CONFIG ----
        self.app.config.setdefault('EASY_FRAMEWORK_VIEW_FOLDER', 'view')
        self.app.config.setdefault('EASY_FRAMEWORK_VIEW_AUTO_IMPORT', False)
        self.app.config.setdefault("EASY_FRAMEWORK_VIEW_CLASS_NAME", "View")

    def authView_register(self):
        ''' 
        Register the Auth View if the config `EASY_FRAMEWORK_AUTH_VIEW_AUTO_REGISTER` is set to True
        '''
        if self.app.config.get('EASY_FRAMEWORK_AUTH_VIEW_AUTO_REGISTER') is True:
            view: AuthView = self.app.config.get('EASY_FRAMEWORK_AUTH_VIEW')
            for route in view.routes:
                self.app.add_url_rule(
                    route, view_func=view.as_view(view.name+'/'+route))

    def exceptions_register(self):
        ''' 
        Register the default exceptions to the flask app
        '''
        for exception in self.exceptionList:
            self.app.register_error_handler(
                exception, exception.getExceptionFunction)

    def userManager_register(self):
        ''' 
        Register the User manager specified in the config
        '''
        self.app.userManager = self.app.config['EASY_FRAMEWORK_USER_MANAGER'](
            self.app)

    def authManager_register(self):
        ''' 
        Register the Auth manager specified in the config
        '''
        self.app.authManager = self.app.config['EASY_FRAMEWORK_AUTH_MANAGER'](
            self.app)

    def passwordManager_register(self):
        ''' 
        Register the Password manager specified in the config
        '''
        self.app.passwordManager = self.app.config['EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER']()

    def database_register(self):
        ''' 
        Initializes and register the Sqldb in the config
        '''
        if self.app.config['EASY_FRAMEWORK_DB_SQL_ACTIVATE']:
            self.app.config['EASY_FRAMEWORK_DB_SQLDB'] = Sqldb(self.app)
        
        if self.app.config['EASY_FRAMEWORK_DB_MONGO_ACTIVATE']:
            self.app.config['EASY_FRAMEWORK_DB_MONGODB'] = Mongodb(self.app)

    def auto_import_view(self):
        if self.app.config['EASY_FRAMEWORK_VIEW_AUTO_IMPORT'] is True:
            
            view_folder = self.app.config['EASY_FRAMEWORK_VIEW_FOLDER']
            view_class_name = self.app.config['EASY_FRAMEWORK_VIEW_CLASS_NAME']

            ViewHandler.register_views(view_folder, self.app, view_class_name)