import socket

class SENDER:
    def send_message(self, message):
        self.socket.sendto(message, (self.host, self.port))
    def send_ack(self):
        self.socket.sendto("ACK", (self.host, self.port))
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        return
