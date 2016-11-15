import socket
import errno
from constant import CONFIG
from constant import ERRORS

class RECEIVER:
    def receive(self):
        try:
            data, client_address = self.socket.recvfrom(
                                                int(CONFIG.packet_size))
            return [data, client_address]
        except socket.timeout:
            return False

    def send(self, data):
        try:
            self.socket.send(data)
        except socket.timeout:
            return False
        except socket.error, e:
            if e[0] == errno.EPIPE:
                print ERRORS.client_pipe_down
            else:
                print ERRORS.unknown_socket_error
        return

    def close(self):
        self.socket.close()
        return

    def add_connection(self, conn):
        self.socket = conn
        self.socket.settimeout(float(CONFIG.keep_alive_time))

    def connect(self, ip, port):
        self.socket.connect((ip, int(port)))

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return

class LISTENER:
    def accept(self):
        try:
            self.socket.listen(int(CONFIG.max_connections))
            (clientsocket, (ip, port)) = self.socket.accept()
            return [clientsocket, ip, port]
        except socket.timeout:
            return False

    def close(self):
        self.socket.close()

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if (CONFIG.port != 0):
            self.socket.bind((CONFIG.ip_address, int(CONFIG.port)))
            self.socket.settimeout(None)
        return
