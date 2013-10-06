import socket
from ioloop import IOLoop
import ioloop

HOST = "127.0.0.1"
BACKLOG = 100

class HTTPServer():
    def __init__(self, request_callback):
        self.request_callback = request_callback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.io_loop = IOLoop.Instance()

    def listen(self, port):
        self.socket.bind((HOST, port))
        self.socket.listen(BACKLOG)
        add_accept_handler(self.socket, self._handle_connection, io_loop=self.io_loop)

    def _handle_connection(self, connection, address):
        print address, 'in'
        print connection.fileno()
        pass

def add_accept_handler(sock, call_back, io_loop=None):
    if io_loop is None:
        io_loop = IOLoop.instance()

    def accept_handler(fd, events):
        while True:
            try:
                connection, address = sock.accept()
            except Exception as e:
                break
            call_back(connection, address)

    io_loop.add_handler(sock.fileno(), accept_handler, ioloop._EPOLLIN)
