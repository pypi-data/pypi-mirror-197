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


class OrderStatus(BaseModel):
    def __init__(self):
        self.time_order_created = ""
        self.time_driver_assigned = ""
        self.time_driver_picked_up_food = ""
        self.time_driver_delivered_food = ""

    def init(self, **kwargs):
        for k, v in kwargs.items():
            if k == "time_order_created":
                self.time_order_created = v
            if k == "time_driver_assigned":
                self.time_driver_assigned = v
            if k == "time_driver_picked_up_food":
                self.time_driver_picked_up_food = v
            if k == "time_driver_delivered_food":
                self.time_driver_delivered_food = v

    def __str__(self):
        return f'driver_assigned={self.time_driver_delivered_food != ""}, ' \
               f'driver_picked_up_food={self.time_driver_picked_up_food != ""}, ' \
               f'driver_delivered_food={self.time_driver_delivered_food != ""}'


class Order(BaseModel):
    def __init__(self):
        self.id = ""
        self.customer_email = ""
        self.total_price = 0.0
        self.items = []
        self.status = OrderStatus()
        self.status.time_order_created = "1/1/2022(TODO)"

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
               f'status=({str(self.status)})'


class BaseOrderEvent:
    def __init__(self, order):
        self.order = order

    def __repr__(self):
        return json.dumps(self.__dict__, default=str)

    def __str__(self):
        return f'{self.order=}'


class OrderAdded(BaseOrderEvent):
    pass


class OrderRemoved(BaseOrderEvent):
    pass
