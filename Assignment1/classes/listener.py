import socket
from constant import CONSTANT

class LISTENER:
    def start(self):
        while 1:
            data, client_address = self.socket.recvfrom(CONSTANT.packet_size)
            print data
            if (self.handle_command(data, client_address) == False):
                self.socket.close()
                return
    def handle_command(self, command, client_address):
        clist = command.split()
        if len(clist) > 1:
            print "put/get"
        elif command == "list":
            print "list"
        elif command == "exit":
            self.socket.sendto("ack", client_address)
            return False
        return True
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", port))
        return
