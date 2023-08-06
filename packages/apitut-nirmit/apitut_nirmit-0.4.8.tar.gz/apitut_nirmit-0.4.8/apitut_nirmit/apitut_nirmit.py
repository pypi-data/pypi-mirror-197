#API to access various services via HTTP as a client

import urllib.request
import json

class HttpApiClient:

    """
    HttpApiClient class provides a simple API to access various services via HTTP as a client. It can perform HTTP GET, POST, PUT, PATCH, and DELETE requests to the given endpoint.

    Example Usage:
    client = HttpApiClient("https://example.com/api/v1/")
    response = client.get("users/")
    print(response)

    Attributes:
    base_url (str): Base URL for all requests.
    auth_token (str): Authorization token to be used in the header of the request.

    Methods:
    _build_request(endpoint, method, data):
    Private method that constructs a urllib.request.Request object with the given endpoint, HTTP method, and data (if provided).
    get(endpoint):
    Sends an HTTP GET request to the given endpoint and returns the response data as a JSON object.

    post(endpoint, data):
    Sends an HTTP POST request to the given endpoint with the provided data and returns the response data as a JSON object.

    put(endpoint, data):
    Sends an HTTP PUT request to the given endpoint with the provided data and returns the response data as a JSON object.

    patch(endpoint, data):
    Sends an HTTP PATCH request to the given endpoint with the provided data and returns the response data as a JSON object.

    delete(endpoint):
    Sends an HTTP DELETE request to the given endpoint and returns the response data as a JSON object.
    """

    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token

    def _build_request(self, endpoint, method="GET", data=None):
        url = self.base_url + endpoint
        headers = {}

        if self.auth_token:
            headers["Authorization"] = "Bearer " + self.auth_token

        if method in ["POST", "PUT", "PATCH"]:
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(url, headers=headers, method=method)

        if data:
            data = json.dumps(data).encode("utf-8")
            request.data = data

        return request

    def get(self, endpoint):
        request = self._build_request(endpoint, method="GET")
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode("utf-8"))

    def post(self, endpoint, data):
        request = self._build_request(endpoint, method="POST", data=data)
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode("utf-8"))

    def put(self, endpoint, data):
        request = self._build_request(endpoint, method="PUT", data=data)
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode("utf-8"))

    def patch(self, endpoint, data):
        request = self._build_request(endpoint, method="PATCH", data=data)
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode("utf-8"))

    def delete(self, endpoint):
        request = self._build_request(endpoint, method="DELETE")
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode("utf-8"))

