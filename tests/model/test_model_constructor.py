
import sqlalchemy as sa
from sqlalchemy import orm
from mongoengine import fields
from flask import Flask

from tests import TestCase
from easy_framework.model import BaseModelSql, BaseModelMongo, ModelConstructor

class TestSqlModelConstructor(TestCase):
    def get_flask_client(self)-> Flask:
        return self.get_flask_app_sql()
    
    class _TestModel(BaseModelSql):
        __tablename__ = 'TestModelConstructor'
        name: orm.Mapped[str] = orm.mapped_column(sa.String(60))

    @property
    def _testConstructor(self):
        class TestSqlConstructor(ModelConstructor):
            __model__ = self._TestModel
            class Meta:
                name = "Test Model"
        return TestSqlConstructor

    def test_check_if_model_constructor_returns_BaseModel_instance(self):
        with self.get_flask_client().app_context():
            self.assertIsInstance(self._testConstructor(), self._TestModel)

    def test_save_sql_model_and_check_in_database(self):
        with self.get_flask_client().app_context():
            id = self._testConstructor().save().id
            entity = self._TestModel.get_one(id=id)
            self.assertTrue(entity)
            self.assertEqual(entity.name, self._testConstructor.Meta.name)
            

class TestMongoModelConstructor(TestSqlModelConstructor):
    def get_flask_client(self)-> Flask:
        return self.get_flask_app_mongo()
    
    class _TestModel(BaseModelMongo):
        meta = {"collection_name": "TestModelConstructor"}
        name = fields.StringField()