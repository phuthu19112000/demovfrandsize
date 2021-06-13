from recom_client_api.api_requests.user_properties_api import AddUserProperty
from recom_client_api.api_requests.base_request import Request

class AddItemProperty(Request):

    def __init__(self, property_name, dtype) -> None:
        super(AddItemProperty, self).__init__()

        self.property_name = property_name
        self.dtype = dtype

        self.method = "put"
        self.uri_path = f"/items/properties/{self.property_name}"

    def get_body_parameters(self):
        params = dict()
        return params
    
    def get_query_parameters(self):
        params = dict()
        return params
    
class GetItemPropertyInfo(Request):

    def __init__(self, property_name) -> None:
        self.property_name = property_name

        self.method = "get"
        self.uri_path = f"/items/properties/{self.property_name}"
    
    def get_body_parameters(self):
        params = dict()
        return params
    
    def get_query_parameters(self):
        params = dict()
        return params
    