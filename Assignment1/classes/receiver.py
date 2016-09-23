import socket
from constant import CONSTANT

class RECEIVER:
    def receive(self, time):
        self.socket.settimeout(time)
        try:
            data, client_address = self.socket.recvfrom(CONSTANT.packet_size)
            return [data, client_address]
        except:
            print "didn't receive"
            return False
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if (port != -1):
            self.socket.bind(("", port))
        return
