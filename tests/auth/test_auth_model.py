from tests import TestCase
from datetime import datetime

from easy_framework.auth import AuthModel
from easy_framework.auth import AuthModelMongo
from easy_framework._context import cache

from tests import generate_objectid
from tests.classes import UserTestSql


class TestAuthModel(TestCase):
    def setUp(self) -> None:
        super().setUp()
        UserTestSql(self.get_flask_app_sql(), "test", "123")

    def test_insert_new_session_and_check_it_values(self):
        with self.get_flask_app_sql().test_request_context():
            session = AuthModel(user_id=1, token="123").save()

            self.assertEqual(session.user_id, 1)
            self.assertEqual(session.token, "123")
            self.assertIsInstance(session.expiration_date, datetime)

    def test_insert_new_session_and_check_its_expiration_datetime(self):
        flask_app = self.get_flask_app_sql()

        with flask_app.test_request_context():
            session = AuthModel(user_id=1, token="123").save()

            self.assertGreater(session.expiration_date, datetime.now())
            self.assertLess(
                session.expiration_date,
                datetime.now() + cache.config.EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION,
            )

    def test_insert_new_session_and_check_it_values_mongo(self):
        with self.get_flask_app_mongo().test_request_context():
            _id = generate_objectid()
            session = AuthModelMongo(user_id=_id, token="123").save()

            self.assertEqual(session.user_id, _id)
            self.assertEqual(session.token, "123")
            self.assertIsInstance(session.expiration_date, datetime)

    def test_insert_new_session_and_check_its_expiration_datetime_mongo(self):
        flask_app = self.get_flask_app_mongo()

        with flask_app.test_request_context():
            _id = generate_objectid()
            session = AuthModelMongo(user_id=_id, token="123").save()

            self.assertGreater(session.expiration_date, datetime.now())
            self.assertLess(
                session.expiration_date,
                datetime.now() + cache.config.EASY_FRAMEWORK_AUTH_TOKEN_EXPIRATION,
            )
