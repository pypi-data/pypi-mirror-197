"""
for now, define this as a simple module. we could later make this into a class if necessary

this module has everything needed to represent Restaurant entity

attributes:
    name
    address
    cuisine_type
    rating
    status
"""

from qb_core.common.base_model import BaseModel


class Restaurant(BaseModel):

    def __init__(self):
        self.name = ""
        self.address = ""
        self.cuisine_type = ""
        self.rating = ""
        self.status = ""
        # for now, implement manager info right here
        self.manager_name = ""
        self.manager_email = ""
        self.verification_code = None
        self.verification_valid_till = None
        self.cook_dict = {}

    def init(self, **kwargs):
        for k, v in kwargs.items():
            if k == "name":
                self.name = v
            if k == "address":
                self.address = v
            if k == "cuisine_type":
                self.cuisine_type = v
            if k == "rating":
                self.rating = v
            if k == "status":
                self.status = v
            if k == "manager_name":
                self.manager_name = v
            if k == "manager_email":
                self.manager_email = v

    def __str__(self):
        return f'{self.name=}, {self.manager_name=}, {self.manager_email}'

    def save_verification_code(self, code):
        self.verification_code = code
        # NICE_TODO Feature - Security - set this to 2 days
        self.verification_valid_till = None
        self.status = "pending_verification"
