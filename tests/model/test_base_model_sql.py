import flask

from tests import TestCase
from tests.classes import ModelTestSql
from easy_framework.user.userModel import UserModel


class TestBasemodelSql(TestCase):
    def test_save_model_into_sqldb(self):
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql()
            new_entity.save()

            with self.get_sqldb().getScopedSession() as dbSession:
                self.assertEqual(dbSession.query(ModelTestSql).filter(ModelTestSql.id == new_entity.id).count(), 1)

    def test_get_one_model_in_sqldb(self):
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql()
            with self.get_sqldb().getScopedSession() as dbSession:
                dbSession.add(new_entity)
                dbSession.commit()
                dbSession.refresh(new_entity)

            entity = ModelTestSql.get_one(ModelTestSql.id == new_entity.id)
            self.assertIsNotNone(entity)

    def test_get_many_model_in_sqldb(self):
        with self.get_flask_app_sql().app_context():
            with self.get_sqldb().getScopedSession() as dbSession:
                dbSession.add_all([ModelTestSql(),ModelTestSql(),ModelTestSql()])
                dbSession.commit()

            entities = ModelTestSql.get_many()
            self.assertEqual(len(entities), 3)

    def test_save_model_into_sqldb_and_check_its_existence(self):
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql(id= 1)
            new_entity.save()

            del new_entity

            with self.get_sqldb().getScopedSession() as dbSession:
                self.assertEqual(dbSession.query(ModelTestSql.id == 1).count(), 1)


    def test_save_model_into_sqldb_and_check_its_content(self):
        info="hello there! I'm a testing entity!"
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql(id= 32, info=info)
            new_entity.save()

            del new_entity

            with self.get_sqldb().getScopedSession() as dbSession:
                self.assertEqual(dbSession.query(ModelTestSql).filter(ModelTestSql.id == 32).first().info, info)

    def test_update_model_in_sqldb_and_check_if_it_was_updated(self, ):
        old_info="hello there! I'm a testing entity!"
        new_info ="I was updated !!!"
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql(id= 55, info=old_info)
            new_entity.save()

            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==55)
            entity.info = new_info
            entity.update()

            del entity

            with self.get_sqldb().getScopedSession() as dbSession:
                self.assertEqual(dbSession.query(ModelTestSql).filter(ModelTestSql.id == 55).first().info, new_info)
    
    def test_hard_delete_model_in_sqldb_and_check_its_non_existance(self, ):
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql(id= 1, info="hello there! I'm a testing entity!")
            new_entity.save()
            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            entity.delete(method='hard')

            with self.get_sqldb().getScopedSession() as dbSession:
                self.assertIsNone(dbSession.query(ModelTestSql).filter(ModelTestSql.id == 1).first(), None)

    def test_soft_delete_model_in_sqldb_and_check_if_deleted_field_is_setted_to_True(self, ):
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql(id= 1, info="hello there! I'm a testing entity!")
            new_entity.save()
            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            entity.delete(method='soft')

            with self.get_sqldb().getScopedSession() as dbSession:
                self.assertTrue(dbSession.query(ModelTestSql).filter(ModelTestSql.id == 1).first()._deleted, True)
        
    def test_query_a_hard_deleted_model_and_return_none(self, ):
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql(id= 1, info="hello there! I'm a testing entity!")
            new_entity.save()
            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            entity.delete(method='hard')

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            self.assertIsNone(entity)

    def test_query_a_soft_deleted_model_and_return_none(self, ):
        with self.get_flask_app_sql().app_context():
            new_entity = ModelTestSql(id= 1, info="hello there! I'm a testing entity!")
            new_entity.save()
            del new_entity

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            entity.delete(method='soft')

            entity = ModelTestSql.get_one(ModelTestSql.id==1)
            self.assertIsNone(entity)

            entity = ModelTestSql.get_many(ModelTestSql.id==1)
            self.assertFalse(entity)


    def test_create_entity_with_user_context_and_register_user_id_as_owner(self):
        with self.get_flask_app_sql().test_request_context():
            flask.g.user = UserModel(login='123', password = '123').save()
            new_entity = ModelTestSql(username='test_soft_delete', password='123', desc="hello there! I'm a testing entity!").save()

            self.assertEqual(ModelTestSql.get_one(id=new_entity.id)._owner_id, flask.g.user.id)


    