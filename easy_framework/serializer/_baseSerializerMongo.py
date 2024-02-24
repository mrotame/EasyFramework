from easy_framework.serializer import BaseSerializerSql
from marshmallow import fields


class BaseSerializerMongo(BaseSerializerSql):
    id = fields.String()