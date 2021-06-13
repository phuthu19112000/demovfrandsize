import json
from recom_client_api.api_requests.user_api import AddUser
import requests
from recom_client_api.api_requests.base_request import Request

class AddItem(Request):
    def __init__(self, data) :
        super(AddItem, self).__init__()

        self.data = data
        self.method = "post"
        self.uri_path = f"/items/"

    def get_body_parameters(self):
        return self.data

class GetItemValues(Request):
    
    def __init__(self, item_id) -> None:
        self.item_id = item_id

        self.method = "get"
        self.uri_path = f"/items/{self.item_id}"
    
    def get_body_parameters(self):
        return {}
    
    def get_query_parameters(self):
        return {}

