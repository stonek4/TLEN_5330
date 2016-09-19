import socket

class SENDER:
    def send(self, message, host, port):
        self.socket.sendto(message, (host, port))
    def __init__(self, bytes):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.max_bytes = bytes
        return
