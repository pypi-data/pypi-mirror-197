#!/usr/bin/env python

import cgi
import json

class MyAPI:
    def __init__(self):
        pass

    def handle_request(self, request):
        # Get the HTTP method and request parameters
        method = request["REQUEST_METHOD"]
        params = cgi.FieldStorage()

        # Handle different methods
        if method == "GET":
            # Handle GET requests here
            response = {"message": "This is a GET request"}
        elif method == "POST":
            # Handle POST requests here
            action = params.getvalue("action")
            if action == "add":
                try:
                    num1 = int(params.getvalue("num1"))
                    num2 = int(params.getvalue("num2"))
                    result = num1 + num2
                    response = {"result": result}
                except:
                    response = {"error": "Invalid input"}
            elif action == "subtract":
                try:
                    num1 = int(params.getvalue("num1"))
                    num2 = int(params.getvalue("num2"))
                    result = num1 - num2
                    response = {"result": result}
                except:
                    response = {"error": "Invalid input"}
            else:
                response = {"error": "Unsupported action"}
        elif method == "PUT":
            # Handle PUT requests here
            response = {"message": "This is a PUT request"}
        elif method == "DELETE":
            # Handle DELETE requests here
            response = {"message": "This is a DELETE request"}
        else:
            # Handle unsupported methods
            response = {"error": "Unsupported HTTP method"}

        self.send_response(response)

    def send_response(self, response):
        # Send response as JSON
        print("Content-Type: application/json")
        print()
        print(json.dumps(response))

if __name__ == "__main__":
    # Parse the incoming request and call the handler function
    api = MyAPI()
    request = cgi.FieldStorage()
    api.handle_request(request)

