import json

from qb_core.common.base_model import BaseModel


class Cook(BaseModel):

    def __init__(self):
        self.name = ""
        self.email = ""

    def init(self, **kwargs):
        for k, v in kwargs.items():
            if k == "name":
                self.name = v
            if k == "email":
                self.email = v

    def __str__(self):
        return f'{self.name=}, {self.email=}'


class BaseCookEvent:
    def __init__(self, cook):
        self.cook = cook

    def __repr__(self):
        return json.dumps(self.__dict__, default=str)

    def __str__(self):
        return f'{self.cook=}'


class CookAdded(BaseCookEvent):
    pass


class CookRemoved(BaseCookEvent):
    pass
