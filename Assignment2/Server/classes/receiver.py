import socket
from constant import CONSTANT

class RECEIVER:
    def receive(self):
        try:
            data, client_address = self.socket.recvfrom(
                                                int(CONSTANT.packet_size))
            return [data, client_address]
        except socket.timeout:
            print "Timed out, didn't receive packet."
            return False

    def send(self, data):
        try:
            self.socket.send(data)
        except socket.timeout:
            return False
        return

    def close(self):
        self.socket.close()
        return

    def __init__(self, conn):
        self.socket = conn
        self.socket.settimeout(float(CONSTANT.keep_alive_time))
        return

class LISTENER:
    def accept(self):
        try:
            (clientsocket, (ip, port)) = self.socket.accept()
            return [clientsocket, ip, port]
        except socket.timeout:
            print "Timed out, didn't receive packet."
            return False

    def close(self):
        self.socket.close()

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if (CONSTANT.port != 0):
            self.socket.bind((CONSTANT.ip_address, int(CONSTANT.port)))
            self.socket.listen(int(CONSTANT.max_connections))
            self.socket.settimeout(float(CONSTANT.stay_awake))
        return
