import socket

class LISTENER:
    def start(self):
        while 1:
            data, client_address = self.socket.recvfrom(self.max_bytes)
            print data
    def __init__(self, port, bytes):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", port))
        self.max_bytes = bytes
        return
