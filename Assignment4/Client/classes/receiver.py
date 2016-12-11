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

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(float(CONFIG.keep_alive_time))
            self.socket.connect((self.ip, self.port))
        except socket.error:
            self.connected = False
            return False
        self.connected = True
        return True

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.receive()
        self.socket.close()
        self.connected = False
        return

    def __init__(self, name, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.port = port
        self.ip = ip
        self.connected = False
        return
