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

    @property
    def class_name(self):
        '''
            Get this BaseSchema's class_name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-16-2023 07:40:50
            `@memberOf`: BaseSchema
            `@property`: class_name
        '''
        return self.__class__.__name__


