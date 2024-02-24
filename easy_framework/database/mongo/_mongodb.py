import uuid
from mongoengine import connect
import os
from flask import Flask

class Mongodb:

    def __init__(self, flaskApp: Flask):
        self.uri: str = flaskApp.config["EASY_FRAMEWORK_DB_MONGO_URI"]
        self.port: int = int(flaskApp.config["EASY_FRAMEWORK_DB_MONGO_PORT"])
        self.username: str = flaskApp.config["EASY_FRAMEWORK_DB_MONGO_USERNAME"]
        self.password: str = flaskApp.config["EASY_FRAMEWORK_DB_MONGO_PASSWORD"]
        self.database: str = flaskApp.config["EASY_FRAMEWORK_DB_MONGO_DBNAME"]
        self.authMecanism: str = flaskApp.config["EASY_FRAMEWORK_DB_MONGO_AUTHMECHANISM"]
        self.authSource: str = flaskApp.config["EASY_FRAMEWORK_DB_MONGO_AUTHSOURCE"]

        self.client = connect(host=f"mongodb://{self.username}:{self.password}@{self.uri}:{self.port}/{self.database}?authMechanism={self.authMecanism}&authSource={self.authSource}", uuidrepresentation="standard")


    def delete_all(self):
        self.client.drop_database('test')

