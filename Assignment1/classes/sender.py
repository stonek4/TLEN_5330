import socket
from constant import CONSTANT

class SENDER:
    def handle_command(self, command, host, port):
        inputs = command.split()
        if len(inputs) > 1:
            if inputs[0] == "get":
                print "get"
            elif inputs[0] == "put":
                try:
                    if(self.send_command(command, host, port)):
                        afile = f.open(inputs[1], "rb")
                        self.send_data(afile, host, port)
                except:
                    print "Could not read file"
        elif command == "list":
            self.send_command(command, host, port)
    def send_command(self, command, host, port):
        if (self.socket.sendto(command, (host, port))):
            try:
                ack, host_address = self.socket.recvfrom(CONSTANT.packet_size)
                return ack
            except socket.timeout:
                print "Command failed to send."
                return False
    def send_data(self, data, host, port):
        packet = data.read(CONSTANT.packet_size)
        print "Beginning to send file"
        while packet:
            if (self.socket.sendto(packet, (host, port))):
                try:
                    ack, host_address = self.socket.recvfrom(CONSTANT.packet_size)
                    packet = data.read(CONSTANT.packet_size)
                except socket.timeout:
                    print "Packet failed to send, retrying..."
        print "Finished sending file"
    def send_message(self, message, host, port):
        self.socket.sendto(message, (host, port))
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(5)
        return
