import xmlrpc.server
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RemoteExecutor:
    def __init__(self, address='localhost', port=8000):
        self.address = address
        self.port = port

    def _execute_function(self, module_name, function_name, *args, **kwargs):
        module = __import__(module_name)
        function = getattr(module, function_name)
        return function(*args, **kwargs)

    def serve(self):
        class RequestHandler(SimpleXMLRPCRequestHandler):
            rpc_paths = ('/RPC2',)

        server = SimpleXMLRPCServer((self.address, self.port), requestHandler=RequestHandler)
        server.register_introspection_functions()
        server.register_function(self._execute_function, 'execute_function')

        print(f"Serving on {self.address}:{self.port}")
        server.serve_forever()

