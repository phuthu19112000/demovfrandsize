import json
import requests
from fastapi import HTTPException
#from client_api.api_requests import *
from recom_client_api.exceptions import ApiTimeoutException, ResponseException
from fastapi import status
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


class Client:

    def __init__(self, protocol='http://', base_uri='192.168.50.69:5849/ping'):
        self.protocol = protocol
        self.base_uri = base_uri

    def send(self, request):
        timeout = request.timeout   
        uri = self.__process_request_uri(request)

        try:
            method = getattr(self, f'_{request.method}')
            print(method)
            response = method(request, uri, timeout)
            return response
        except requests.exceptions.Timeout:
            return HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as e:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = e)

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
