from marshmallow_sqlalchemy import SQLAlchemySchema

from copper_rabbit.settings.globe import session


# class BaseSchema(SQLAlchemySchema):
#     class Meta:
#         sqla_session = session


from marshmallow_sqlalchemy import SQLAlchemySchemaOpts, SQLAlchemySchema
# from .db import Session


class BaseOpts(SQLAlchemySchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = session
        super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemySchema):
    OPTIONS_CLASS = BaseOpts


