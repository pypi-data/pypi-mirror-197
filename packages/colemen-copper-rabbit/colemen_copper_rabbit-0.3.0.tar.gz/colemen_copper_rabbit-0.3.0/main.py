# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import json
from typing import Union
import colemen_utils as _c
import copper_rabbit.settings as _settings

import copper_rabbit.models as _models
import copper_rabbit.schemas as _schemas
import copper_rabbit.actions as act




_settings.globe.base.metadata.create_all(_settings.globe._engine)

# class Main:
#     def __init__(self):
#         self.settings = {}
#         _settings.globe.base.metadata.create_all(_settings.globe._engine)
#         # self.prep()
#         # self.set_defaults()

#     # def set_defaults(self):
#     #     self.settings = c.file.import_project_settings("copper_rabbit.settings.json")

#     def master(self):
#         print("master")



#     # def prep(self):
#     #     # c.file.delete(f"{os.getcwd()}/{_settings.control.db_file_name}")
#     #     self.engine = _create_engine(f"sqlite:///test.db")

#     #     Session = _sessionmaker(bind=self.engine)
#     #     session = Session()

#     #     _settings.globe.session = session
#     #     _settings.globe.base.metadata.create_all(self.engine)

#     # def new_request(self,data):

#     #     rs:_models.Request = _schemas.requests.CreateRequestSchema().load(data)
#     #     # print(rs)

#     #     # data = rs.dump(rs)
#     #     # rs = _schemas.requests.CreateRequestSchema().make_instance(data)

#     #     _settings.globe.session.add(rs)
#     #     _settings.globe.session.commit()

#     # def get_requests(self):
#     #     result = _settings.globe.session.query(_models.Request).all()
#     #     out = []
#     #     for r in result:
#     #         rs = _schemas.requests.PublicRequestSchema().dump(r)
#     #         out.append(rs)
#     #     return out

#     # def update_request(self,data):
#     #     # @Mstep [] load the model from the data provided.
#     #     rqst = _schemas.requests.UpdateRequestSchema().load(data)
#     #     # @Mstep [] add the model again, which will cause an update because the id is provided.
#     #     _settings.globe.session.add(rqst)
#     #     # @Mstep [] commit the changes.
#     #     _settings.globe.session.commit()

#     # def soft_delete_request(self,data):
#     #     # @Mstep [] load the model from the data provided.
#     #     rqst = _schemas.requests.SoftDeleteRequestSchema().load(data)
#     #     # @Mstep [] add the model again, which will cause an update because the id is provided.
#     #     _settings.globe.session.add(rqst)
#     #     # @Mstep [] commit the changes.
#     #     _settings.globe.session.commit()

#     # def undo_soft_delete_request(self,data):
#     #     # @Mstep [] load the model from the data provided.
#     #     rqst = _schemas.requests.SoftDeleteRequestSchema().load(data)
#     #     # @Mstep [] add the model again, which will cause an update because the id is provided.
#     #     _settings.globe.session.add(rqst)
#     #     # @Mstep [] commit the changes.
#     #     _settings.globe.session.commit()

#     # def delete_request(self,data):
#     #     # @Mstep [] load the model from the data provided.
#     #     rqst = _schemas.requests.DeleteRequestSchema().load(data)
#     #     # @Mstep [] add the model again, which will cause an update because the id is provided.
#     #     _settings.globe.session.delete(rqst)
#     #     # @Mstep [] commit the changes.
#     #     _settings.globe.session.commit()



# if __name__ == '__main__':
#     m = Main()
#     # m.master()
    

