class Request:
    timeout = 1000

    def get_body_parameters(self):
        raise NotImplementedError

    def get_query_parameters(self):
        raise NotImplementedError
