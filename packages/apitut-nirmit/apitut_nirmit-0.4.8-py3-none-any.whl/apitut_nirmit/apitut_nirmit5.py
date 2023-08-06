#!/usr/bin/env python

import cgi
import json

def handle_request(environ, start_response):
    # Get the HTTP method and request parameters
    method = environ.get("REQUEST_METHOD", "").upper()
    params = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

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

    # Send response as JSON
    headers = [("Content-Type", "application/json")]
    start_response("200 OK", headers)
    return [json.dumps(response).encode("utf-8")]

