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

class GetValues(Request):

    def __init__(self, data):
        self.data = data

        self.method = 'get'
        self.uri_path = f'/users'

    def get_query_parameters(self):
        return self.data
