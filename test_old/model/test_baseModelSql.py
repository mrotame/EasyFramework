from test.testClasses import ModelTestSql

from flask import Flask
import flask

from easy_framework.database.sql import Sqldb
from easy_framework.user.userModel import UserModel


class TestBasemodelSql:
    def test_save_model_into_sqldb(self, sqldb: Sqldb, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTestSql()
            new_entity.save()

            with sqldb.getScopedSession() as dbSession:
                assert dbSession.query(ModelTestSql).filter(ModelTestSql.id == new_entity.id).count() == 1

    def test_get_one_model_in_sqldb(self, sqldb: Sqldb, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTestSql()
            with sqldb.getScopedSession() as dbSession:
                dbSession.add(new_entity)
                dbSession.commit()
                dbSession.refresh(new_entity)

            entity = ModelTestSql.get_one(ModelTestSql.id == new_entity.id)
            assert entity is not None

    def test_get_many_model_in_sqldb(self, sqldb:Sqldb, flaskApp: Flask):
        with flaskApp.app_context():
            with sqldb.getScopedSession() as dbSession:
                dbSession.add_all([ModelTestSql(),ModelTestSql(),ModelTestSql()])
                dbSession.commit()

            entities = ModelTestSql.get_many()
            assert len(entities) == 3

    def test_save_model_into_sqldb_and_check_its_existence(self, sqldb:Sqldb, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTestSql(id= 1)
            new_entity.save()

            del new_entity

            with sqldb.getScopedSession() as dbSession:
                assert dbSession.query(ModelTestSql.id == 1).count() == 1


    def test_save_model_into_sqldb_and_check_its_content(self, sqldb:Sqldb, flaskApp: Flask):
        info="hello there! I'm a testing entity!"
        with flaskApp.app_context():
            new_entity = ModelTestSql(id= 32, info=info)
            new_entity.save()

            del new_entity

            with sqldb.getScopedSession() as dbSession:
                assert dbSession.query(ModelTestSql).filter(ModelTestSql.id == 32).first().info == info

    def test_update_model_in_sqldb_and_check_if_it_was_updated(self,sqldb:Sqldb, flaskApp: Flask):
        old_info="hello there! I'm a testing entity!"
        new_info ="I was updated !!!"
        with flaskApp.app_context():
            new_entity = ModelTestSql(id= 55, info=old_info)
            new_entity.save()

            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==55)
            entity.info = new_info
            entity.update()

            del entity

            with sqldb.getScopedSession() as dbSession:
                assert dbSession.query(ModelTestSql).filter(ModelTestSql.id == 55).first().info == new_info
    
    def test_hard_delete_model_in_sqldb_and_check_its_non_existance(self,sqldb:Sqldb, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTestSql(id= 1, info="hello there! I'm a testing entity!")
            new_entity.save()
            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            entity.delete(method='hard')

            with sqldb.getScopedSession() as dbSession:
                assert dbSession.query(ModelTestSql).filter(ModelTestSql.id == 1).first() is None

    def test_soft_delete_model_in_sqldb_and_check_if_deleted_field_is_setted_to_True(self,sqldb:Sqldb, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTestSql(id= 1, info="hello there! I'm a testing entity!")
            new_entity.save()
            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            entity.delete(method='soft')

            with sqldb.getScopedSession() as dbSession:
                assert dbSession.query(ModelTestSql).filter(ModelTestSql.id == 1).first()._deleted == True
        
    def test_query_a_hard_deleted_model_and_return_none(self,sqldb:Sqldb, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTestSql(id= 1, info="hello there! I'm a testing entity!")
            new_entity.save()
            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            entity.delete(method='hard')

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            assert entity is None

    def test_query_a_soft_deleted_model_and_return_none(self,sqldb:Sqldb, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTestSql(id= 1, info="hello there! I'm a testing entity!")
            new_entity.save()
            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            entity.delete(method='soft')

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            assert entity is None 

            entity = ModelTestSql.get_many(ModelTestSql.id==1)
            assert not entity


    def test_create_entity_with_user_context_and_register_user_id_as_owner(self, sqldb:Sqldb, flaskApp: Flask):
        with flaskApp.test_request_context():
            flask.g.user = UserModel(login='123', password = '123').save()
            new_entity = ModelTestSql(username='test_soft_delete', password='123', desc="hello there! I'm a testing entity!").save()

            assert ModelTestSql.get_one(id=new_entity.id)._owner_id == flask.g.user.id


    