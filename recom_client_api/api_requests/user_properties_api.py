from recom_client_api.api_requests.base_request import Request


class AddUserProperty(Request):
    
    def __init__(self, property_name, dtype):
        super(AddUserProperty, self).__init__()

        self.property_name = property_name
        self.dtype = dtype

        self.method = 'put'
        self.uri_path = f'/users/properties/{self.property_name}'

    def get_body_parameters(self):
        params = dict()
        return params

    def get_query_parameters(self):
        params = dict()
        params['dtype'] = self.dtype
        return params


class GetUserPropertyInfo(Request):

    def __init__(self, property_name):
        self.property_name = property_name

        self.method = 'get'
        self.uri_path = f'/users/properties/{self.property_name}'

    def get_body_parameters(self):
        params = dict()
        return params

    def get_query_parameters(self):
        params = dict()
        return params
