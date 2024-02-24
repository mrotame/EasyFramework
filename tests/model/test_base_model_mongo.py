import flask

from tests import TestCase
from tests.classes import ModelTestMongo
from easy_framework.user.userModelMongo import UserModelMongo


class TestBasemodelMongo(TestCase):
    def test_save_model_into_mongodb(self):
            new_entity = ModelTestMongo(username='test',password='test')
            new_entity.save()

            self.assertEqual(ModelTestMongo.get_one(ModelTestMongo.username == new_entity.username).username,'test')

    def test_get_one_model_in_mongodb(self):
            new_entity = ModelTestMongo(username='test',password='test').save()

            entity = ModelTestMongo.get_one(ModelTestMongo.username == new_entity.username)
            self.assertIsNotNone(entity)

    def test_get_many_model_in_mongodb(self):
            for i in range(3):
                ModelTestMongo(username=f'test{i}',password='test').save()

            entities = ModelTestMongo.get_many()
            self.assertEqual(len(entities), 3)

    def test_save_model_into_mongodb_and_check_its_existence(self):
        new_entity = ModelTestMongo(username='test',password='test', desc='1')
        new_entity.save()

        del new_entity

        self.assertIsNotNone(ModelTestMongo.get_one(ModelTestMongo.desc == "1"))

    def test_save_model_into_mongodb_and_check_its_content(self):
        desc="hello there! I'm a testing entity! ;D"

        new_entity = ModelTestMongo(username="desc_test", password="test", desc=desc)
        new_entity.save()

        del new_entity

        self.assertEqual(ModelTestMongo.get_one(ModelTestMongo.desc == desc).username, 'desc_test')

    def test_update_model_in_mongodb_and_check_if_it_was_updated(self):
        old_desc="hello there! I'm a testing entity! ;D"
        new_desc ="I was updated !!!"

        new_entity = ModelTestMongo(username='test_update', password='123', desc=old_desc).save()

        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username==55)
        entity.desc = new_desc
        entity.update()

        del entity

        self.assertEqual(ModelTestMongo.get_one(ModelTestMongo.username == 'test_update').desc, new_desc)
    
    def test_hard_delete_model_in_mongodb_and_check_its_non_existance(self):
        new_entity = ModelTestMongo(username='test_delete', password='123', desc="hello there! I'm a testing entity! ;D")
        new_entity.save()
        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_delete')
        entity.delete(method='hard')
        del entity

        self.assertIsNone(ModelTestMongo.get_one(ModelTestMongo.username == 'test_delete'))

    def test_soft_delete_model_in_mongodb_and_check_if_deleted_field_is_setted_to_True(self):
        new_entity = ModelTestMongo(username='test_hard_delete', password='123', desc="hello there! I'm a testing entity! ;D")
        new_entity.save()
        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_hard_delete')
        entity.delete(method='soft')

        self.assertTrue(ModelTestMongo.objects(ModelTestMongo.username == 'test_hard_delete').first()._deleted)
        
    def test_query_a_hard_deleted_model_and_return_none(self):
        new_entity = ModelTestMongo(username='test_hard_delete', password='123', desc="hello there! I'm a testing entity! ;D")
        new_entity.save()
        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_hard_delete')
        entity.delete(method='hard')

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_hard_delete')
        self.assertIsNone(entity)

    def test_query_a_soft_deleted_model_and_return_none(self):
        new_entity = ModelTestMongo(username='test_soft_delete', password='123', desc="hello there! I'm a testing entity! ;D")
        new_entity.save()
        del new_entity

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_soft_delete')
        entity.delete(method='soft')

        entity = ModelTestMongo.get_one(ModelTestMongo.username=='test_soft_delete')
        self.assertIsNone(entity)

        entity = ModelTestMongo.get_many(ModelTestMongo.id==1)
        self.assertFalse(entity)

    def test_create_entity_with_user_context_and_register_user_id_as_owner(self):
        with self.get_flask_app_mongo().test_request_context():
            flask.g.user = UserModelMongo(login='123', password = '123').save()
            new_entity = ModelTestMongo(username='test_soft_delete', password='123', desc="hello there! I'm a testing entity! ;D").save()

            self.assertEqual(ModelTestMongo.get_one(id=new_entity.id)._owner_id, flask.g.user.id)
            




    