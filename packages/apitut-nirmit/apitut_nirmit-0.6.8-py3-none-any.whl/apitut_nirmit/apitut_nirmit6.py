# Import necessary modules
import xmlrpc.server
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RemoteExecutor:
    """
    RemoteExecutor class that allows remote execution of functions from a specified module.
    """
    def __init__(self, address='localhost', port=8000):
        """
        Initializes a RemoteExecutor object.

        :param address: (optional) IP address or hostname to bind the server to. Defaults to 'localhost'.
        :param port: (optional) Port number to bind the server to. Defaults to 8000.
        """
        self.address = address
        self.port = port

    def _execute_function(self, module_name, function_name, *args, **kwargs):
        """
        Internal method that executes a function from a specified module.

        :param module_name: Name of the module that contains the function to execute.
        :param function_name: Name of the function to execute.
        :param args: (optional) Positional arguments to pass to the function.
        :param kwargs: (optional) Keyword arguments to pass to the function.
        :return: The return value of the executed function.
        """
        # Import the module dynamically
        module = __import__(module_name)
        # Get the function from the module
        function = getattr(module, function_name)
        # Call the function with the given arguments
        return function(*args, **kwargs)

    def serve(self):
        """
        Method that starts the XML-RPC server and serves requests indefinitely.
        """
        # Define a custom request handler that restricts the RPC paths to '/RPC2'
        class RequestHandler(SimpleXMLRPCRequestHandler):
            rpc_paths = ('/RPC2',)

        # Create a server instance with the specified address, port and request handler
        server = SimpleXMLRPCServer((self.address, self.port), requestHandler=RequestHandler)
        # Register the introspection functions to allow clients to get information about the server
        server.register_introspection_functions()
        # Register the '_execute_function' method as an XML-RPC function with the name 'execute_function'
        server.register_function(self._execute_function, 'execute_function')

        # Start serving requests and print a message indicating the server is running
        print(f"Serving on {self.address}:{self.port}")
        server.serve_forever()

