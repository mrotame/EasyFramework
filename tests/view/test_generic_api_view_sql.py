from flask import Flask
from easy_framework.view._genericApiView import GenericApiView
from tests.classes import ModelTestSql, SerializerTestSql, UserTestSql
from tests import TestCase, FlaskClient


class TestGenericApiView(TestCase):

    class GenericView(GenericApiView):
        routes = ["/GenericViewTest/"]
        methods = ["POST", "GET", "PATCH", "DELETE"]
        model = ModelTestSql
        serializer = SerializerTestSql
        field_lookup = "name"

    def setUp(self) -> None:
        super().setUp()

        with Flask(__name__).test_request_context(json=self.genericJson()):
            self.view = self.GenericView
            self.flaskApp = self.get_flask_app_sql()

            try:
                for route in self.view.routes:
                    self.flaskApp.add_url_rule(
                        route, view_func=self.view.as_view(f"GenericViewTest/{route}")
                    )
            except Exception as e:
                pass

    def url(self):
        return self.view.routes[0]

    def genericJson(self):
        return {"name": "testing", "desc": "Testing Easy Framework with pytest"}

    def test_if_view_auto_insert_data_into_database_with_post(self):
        with self.flaskApp.test_request_context(json=self.genericJson()):
            self.view().auto_post()

            self.assertEqual(
                ModelTestSql.get_one(
                    ModelTestSql.name == self.genericJson()["name"]
                ).desc,
                self.genericJson()["desc"],
            )

    def test_if_view_auto_read_data_from_database_with_get(self):
        with self.flaskApp.test_request_context(json=self.genericJson()):
            self.view().auto_post()

        with self.flaskApp.test_request_context(
            query_string={"name": self.genericJson()["name"]}
        ):
            res = self.view().auto_get()
            self.assertEqual(res["desc"], self.genericJson()["desc"])

    def test_if_view_auto_update_data_from_database_with_patch(self):
        new_desc = "updated by auto_patch"

        with self.flaskApp.test_request_context(json=self.genericJson()):
            self.view().auto_post()

        with self.flaskApp.test_request_context(
            query_string={"name": self.genericJson()["name"]}, json={"desc": new_desc}
        ):
            res = self.view().auto_patch()

        with self.flaskApp.test_request_context(
            query_string={"name": self.genericJson()["name"]}
        ):
            res = self.view().auto_get()
            self.assertEqual(res["desc"], new_desc)

    def test_if_view_auto_delete_data_from_database_with_delete(self):
        with self.flaskApp.test_request_context(json=self.genericJson()):
            self.view().auto_post()

        with self.flaskApp.test_request_context(
            query_string={"name": self.genericJson()["name"]}
        ):
            res = self.view().auto_delete()

        with self.flaskApp.test_request_context(
            query_string={"name": self.genericJson()["name"]}
        ):
            res = self.view().auto_get()
            self.assertFalse(res)

        with self.flaskApp.test_request_context():
            res = self.view().auto_get()
            self.assertFalse(res)

    def test_if_getOwnedEntities_return_all_owned_entities_from_db(self):
        user = UserTestSql(self.flaskApp, "test", "123")
        with self.flaskApp.app_context():
            testModels_user1 = [
                ModelTestSql(desc=f"test_{i}", _owner_id=user.user.id).save()
                for i in range(0, 5)
            ]
            testModels_user2 = [
                ModelTestSql(desc=f"test_{i}", _owner_id=123456789).save()
                for i in range(5, 10)
            ]

        with self.flaskApp.test_request_context(headers={"Authorization": user.token}):
            set_user1_models = [
                set(SerializerTestSql().dump(i).items()) for i in testModels_user1
            ]
            set_owned_entities = [
                set(i.items()) for i in self.view().getOwnedEntities()
            ]
            self.assertEqual(set_user1_models, set_owned_entities)

    def test_if_getOwnedEntities_do_not_return_not_owned_entities_from_db(self):
        user = UserTestSql(self.flaskApp, "test", "123")
        with self.flaskApp.app_context():
            testModels_user1 = [
                ModelTestSql(desc=f"test_{i}", _owner_id=user.user.id).save()
                for i in range(0, 5)
            ]
            testModels_user2 = [
                ModelTestSql(desc=f"test_{i}", _owner_id=123456789).save()
                for i in range(5, 10)
            ]

        with self.flaskApp.test_request_context(headers={"Authorization": user.token}):
            set_user2_models = [
                set(SerializerTestSql().dump(i).items()) for i in testModels_user2
            ]
            set_owned_entities = [
                set(i.items()) for i in self.view().getOwnedEntities()
            ]
            self.assertFalse(any([i in set_user2_models for i in set_owned_entities]))


class TestGenericApiViewWithPathFieldlookup(TestGenericApiView):
    def setUp(self) -> None:
        super().setUp()
        with Flask(__name__).test_request_context(json=self.genericJson()):
            self.view = self.GenericView
            self.flaskApp = FlaskClient().flaskApp

            for route in self.view.routes:
                self.flaskApp.add_url_rule(
                    route, view_func=self.view.as_view(f"GenericViewTest/{route}")
                )

    class GenericView(TestGenericApiView.GenericView):
        routes = ["/GenericViewPathTest/<id>", "/GenericViewPathTest"]
        field_lookup_method = "path"
        field_lookup = "id"

    def test_if_view_auto_read_data_from_database_with_get(self):
        with self.flaskApp.app_context():
            entity = ModelTestSql(username="test").save()

        client = self.flaskApp.test_client()
        res = client.get(f"/GenericViewPathTest/{entity.id}")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["id"], entity.id)

    def test_if_view_auto_update_data_from_database_with_patch(self):
        new_desc = "updated by auto_patch"

        with self.flaskApp.app_context():
            entity = ModelTestSql(username="test").save()

        client = self.flaskApp.test_client()
        client.patch(
            self.GenericView.routes[0].replace("<id>", str(entity.id)),
            json={"desc": new_desc},
        )

        res = client.get(self.GenericView.routes[0].replace("<id>", str(entity.id)))

        self.assertEqual(res.get_json()["desc"], new_desc)

    def test_if_view_auto_delete_data_from_database_with_delete(self):
        with self.flaskApp.app_context():
            entity = ModelTestSql(username="test").save()

        client = self.flaskApp.test_client()
        client.delete(self.GenericView.routes[0].replace("<id>", str(entity.id)))

        res = client.get(self.GenericView.routes[0].replace("<id>", str(entity.id)))
        self.assertFalse(res.get_json())

        res = client.get(self.GenericView.routes[0])
        self.assertFalse(res.get_json())
