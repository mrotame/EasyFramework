from test.testClasses import ModelTestSql
from flask import Flask
from sqlalchemy.orm import Session

from easy_framework.database.sql import Sqldb

class TestDbSql():
        
    def test_assert_session_is_active_before_closing_it(self, sqldb: Sqldb):
        dbSession: Session = sqldb.getNewSession()
        assert dbSession.is_active
        sqldb.closeSession()

    def test_receive_scoped_session_and_check_if_is_active(self, sqldb:Sqldb):
        with sqldb.getScopedSession() as dbSession:
            assert dbSession.is_active
    
    def test_set_scoped_session_and_check_if_is_active(self, sqldb:Sqldb):
        with sqldb.setScopedSession():
            assert sqldb.dbSession.is_active

    def test_get_session_and_check_if_is_active(self, sqldb:Sqldb):
        dbSession = sqldb.getNewSession()
        assert dbSession.is_active
        sqldb.closeSession()

    def test_set_session_and_check_if_is_active(self, sqldb:Sqldb):
        sqldb.openSession()
        assert sqldb.dbSession.is_active
        sqldb.closeSession()

    def test_getting_scoped_session_save_new_entity_into_sqldb_and_check_if_is_there(self, sqldb: Sqldb, flaskApp:Flask):
        with flaskApp.app_context():
            test_entity = ModelTestSql(id=1, info="hello there! I'm a testing entity")
            with sqldb.getScopedSession() as dbSession:
                dbSession.add(test_entity)
                dbSession.commit()

            with sqldb.getScopedSession() as dbSession:
                assert dbSession.query(ModelTestSql).filter(ModelTestSql.id==1).count() == 1

    def test_setting_scoped_session_save_new_entity_into_sqldb_and_check_if_is_there(self, sqldb: Sqldb, flaskApp:Flask):
        with flaskApp.app_context():
            test_entity = ModelTestSql(id=1, info="hello there! I'm a testing entity")
            with sqldb.setScopedSession():
                sqldb.dbSession.add(test_entity)
                sqldb.dbSession.commit()

            with sqldb.setScopedSession():
                assert sqldb.dbSession.query(ModelTestSql).filter(ModelTestSql.id==1).count() == 1

    def test_getting_session_save_new_entity_into_sqldb_and_check_if_is_there(self, sqldb: Sqldb, flaskApp:Flask):
        with flaskApp.app_context():
            test_entity = ModelTestSql(id=1, info="hello there! I'm a testing entity")
            dbSession = sqldb.getNewSession()
            dbSession.add(test_entity)
            dbSession.commit()
            sqldb.closeSession()

            dbSession = sqldb.getNewSession()
            assert dbSession.query(ModelTestSql).filter(ModelTestSql.id==1).count() == 1
            sqldb.closeSession()

    def test_setting_session_save_new_entity_into_sqldb_and_check_if_is_there(self, sqldb: Sqldb, flaskApp:Flask):
        with flaskApp.app_context():
            test_entity = ModelTestSql(id=1, info="hello there! I'm a testing entity")
            sqldb.openSession()
            sqldb.dbSession.add(test_entity)
            sqldb.dbSession.commit()
            sqldb.closeSession()

            sqldb.openSession()
            assert sqldb.dbSession.query(ModelTestSql).filter(ModelTestSql.id==1).count() == 1
            sqldb.closeSession()
    

        