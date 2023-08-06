"""
this is a base class for all model classes used in this application
"""
import json


class BaseModel:
    def __repr__(self):
        return json.dumps(self.__dict__, default=str)
