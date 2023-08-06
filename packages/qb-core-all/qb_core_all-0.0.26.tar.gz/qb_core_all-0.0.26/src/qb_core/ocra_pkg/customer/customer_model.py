import json

from qb_core.common.base_model import BaseModel


class Customer(BaseModel):

    def __init__(self):
        self.name = ""
        self.email = ""
        self.phone_number = ""
        self.address = ""
        self.card_info = ""

    def init(self, **kwargs):
        for k, v in kwargs.items():
            if k == "name":
                self.name = v
            if k == "email":
                self.email = v
            if k == "phone_number":
                self.phone_number = v
            if k == "address":
                self.address = v
            if k == "card_info":
                self.card_info = v

    def __str__(self):
        return f'{self.name=}, {self.email=}'


class BaseCustomerEvent:
    def __init__(self, customer):
        self.customer = customer

    def __repr__(self):
        return json.dumps(self.__dict__, default=str)

    def __str__(self):
        return f'{self.customer=}'


class CustomerAdded(BaseCustomerEvent):
    pass


class CustomerRemoved(BaseCustomerEvent):
    pass
