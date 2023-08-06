import ssl
import socket

class SSLServer:
    def __init__(self, host, port, certfile, keyfile):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        
    def start(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            
            while True:
                conn, addr = server_socket.accept()
                conn_ssl = context.wrap_socket(conn, server_side=True)
                
                # Do something with conn_ssl
                data = conn_ssl.recv(1024)
                conn_ssl.sendall(b"Hello, client!")
                conn_ssl.close()

class SSLClient:
    def __init__(self, host, port, certfile):
        self.host = host
        self.port = port
        self.certfile = certfile
        
    def connect(self):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(cafile=self.certfile)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            conn_ssl = context.wrap_socket(client_socket, server_hostname=self.host)
            conn_ssl.connect((self.host, self.port))
            
            # Do something with conn_ssl
            conn_ssl.sendall(b"Hello, server!")
            data = conn_ssl.recv(1024)
            conn_ssl.close()
