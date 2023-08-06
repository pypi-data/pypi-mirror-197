"""
tcp_server package
==================

This package provides an API for implementing a server that communicates with clients using the TCP Internet protocol.

Classes
-------
MyTCPHandler(BaseRequestHandler)
    The request handler class for the TCP server.
    
Functions
---------
start_server(host: str, port: int)
    Start the TCP server and listen for incoming connections.

Usage
-----
To start the TCP server, import the `start_server()` function and call it with the host address and port number to bind to.

Example:
    
    >>> from tcp_server import start_server
    >>> if __name__ == "__main__":
    >>>     start_server("localhost", 9999)
    
This will start the TCP server on `localhost` and port `9999`.
"""

import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        # send back the same message to the client
        self.request.sendall(data)

def start_server(host: str, port: int):
    """
    Start the TCP server and listen for incoming connections.
    
    Parameters
    ----------
    host : str
        The host address to bind to.
    port : int
        The port number to bind to.
    """
    with socketserver.TCPServer((host, port), MyTCPHandler) as server:
        print("Server running on {}:{}".format(host, port))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.shutdown()
            print("Server stopped.")

