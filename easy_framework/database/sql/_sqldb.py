from flask import Flask
from flask import current_app
from sqlalchemy.orm import Session

from ._dbConfig import DbConfig
from easy_framework._context import cache


class SessionFactory:
    """
    Session factory to be used within `with` scope
    """

    def __init__(self, cls: "Sqldb"):
        self.cls = cls

    def __enter__(self):
        return self.cls.getNewSession()

    def __exit__(self, exception_type, exception_value, traceback):
        self.cls.closeSession()


class Sqldb:
    """
    Main Database class that will be used to access the database.

    ### Parameters
    `flaskApp` Optional parameter (if empty, the current_app will be used) containing
    the flask application client that contains all the parameters that need to be passed
    to the database configuration class.

    ### Overwriting
    If you want to change any configuration, the connection method or anithing else,
    you can inherit and overwrite most of this class attributes and methods.
    Also, give it a look at the DbConfig class
    """

    dbConfigClass = (
        DbConfig  # the class responsible for configurating the db connection
    )
    dbSession: Session = None

    def __init__(self, flaskApp: Flask = None) -> None:
        if not flaskApp:
            flaskApp = current_app
        self.app = flaskApp
        self.dbConfig = self.getDbConfig()

    def getDbConfig(self) -> DbConfig:
        """
        get the database config class by passing all the configs defined
        in the flask app config attribute
        """
        env: str = cache.config.EASY_FRAMEWORK_ENVIRONMENT.upper()

        return self.dbConfigClass(
            create_all=getattr(cache.config, f"EASY_FRAMEWORK_DB_{env}_SQL_CREATE_ALL"),
            dialect=getattr(cache.config, f"EASY_FRAMEWORK_DB_{env}_SQL_DIALECT"),
            uri=getattr(cache.config, f"EASY_FRAMEWORK_DB_{env}_SQL_URI"),
            port=getattr(cache.config, f"EASY_FRAMEWORK_DB_{env}_SQL_PORT"),
            databaseName=getattr(cache.config, f"EASY_FRAMEWORK_DB_{env}_SQL_DBNAME"),
            username=getattr(cache.config, f"EASY_FRAMEWORK_DB_{env}_SQL_USERNAME"),
            password=getattr(cache.config, f"EASY_FRAMEWORK_DB_{env}_SQL_PASSWORD"),
        )

    # session = getNewSession()
    def getNewSession(self) -> Session:
        """
        retrieves a new scoped session
        """
        return self.dbConfig.session_scoped()

    # with getScopedSession() as dbSession:
    def getScopedSession(self) -> SessionFactory:
        """
        retrieve a new session and close it automatically when finishing using it.

        ### How to use:
        ```
        > with database.getScopedSession() as dbSession: # use the `with` context
        >     ... # use the dbSession as needed
        > ...
        > # no need to manually close the session. It was already closed when left the context
        ```
        """
        return SessionFactory(self)

    def openSession(self) -> None:
        """
        Default method that actives the session. Don't forget to call
        `.closeSession()` after finishing using the session.

        ### How to use
        ```
        > database.openSession() # Open a new session
        > session = database.dbSession # set the new session as a local var
        ... # Using the session here
        > database.closeSession() # Close the session after using it
        ```
        """
        self.dbSession = self.getNewSession()

    def closeSession(self) -> None:
        """
        Close the session after used. Always call this method
        if you are not using the context method to grab the sessions
        """
        return self.dbConfig.session_scoped.remove()

    def setScopedSession(self) -> None:
        """
        Open a new session and close it automatically when finishing using it.

        ### How to use:
        ```
        > with database.setScopedSession(): # use the `with` context
        >     session = database.session # set the session in a local var
        >     ... # use the session as needed
        > ...
        > # no need to manually close the session. It was already closed when left the context
        ```
        """

        class SessionFactory:
            def __enter__(factorySelf):
                self.openSession()

            def __exit__(factorySelf, exception_type, exception_value, traceback):
                self.closeSession()

        return SessionFactory()
