"""
udp_server package
==================

This package provides an API for implementing a server that communicates with clients using the UDP Internet protocol.

Classes
-------
MyUDPHandler(DatagramRequestHandler)
    The request handler class for the UDP server.
    
Functions
---------
start_server(host: str, port: int)
    Start the UDP server and listen for incoming messages.

Usage
-----
To start the UDP server, import the `start_server()` function and call it with the host address and port number to bind to.

Example:
    
    >>> from udp_server import start_server
    >>> if __name__ == "__main__":
    >>>     start_server("localhost", 9999)
    
This will start the UDP server on `localhost` and port `9999`.
"""

import socketserver

class MyUDPHandler(socketserver.DatagramRequestHandler):
    """
    The request handler class for our server.
    """

    def handle(self):
        # self.request is the UDP socket connected to the client
        data, socket = self.request
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        # send back the same message to the client
        socket.sendto(data, self.client_address)

def start_server2(host: str, port: int):
    """
    Start the UDP server and listen for incoming messages.
    
    Parameters
    ----------
    host : str
        The host address to bind to.
    port : int
        The port number to bind to.
    """
    with socketserver.UDPServer((host, port), MyUDPHandler) as server:
        print("Server running on {}:{}".format(host, port))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.shutdown()
            print("Server stopped.")
