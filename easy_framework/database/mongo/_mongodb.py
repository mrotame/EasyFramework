from mongoengine import connect

from easy_framework._context import cache


class Mongodb:

    def __init__(self):
        self.uri: str = cache.config.EASY_FRAMEWORK_DB_MONGO_URI
        self.port: int = int(cache.config.EASY_FRAMEWORK_DB_MONGO_PORT)
        self.username: str = cache.config.EASY_FRAMEWORK_DB_MONGO_USERNAME
        self.password: str = cache.config.EASY_FRAMEWORK_DB_MONGO_PASSWORD
        self.database: str = cache.config.EASY_FRAMEWORK_DB_MONGO_DBNAME
        self.authMecanism: str = cache.config.EASY_FRAMEWORK_DB_MONGO_AUTHMECHANISM
        self.authSource: str = cache.config.EASY_FRAMEWORK_DB_MONGO_AUTHSOURCE

        self.client = connect(
            host=f"mongodb://{self.username}:{self.password}@{self.uri}:{self.port}/{self.database}?authMechanism={self.authMecanism}&authSource={self.authSource}",
            uuidrepresentation="standard",
        )

    def delete_all(self):
        self.client.drop_database("test")
