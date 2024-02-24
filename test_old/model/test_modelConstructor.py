
import sqlalchemy as sa
from mongoengine import fields

from easy_framework.model import BaseModelSql, BaseModelMongo, ModelConstructor
from test.easy_framework_conftest import FlaskClient

class TestSqlModelConstructor:
    flaskClient = FlaskClient().flaskApp

    class _TestModel(BaseModelSql):
        __tablename__ = 'TestModelConstructor'
        name = sa.Column(sa.String(60))

    @property
    def _testConstructor(self):
        class TestSqlConstructor(ModelConstructor):
            __model__ = self._TestModel
            class Meta:
                name = "Test Model"
        return TestSqlConstructor

    def test_check_if_model_constructor_returns_BaseModel_instance(self):
        with self.flaskClient.app_context():
            assert isinstance(self._testConstructor(), self._TestModel)

    def test_save_sql_model_and_check_in_database(self):
        with self.flaskClient.app_context():
            id = self._testConstructor().save().id
            entity = self._TestModel.get_one(id=id)
            assert entity
            assert entity.name == self._testConstructor.Meta.name
            

class TestMongoModelConstructor(TestSqlModelConstructor):
    flaskClient = FlaskClient().flaskAppMongo

    class _TestModel(BaseModelMongo):
        meta = {"collection_name": "TestModelConstructor"}
        name = fields.StringField()