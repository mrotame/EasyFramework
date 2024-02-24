from flask import Flask

from tests import TestCase
from easy_framework.view._genericApiView import GenericApiView
from tests.classes import ModelTestMongo
from tests.classes import SerializerTestMongo
from tests.classes import UserTestMongo

class TestGenericApiViewMongo(TestCase):
    def setUp(self) -> None:
        with Flask(__name__).test_request_context(json=self.genericJson()):
            class GenericView (GenericApiView):
                routes=['/GenericViewTest/']
                methods = ["POST", "GET", "PATCH", "DELETE"]
                model = ModelTestMongo
                serializer = SerializerTestMongo
                field_lookup = "username"

            self.view = GenericView
            self.flaskApp = self.get_flask_app_mongo()

            try:
                self.flaskApp.add_url_rule(self.view.routes[0], view_func=self.view.as_view("GenericViewTest"))
            except Exception as e:
                pass
        return super().setUp()    

    def url(self):
        return self.view.routes[0]
    
    def genericJson(self):
        return {"username":"testing", 'password':'123',"desc":"Testing Easy Framework with pytest"}
    
    def test_if_view_auto_insert_data_into_database_with_post(self):
        with self.flaskApp.test_request_context(json=self.genericJson()):
            self.view().auto_post()
            self.assertTrue(ModelTestMongo.get_one(**{"username": self.genericJson()['username']}).desc == self.genericJson()['desc'])

    def test_if_view_auto_read_data_from_database_with_get(self):

        with self.flaskApp.test_request_context(json=self.genericJson()):
            self.view().auto_post()

        with self.flaskApp.test_request_context(query_string={"username":self.genericJson()['username']}): 
            res = self.view().auto_get()
            self.assertEqual(res['username'], self.genericJson()['username'])

    def test_if_view_auto_update_data_from_database_with_patch(self):
        new_desc = "updated by auto_patch"

        with self.flaskApp.test_request_context(json=self.genericJson()):
            self.view().auto_post()

        with self.flaskApp.test_request_context(query_string={"username":self.genericJson()['username']}, json= {"desc":new_desc}): 
            res = self.view().auto_patch()

        with self.flaskApp.test_request_context(query_string={"username":self.genericJson()['username']}): 
            res = self.view().auto_get()
            self.assertEqual(res['desc'], new_desc)

    def test_if_getOwnedEntities_return_all_owned_entities_from_db(self):
        user = UserTestMongo(self.flaskApp, 'test','123')
        with self.flaskApp.app_context():
            testModels_user1 = [ModelTestMongo(desc=f'test_{i}', _owner_id=user.user.id).save() for i in range(0,5)]
            testModels_user2 = [ModelTestMongo(desc=f'test_{i}', _owner_id= 123456789).save() for i in range(5,10)]
        with self.flaskApp.test_request_context(headers={'Authorization': user.token}):
            set_user1_models = [set(SerializerTestMongo().dump(i).items()) for i in testModels_user1]
            set_owned_entities = [set(i.items()) for i in self.view().getOwnedEntities()]
            self.assertEqual(set_user1_models, set_owned_entities)

    def test_if_getOwnedEntities_do_not_return_not_owned_entities_from_db(self):
        user = UserTestMongo(self.flaskApp, 'test','123')
        with self.flaskApp.app_context():
            testModels_user1 = [ModelTestMongo(desc=f'test_{i}', _owner_id=user.user.id).save() for i in range(0,5)]
            testModels_user2 = [ModelTestMongo(desc=f'test_{i}', _owner_id= 123456789).save() for i in range(5,10)]

        with self.flaskApp.test_request_context(headers={'Authorization': user.token}):
            set_user2_models = [set(SerializerTestMongo().dump(i).items()) for i in testModels_user2]
            set_owned_entities = [set(i.items()) for i in self.view().getOwnedEntities()]
            self.assertFalse(any([i in set_user2_models for i in set_owned_entities]))

    