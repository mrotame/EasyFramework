from test.testClasses import ModelTestMongo

from flask import Flask
import flask

from easy_framework.database.mongo import Mongodb
from easy_framework.user.userModelMongo import UserModelMongo


class TestBasemodelSql:
    def test_save_model_into_mongodb(self, mongodb: Mongodb, flaskApp: Flask):
            new_entity = ModelTestMongo(username='test',password='test')
            new_entity.save()

            assert ModelTestMongo.get_one(ModelTestMongo.username == new_entity.username).username == 'test'

    def test_get_one_model_in_mongodb(self, mongodb: Mongodb, flaskApp: Flask):
            new_entity = ModelTestMongo(username='test',password='test').save()

            entity = ModelTestMongo.get_one(ModelTestMongo.username == new_entity.username)
            assert entity is not None

    def test_get_many_model_in_mongodb(self, mongodb:Mongodb, flaskApp: Flask):
            for i in range(3):
                ModelTestMongo(username=f'test{i}',password='test').save()

            entities = ModelTestMongo.get_many()
            assert len(entities) == 3

    def test_save_model_into_mongodb_and_check_its_existence(self, mongodb:Mongodb, flaskApp: Flask):
        new_entity = ModelTestMongo(username='test',password='test', desc='1')
        new_entity.save()

        del new_entity

        assert ModelTestMongo.get_one(ModelTestMongo.desc == "1")

    def test_save_model_into_mongodb_and_check_its_content(self, mongodb:Mongodb, flaskApp: Flask):
        desc="hello there! I'm a testing entity! ;D"

        new_entity = ModelTestMongo(username="desc_test", password="test", desc=desc)
        new_entity.save()

        del new_entity

        assert ModelTestMongo.get_one(ModelTestMongo.desc == desc).username == 'desc_test'

    def test_update_model_in_mongodb_and_check_if_it_was_updated(self,mongodb:Mongodb, flaskApp: Flask):
        old_desc="hello there! I'm a testing entity! ;D"
        new_desc ="I was updated !!!"

        new_entity = ModelTestMongo(username='test_update', password='123', desc=old_desc).save()

        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username==55)
        entity.desc = new_desc
        entity.update()

        del entity

        assert ModelTestMongo.get_one(ModelTestMongo.username == 'test_update').desc == new_desc
    
    def test_hard_delete_model_in_mongodb_and_check_its_non_existance(self,mongodb:Mongodb, flaskApp: Flask):
        new_entity = ModelTestMongo(username='test_delete', password='123', desc="hello there! I'm a testing entity! ;D")
        new_entity.save()
        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_delete')
        entity.delete(method='hard')
        del entity

        assert ModelTestMongo.get_one(ModelTestMongo.username == 'test_delete') is None

    def test_soft_delete_model_in_mongodb_and_check_if_deleted_field_is_setted_to_True(self,mongodb:Mongodb, flaskApp: Flask):
        new_entity = ModelTestMongo(username='test_hard_delete', password='123', desc="hello there! I'm a testing entity! ;D")
        new_entity.save()
        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_hard_delete')
        entity.delete(method='soft')

        assert ModelTestMongo.objects(ModelTestMongo.username == 'test_hard_delete').first()._deleted == True
        
    def test_query_a_hard_deleted_model_and_return_none(self,mongodb:Mongodb, flaskApp: Flask):
        new_entity = ModelTestMongo(username='test_hard_delete', password='123', desc="hello there! I'm a testing entity! ;D")
        new_entity.save()
        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_hard_delete')
        entity.delete(method='hard')

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_hard_delete')
        assert entity is None

    def test_query_a_soft_deleted_model_and_return_none(self,mongodb:Mongodb, flaskApp: Flask):
        new_entity = ModelTestMongo(username='test_soft_delete', password='123', desc="hello there! I'm a testing entity! ;D")
        new_entity.save()
        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_soft_delete')
        entity.delete(method='soft')

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_soft_delete')
        assert entity is None 

        entity = ModelTestMongo.get_many(ModelTestMongo.id==1)
        assert not entity

    def test_create_entity_with_user_context_and_register_user_id_as_owner(self, mongodb:Mongodb, flaskAppMongo: Flask):
        with flaskAppMongo.test_request_context():
            flask.g.user = UserModelMongo(login='123', password = '123').save()
            new_entity = ModelTestMongo(username='test_soft_delete', password='123', desc="hello there! I'm a testing entity! ;D").save()

            assert ModelTestMongo.get_one(id=new_entity.id)._owner_id == flask.g.user.id
            




    