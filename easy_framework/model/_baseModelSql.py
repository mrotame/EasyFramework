from __future__ import annotations

import typing as t
from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy import orm

from easy_framework.user.userMixin import UserMixin
from easy_framework.user.utils import current_user
from easy_framework.database.sql import Sqldb, Base


class BaseModelSql(orm.MappedAsDataclass, Base):
    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(init=False, primary_key=True)
    _owner_id: orm.Mapped[t.Optional[int]] = orm.mapped_column(
        init=False,
        nullable=True,
        insert_default=lambda: (
            current_user.id if isinstance(current_user, UserMixin) else None
        ),
    )
    _created_at: orm.Mapped[datetime] = orm.mapped_column(
        init=False, server_default=func.now()
    )
    _updated_at: orm.Mapped[datetime] = orm.mapped_column(
        init=False, server_default=func.now(), server_onupdate=func.now()
    )
    _deleted: orm.Mapped[bool] = orm.mapped_column(init=False, insert_default=False)

    @classmethod
    def get_databaseClass(self) -> Sqldb:
        return Sqldb()

    @classmethod
    def get_one(cls, *args, **kwargs) -> t.Self:
        with cls.get_databaseClass().getScopedSession() as dbSession:
            if args:
                return (
                    cls.get_one_base_query(dbSession, cls)
                    .filter(*args, **kwargs)
                    .first()
                )
            else:
                return (
                    cls.get_one_base_query(dbSession, cls).filter_by(**kwargs).first()
                )

    @classmethod
    def get_many(cls, *args, **kwargs) -> t.List[t.Self]:
        with cls.get_databaseClass().getScopedSession() as dbSession:
            if args:
                return (
                    cls.get_many_base_query(dbSession, cls)
                    .filter(*args, **kwargs)
                    .all()
                )
            else:
                return cls.get_many_base_query(dbSession, cls).filter_by(**kwargs).all()

    def save(self):
        with self.get_databaseClass().getScopedSession() as dbSession:
            self.save_procedure(dbSession)
            return self

    def update(self):
        with self.get_databaseClass().getScopedSession() as dbSession:
            self.update_procedure(dbSession)
            return self

    def delete(self, method="soft"):
        with self.get_databaseClass().getScopedSession() as dbSession:
            if method == "hard":
                self.hard_delete_procedure(dbSession)
            else:
                self.soft_delete_procedure(dbSession)
            return self

    @classmethod
    def get_one_by_unique_field(self, model, field, value):
        with self.get_databaseClass().getScopedSession() as dbSession:
            return dbSession.query(model).filter_by(**{field: value})

    @classmethod
    def get_one_base_query(self, dbSession: Session, model):
        return dbSession.query(model).filter(model._deleted != True)

    @classmethod
    def get_many_base_query(self, dbSession: Session, model):
        return dbSession.query(model).filter(model._deleted != True)

    def save_procedure(self, dbSession: Session):
        dbSession.add(self)
        dbSession.commit()
        dbSession.refresh(self)

    def update_procedure(self, dbSession: Session):
        dbSession.merge(self)
        dbSession.commit()

    def hard_delete_procedure(self, dbSession: Session):
        dbSession.delete(self)
        dbSession.commit()

    def soft_delete_procedure(self, dbSession: Session):
        self._deleted = True
        dbSession.merge(self)
        dbSession.commit()

    """
    # if needed, model can be self updated by merging after making the changes
    # like the example below:

    def selfChangeData(self, *args, **kwargs):
        with self.get_databaseClass().getScopedSession() as dbSession: # Start the session within scope
            self.login = 'updatedFromBaseModel' # Change the data as you want
            dbSession.merge(self) # Merge to the new session
            dbSession.commit() # Commit the changes
            # After that, any changes will not be stored even if commited.
            return 'ok'
    """
