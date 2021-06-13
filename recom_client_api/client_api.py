import json
import requests

#from client_api.api_requests import *
from recom_client_api.exceptions import ApiTimeoutException

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


class Client:

    def __init__(self, protocol='http://', base_uri='192.168.50.69:5849'):
        self.protocol = protocol
        self.base_uri = base_uri

    def send(self, request):
        timeout = request.timeout
        uri = self.__process_request_uri(request)

        try:
            method = getattr(self, f'_{request.method}')
            print(uri)
            return method(request, uri, timeout)
        except requests.exceptions.Timeout:
            raise ApiTimeoutException(request)

    def _get(self, request, uri, timeout):
        response = requests.get(uri,
                                headers=self.__get_http_headers(),
                                timeout=timeout)
        return response

    def __get_http_headers(self):
        return {'Content-Type': 'application/json'}

    def __process_request_uri(self, request):
        uri = self.protocol + self.base_uri

        if request.method == "post":
            uri += request.uri_path

        if request.method == "post":
            return uri
        else:
            uri += self.__query_parameters_to_url(request)
            return uri

    def __query_parameters_to_url(self, request):
        def _format_value(value):
            if isinstance(value, list):
                return ','.join([quote(str(v)) for v in value])
            return quote(str(value))

        ps = ''
        query_params = request.get_query_parameters()
        for key, value in query_params.items():
            value = _format_value(value)
            ps += '&' if (ps!='') else '?'
            ps += '%s=%s' % (key, value)
        return ps
