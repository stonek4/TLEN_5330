import socket
import errno
from constant import CONFIG
from constant import ERRORS
from constant import INFO

class RECEIVER:
    def receive(self):
        try:
            data, client_address = self.socket.recvfrom(
                                                int(CONFIG.packet_size))
            return [data, client_address]
        except socket.timeout:
            return False
        except socket.error:
            print INFO.client_disconnect
            return False

    def receive_data(self):
        self.socket.settimeout(3)
        data = self.receive()
        self.socket.settimeout(float(CONFIG.keep_alive_time))
        return data

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
        self.socket.shutdown(socket.SHUT_RDWR)
        self.receive()
        self.socket.close()
        return

    def __init__(self, conn):
        self.socket = conn
        self.socket.settimeout(float(CONFIG.keep_alive_time))
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
