import json
import requests

from recom_client_api.api_requests.base_request import Request


class AddUser(Request):
    def __init__(self, data):
        super(AddUser, self).__init__()

        self.data = data
        self.method = 'post'
        self.uri_path = f'/users/'

    def get_body_parameters(self):

        return self.data

class GetUserValues(Request):

    def __init__(self, user_id):
        self.user_id = user_id

        self.method = 'get'
        self.uri_path = f'/users/{self.user_id}'

    def get_query_parameters(self):
        return self.param
