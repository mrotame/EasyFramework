from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, scoped_session, sessionmaker
from sqlalchemy.orm.session import close_all_sessions, Engine

from ._base import Base as DefaultBase


class DbConfig:
    """
    SQLAlchemy Database configuration class.
    Here we define the engine and prepare the sessions and scoped sessions
    to be used by the main database class
    """

    __dialect: str
    __databaseName: str
    __uri: str
    __port: str
    __username: str
    __password: str

    echo: bool = False
    base: DefaultBase
    engine: Engine
    session: Session
    session_scoped: scoped_session

    def __init__(
        self,
        dialect,
        uri,
        databaseName,
        port,
        username,
        password,
        create_all,
        base=DefaultBase,
    ) -> None:
        self.__dialect = dialect
        self.__username = username
        self.__databaseName = databaseName
        self.__password = password
        self.__port = port
        self.__uri = uri

        self.base = base

        self.string_url = self.getStringUri()
        self.engine = self.createEngine()

        self.session = sessionmaker(bind=self.engine)
        self.session_scoped = scoped_session(sessionmaker(bind=self.engine))
        if create_all:
            self.create_all()

    def createEngine(self) -> Engine:
        """
        returns the SQLAlchemy engine
        """
        return create_engine(
            self.string_url,
            pool_recycle=300,
            pool_pre_ping=True,
            echo=self.echo,
        )

    def getStringUri(self) -> str:
        """
        returns the uri connection string
        """
        if self.__dialect == "sqlite":
            return f"{self.__dialect}://{self.__uri}{self.__databaseName}"

        return f"{self.__dialect}://{self.__username}:{self.__password}@{self.__uri}:{self.__port}/{self.__databaseName}"

    def create_all(self) -> None:
        """
        Create all tables for all models registered within the same base
        """
        self.base.metadata.create_all(self.engine)

    def delete_all(self) -> None:
        """
        Drop all tables for all models registered within the same base
        """
        self.base.metadata.drop_all(self.engine)

    def close_all_sessions(self) -> None:
        """
        Close all connection sessions
        """
        close_all_sessions()
