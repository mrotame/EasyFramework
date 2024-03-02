import typing as t
from pathlib import Path
import os
from flask import Flask

from .database.sql import Base
from .database.sql import Sqldb
from .database.mongo import Mongodb
from .view._viewHandler import ViewHandler
from .config import Config
from easy_framework._context import cache


class EasyFramework:
    """
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
    """

    exceptionList: t.List[BaseException] = cache.api_exception_list
    run_server: t.Callable
    config = Config()

    def __init__(self, flaskApp: Flask) -> None:
        self.app = flaskApp

        self.run_server = self.app.run
        self.app.run = self._before_run_server
        self.setupCache()

    def _before_run_server(self, *args, **kwargs):
        self.run_all_configs()
        self.run_server(*args, **kwargs)

    def run_all_configs(self):
        self.database_register()
        self.database_create_all()
        self.exceptions_register()
        self.authView_register()
        self.userManager_register()
        self.authManager_register()
        self.passwordManager_register()
        self.auto_import_view()

    def setupCache(self):
        cache.app = self.app
        cache.root_dir = Path(os.path.dirname(os.path.dirname(__file__)))

        cache.config = self.config

    def authView_register(self):
        """
        Register the Auth View if the config `EASY_FRAMEWORK_AUTH_VIEW_AUTO_REGISTER` is set to True
        """
        if self.config.EASY_FRAMEWORK_AUTH_VIEW_AUTO_REGISTER is True:
            view = self.config.EASY_FRAMEWORK_AUTH_VIEW
            for route in view.routes:
                self.app.add_url_rule(
                    route, view_func=view.as_view(view.name + "/" + route)
                )

    def exceptions_register(self):
        """
        Register the default exceptions to the flask app
        """
        for exception in self.exceptionList:
            self.app.register_error_handler(exception, exception.getExceptionFunction)

    def userManager_register(self):
        """
        Register the User manager specified in the config
        """
        self.app.userManager = self.config.EASY_FRAMEWORK_USER_MANAGER(self.app)

    def authManager_register(self):
        """
        Register the Auth manager specified in the config
        """
        self.app.authManager = self.config.EASY_FRAMEWORK_AUTH_MANAGER(self.app)

    def passwordManager_register(self):
        """
        Register the Password manager specified in the config
        """
        self.app.passwordManager = self.config.EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER()

    def database_register(self):
        """
        Initializes and register the Sqldb in the config
        """
        if self.config.EASY_FRAMEWORK_DB_SQL_ACTIVATE:
            self.config.EASY_FRAMEWORK_DB_SQLDB = Sqldb(self.app)

        if self.config.EASY_FRAMEWORK_DB_MONGO_ACTIVATE:
            self.config.EASY_FRAMEWORK_DB_MONGODB = Mongodb()

    def database_create_all(self):
        env: str = self.config.EASY_FRAMEWORK_ENVIRONMENT
        if getattr(self.config, f"EASY_FRAMEWORK_DB_{env.upper()}_SQL_CREATE_ALL"):
            database: Sqldb = self.config.EASY_FRAMEWORK_DB_SQLDB
            Base.metadata.create_all(database.dbConfig.engine)

    def auto_import_view(self):
        if self.config.EASY_FRAMEWORK_VIEW_AUTO_IMPORT is True:

            view_folder = self.config.EASY_FRAMEWORK_VIEW_FOLDER
            view_class_name = self.config.EASY_FRAMEWORK_VIEW_CLASS_NAME

            ViewHandler.register_views(view_folder, self.app, view_class_name)
