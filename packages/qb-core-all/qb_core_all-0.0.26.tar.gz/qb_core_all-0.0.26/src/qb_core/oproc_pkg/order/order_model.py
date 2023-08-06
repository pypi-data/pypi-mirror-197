import json

from qb_core.common.base_model import BaseModel


class OrderItem(BaseModel):
    def __init__(self):
        self.item_name = ""
        self.quantity = 0
        self.price = 0.0
        self.special_instruction = ""

    def init(self, **kwargs):
        for k, v in kwargs.items():
            if k == "item_name":
                self.item_name = v
            if k == "quantity":
                self.quantity = v
            if k == "price":
                self.price = v
            if k == "special_instruction":
                self.special_instruction = v

    def __str__(self):
        return f'{self.item_name=}, {self.quantity=}'


class CookAssignment(BaseModel):
    def __init__(self):
        self.cook_name = ""
        self.cook_email = ""
        self.time_cook_picked_up = ""
        self.time_cook_completed = ""

    def init(self, **kwargs):
        for k, v in kwargs.items():
            if k == "cook_name":
                self.cook_name = v
            if k == "cook_email":
                self.cook_email = v
            if k == "time_cook_picked_up":
                self.time_cook_picked_up = v
            if k == "time_cook_completed":
                self.time_cook_completed = v

    def __str__(self):
        return f'cook_name={self.cook_name}, ' \
               f'cook_picked_up={self.time_cook_picked_up != ""}, ' \
               f'cook_completed={self.time_cook_completed != ""}'


class Order(BaseModel):
    def __init__(self):
        self.id = ""
        self.customer_email = ""
        self.total_price = 0.0
        self.items = []
        self.cook_assignment = None

    def init(self, **kwargs):
        for k, v in kwargs.items():
            if k == "total_price":
                self.total_price = v
            if k == "items":
                self.items = v
            if k == "id":
                self.id = v

    def __str__(self):
        return f'customer_email={self.customer_email}, ' \
               f'total_price={self.total_price}, ' \
               f'number_of_items={len(self.items)} ' \
               f'cook_assignment=({str(self.cook_assignment)})'


class BaseOrderEvent:
    def __init__(self, order):
        self.order = order

    def __repr__(self):
        return json.dumps(self.__dict__, default=str)

    def __str__(self):
        return f'{self.order=}'


class OrderReadyForPickup(BaseOrderEvent):
    pass


class OrderInProgress(BaseOrderEvent):
    pass
