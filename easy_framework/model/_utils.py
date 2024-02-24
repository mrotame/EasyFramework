from __future__ import annotations
import typing as t
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
    from ._baseModelMongo import BaseModelMongo
    from ._baseModelSql import BaseModelSql

class ModelConstructor(ABC):
    __remove_fields = []
    
    class Meta(ABC):
        pass

    @property
    @abstractmethod
    def __model__(self)-> t.Union[BaseModelSql, BaseModelMongo]:
        pass

    def __new__(cls):  
        fields = cls._get_attributes(cls)
        item = cls.__model__(**fields)
        return item
    
    def _get_attributes(self):
        fields_value = {}

        for i in self.Meta.__dict__:
            if i in self.__remove_fields:
                continue
            
            if i.startswith('__'):
                continue

            fields_value[i] = self.Meta.__dict__[i]

        return fields_value