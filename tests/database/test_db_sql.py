from sqlalchemy.orm import Session

from tests import TestCase
from tests.classes import ModelTestSql


class TestDbSql(TestCase):
    def test_assert_session_is_active_before_closing_it(self):
        dbSession: Session = self.get_sqldb().getNewSession()

        self.assertTrue(dbSession.is_active)

        self.get_sqldb().closeSession()

    def test_receive_scoped_session_and_check_if_is_active(self):
        with self.get_sqldb().getScopedSession() as dbSession:

            self.assertTrue(dbSession.is_active)
    
    def test_set_scoped_session_and_check_if_is_active(self):
        sqldb = self.get_sqldb()
        with sqldb.setScopedSession():
            self.assertTrue(sqldb.dbSession.is_active)

    def test_get_session_and_check_if_is_active(self):
        dbSession = self.get_sqldb().getNewSession()
        self.assertTrue(dbSession.is_active)
        self.get_sqldb().closeSession()

    def test_set_session_and_check_if_is_active(self):
        sqldb = self.get_sqldb()
        sqldb.openSession()
        self.assertTrue(sqldb.dbSession.is_active)
        sqldb.closeSession()

    def test_getting_scoped_session_save_new_entity_into_sqldb_and_check_if_is_there(self):
        with self.get_flask_app_sql().app_context():
            test_entity = ModelTestSql(id=1, info="hello there! I'm a testing entity")
            with self.get_sqldb().getScopedSession() as dbSession:
                dbSession.add(test_entity)
                dbSession.commit()

            with self.get_sqldb().getScopedSession() as dbSession:
                self.assertEqual(dbSession.query(ModelTestSql).filter(ModelTestSql.id==1).count(), 1)

    def test_setting_scoped_session_save_new_entity_into_get_sqldb_and_check_if_is_there(self):
        with self.get_flask_app_sql().app_context():
            sqldb = self.get_sqldb()
            test_entity = ModelTestSql(id=1, info="hello there! I'm a testing entity")
            with sqldb.setScopedSession():
                sqldb.dbSession.add(test_entity)
                sqldb.dbSession.commit()

            with sqldb.setScopedSession():
                self.assertEqual(sqldb.dbSession.query(ModelTestSql).filter(ModelTestSql.id==1).count(), 1)

    def test_getting_session_save_new_entity_into_get_sqldb_and_check_if_is_there(self):
        with self.get_flask_app_sql().app_context():
            sqldb = self.get_sqldb()
            test_entity = ModelTestSql(id=1, info="hello there! I'm a testing entity")
            dbSession = sqldb.getNewSession()
            dbSession.add(test_entity)
            dbSession.commit()
            sqldb.closeSession()

            dbSession = self.get_sqldb().getNewSession()
            self.assertEqual(dbSession.query(ModelTestSql).filter(ModelTestSql.id==1).count(), 1)
            self.get_sqldb().closeSession()

    def test_setting_session_save_new_entity_into_get_sqldb_and_check_if_is_there(self):
        with self.get_flask_app_sql().app_context():
            sqldb = self.get_sqldb()
            test_entity = ModelTestSql(id=1, info="hello there! I'm a testing entity")
            sqldb.openSession()
            sqldb.dbSession.add(test_entity)
            sqldb.dbSession.commit()
            sqldb.closeSession()

            sqldb.openSession()
            self.assertEqual(sqldb.dbSession.query(ModelTestSql).filter(ModelTestSql.id==1).count(), 1)
            sqldb.closeSession()
    

        