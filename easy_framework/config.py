import typing as t
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from easy_framework.auth import AuthManager
from easy_framework.auth import AuthView
from easy_framework.database.sql import Sqldb
from easy_framework.database.mongo import Mongodb
from easy_framework.auth._authModel import AuthModel
from easy_framework.user.userManager import UserManager
from easy_framework.user.userModel import UserModel
from easy_framework.auth import PasswordManager


@dataclass
class Config:
    # ----- EASY FRAMEWORK BASIC CONFIGS -----
    EASY_FRAMEWORK_ENVIRONMENT: t.Optional[str] = "dev"

    # ----- SQL DATABASE CONFIG -----
    EASY_FRAMEWORK_DB_SQL_ACTIVATE: t.Optional[bool] = True
    EASY_FRAMEWORK_DB_SQLDB: Sqldb = field(init=False)

    # Production Database
    EASY_FRAMEWORK_DB_PROD_SQL_DIALECT: t.Optional[str] = "sqlite"
    EASY_FRAMEWORK_DB_PROD_SQL_URI: t.Optional[str] = "/"
    EASY_FRAMEWORK_DB_PROD_SQL_PORT: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_PROD_SQL_DBNAME: t.Optional[str] = "prod_sqlite.db"
    EASY_FRAMEWORK_DB_PROD_SQL_USERNAME: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_PROD_SQL_PASSWORD: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_PROD_SQL_CREATE_ALL: t.Optional[str] = False

    # Development Database
    EASY_FRAMEWORK_DB_DEV_SQL_DIALECT: t.Optional[str] = "sqlite"
    EASY_FRAMEWORK_DB_DEV_SQL_URI: t.Optional[str] = "/"
    EASY_FRAMEWORK_DB_DEV_SQL_PORT: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_DEV_SQL_DBNAME: t.Optional[str] = "dev_sqlite.db"
    EASY_FRAMEWORK_DB_DEV_SQL_USERNAME: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_DEV_SQL_PASSWORD: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_DEV_SQL_CREATE_ALL: t.Optional[str] = False

    # Test database
    EASY_FRAMEWORK_DB_TEST_SQL_DIALECT: t.Optional[str] = "sqlite"
    EASY_FRAMEWORK_DB_TEST_SQL_URI: t.Optional[str] = "/"
    EASY_FRAMEWORK_DB_TEST_SQL_PORT: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_TEST_SQL_DBNAME: t.Optional[str] = "TEST_sqlite.db"
    EASY_FRAMEWORK_DB_TEST_SQL_USERNAME: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_TEST_SQL_PASSWORD: t.Optional[str] = ""
    EASY_FRAMEWORK_DB_TEST_SQL_CREATE_ALL: t.Optional[str] = False

    # ----- MONGO DATABASE CONFIG -----
    EASY_FRAMEWORK_DB_MONGO_ACTIVATE: t.Optional[str] = False
    EASY_FRAMEWORK_DB_MONGODB: Mongodb = field(init=False)

    EASY_FRAMEWORK_DB_MONGO_URI: t.Optional[str] = "127.0.0.1"
    EASY_FRAMEWORK_DB_MONGO_PORT: t.Optional[str] = "27017"
    EASY_FRAMEWORK_DB_MONGO_DBNAME: t.Optional[str] = "test"
    EASY_FRAMEWORK_DB_MONGO_USERNAME: t.Optional[str] = "admin"
    EASY_FRAMEWORK_DB_MONGO_PASSWORD: t.Optional[str] = "admin"
    EASY_FRAMEWORK_DB_MONGO_AUTHMECHANISM: t.Optional[str] = "SCRAM-SHA-256"
    EASY_FRAMEWORK_DB_MONGO_AUTHSOURCE: t.Optional[str] = "admin"

    # ----- AUTH MODULE CONFIG -----
    EASY_FRAMEWORK_AUTH_VIEW: t.Optional[AuthView] = AuthView
    EASY_FRAMEWORK_AUTH_MANAGER: t.Optional[AuthManager] = AuthManager
    EASY_FRAMEWORK_AUTH_VIEW_AUTO_REGISTER: t.Optional[bool] = True
    EASY_FRAMEWORK_AUTH_METHOD: t.Optional[str] = "database_sql"
    EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION: t.Optional[datetime] = timedelta(days=1)
    EASY_FRAMEWORK_AUTH_PASSWORD_MANAGER: t.Optional[PasswordManager] = PasswordManager
    EASY_FRAMEWORK_AUTH_MODEL: t.Optional[AuthModel] = AuthModel

    # ----- USER CONFIG -----
    EASY_FRAMEWORK_USER_MODEL: t.Optional[UserModel] = UserModel
    EASY_FRAMEWORK_USER_MANAGER: t.Optional[UserManager] = UserManager

    # ---- VIEW CONFIG ----
    EASY_FRAMEWORK_VIEW_FOLDER: t.Optional[str] = "views"
    EASY_FRAMEWORK_VIEW_AUTO_IMPORT: t.Optional[bool] = False
    EASY_FRAMEWORK_VIEW_CLASS_NAME: t.Optional[str] = "View"
