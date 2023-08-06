import socket
import ssl


class SSLServer:
    """
    Provides an SSL server that can receive and respond to client requests.
    """
    
    def __init__(self, address, port, certfile, keyfile, cafile=None):
        """
        Initializes the SSL server with the specified address, port, certificate file, key file, and CA file (optional).
        :param address: The IP address of the server.
        :param port: The port number to listen on.
        :param certfile: The path to the server's SSL certificate file.
        :param keyfile: The path to the server's SSL key file.
        :param cafile: The path to the CA file used to validate client certificates (optional).
        """
        self.address = address
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.cafile = cafile
        
    def start(self):
        """
        Starts the SSL server and listens for incoming client connections.
        """
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        if self.cafile:
            context.load_verify_locations(cafile=self.cafile)
            context.verify_mode = ssl.CERT_REQUIRED
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.address, self.port))
            server_socket.listen()
            with context.wrap_socket(server_socket, server_side=True) as ssl_socket:
                print(f"SSL server started on {self.address}:{self.port}")
                while True:
                    client_socket, client_address = ssl_socket.accept()
                    print(f"Connection from {client_address}")
                    client_socket.close()  # TODO: implement client handling logic
                    
                    
class SSLClient:
    """
    Provides an SSL client that can connect to an SSL server and send requests.
    """
    
    def __init__(self, address, port, certfile, keyfile, cafile=None):
        """
        Initializes the SSL client with the specified address, port, certificate file, key file, and CA file (optional).
        :param address: The IP address of the server.
        :param port: The port number to connect to.
        :param certfile: The path to the client's SSL certificate file.
        :param keyfile: The path to the client's SSL key file.
        :param cafile: The path to the CA file used to validate server certificates (optional).
        """
        self.address = address
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.cafile = cafile
        
    def connect(self):
        """
        Connects the SSL client to the SSL server.
        """
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        if self.cafile:
            context.load_verify_locations(cafile=self.cafile)
            context.verify_mode = ssl.CERT_REQUIRED
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            with context.wrap_socket(client_socket, server_hostname=self.address) as ssl_socket:
                ssl_socket.sendall(b"Hello, server!")
                response = ssl_socket.recv(1024)
                print(f"Server response: {response.decode()}")

