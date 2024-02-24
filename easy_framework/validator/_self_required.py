import typing as t
from flask import request, current_app
from easy_framework.user import current_user
from easy_framework.validator import BaseValidator
from easy_framework.validator import Login_required
from easy_framework.user import current_user
from easy_framework.exception import NotTheOwner
class Self_required(BaseValidator):
    '''
    Validate if the user is the owner of the data that he is accessing
    by checking the model's `_owner_id` field
    '''

    def validate(self):
        if request.method == 'GET': self.request_data = request.args
        else: self.request_data = request.get_json()

        Login_required(self.view)

        if not self.view.field_lookup_value:
            return
        
        self.check_field_lookup()
        self.check_owner()

    def check_request_method(self, methods_to_validate: t.List[str]):
        if request.method.lower() in [i.lower() for i in methods_to_validate]:
            return True

    def check_field_lookup(self):
        
        if self.view.field_lookup not in self.request_data and request.method != 'POST':
            return NotTheOwner()

    def check_owner(self):
        if self.view.model.get_one(_owner_id = current_user.id, **{self.view.field_lookup:self.view.field_lookup_value}) is None:
            raise NotTheOwner()