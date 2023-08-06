#!/usr/bin/env python
import cgi
import json

def handle_request(environ, start_response):
    """
This script provides a simple HTTP API to perform various operations based on the HTTP method.

Supported HTTP Methods:
- GET
- POST
- PUT
- PATCH
- DELETE

Endpoints:
- For GET requests, returns a message indicating it's a GET request.
- For POST requests, supports two actions: add and subtract. The input values num1 and num2 are added or subtracted depending on the action provided.
- For PUT requests, returns a message indicating it's a PUT request.
- For DELETE requests, returns a message indicating it's a DELETE request.

Usage:
- Start the server with the command `python script_name.py`
- Send requests to `http://localhost:8000` with the desired HTTP method and endpoint.

Example Usage:
- GET: http://localhost:8000
- POST: http://localhost:8000?action=add&num1=5&num2=10
- PUT: http://localhost:8000
- DELETE: http://localhost:8000

    Handles the HTTP request based on the HTTP method and returns the response as a JSON object.

    Args:
        environ (dict): A dictionary containing CGI-like variables provided by the server.
        start_response (callable): A callback function that takes the HTTP status and headers.

    Returns:
        list: A list containing the response data as a JSON object encoded in UTF-8.
    """
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

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    # Create a simple server with the handle_request function
    httpd = make_server('', 8000, handle_request)
    print("Server started on port 8000...")
    # Serve until process is killed
    httpd.serve_forever()

