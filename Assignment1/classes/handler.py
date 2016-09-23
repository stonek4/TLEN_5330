import socket
from constant import CONSTANT
from receiver import RECEIVER
from sender import SENDER

class CLIENT_HANDLER:
    def put(self, file_name):
        self.sender.send_message("put" + " " + file_name)
        self.receiver.receive(5)
        try:
            afile = open("Client_Files/" + file_name, "rb")
        except:
            print "Couldn't open file"
            return False
        print "Beginning to send file"
        packet = afile.read(CONSTANT.packet_size)
        except_count = 0
        while packet:
            if (except_count > 5):
                print "gave up on sending file"
                break
            self.sender.send_message(packet)
            try:
                self.receiver.receive(5)
                packet = afile.read(CONSTANT.packet_size)
            except socket.timeout:
                print "Packet failed to send, retrying..."
                except_count += 1
        print "Finished sending file"
        self.sender.send_message("$$$done$$$")
    def start(self):
        while 1:
            data = raw_input()
            inputs = data.split()
            if len(inputs) > 1:
                if inputs[0] == "get":
                    print "get"
                elif inputs[0] == "put":
                    self.put(inputs[1])
            elif data == "list":
                print "list"
            elif data == "exit":
                self.sender.send_message("exit")
    def __init__(self, host, port):
        self.sender = SENDER(host, port)
        self.receiver = RECEIVER(-1)
        self.receiver.socket = self.sender.socket
        return

class SERVER_HANDLER:
    def put(self, file_name):
        try:
            afile = open("Server_Files/"+file_name, "wb")
        except:
            print "couldn't open file"
            return False
        while 1:
            try:
                output = self.receiver.receive(5)
                sender = SENDER(output[1][0], output[1][1])
                if (output[0] == "$$$done$$$"):
                    sender.send_ack()
                    break
                afile.write(output[0])
                sender.send_ack()
            except socket.timeout:
                print "timed out"
                return False
    def exit(self):
        self.socket.close()
    def start(self):
        while 1:
            data = self.receiver.receive(1000)
            inputs = data[0].split()
            sender = SENDER(data[1][0], data[1][1])
            sender.send_ack()
            if len(inputs) > 1:
                if (inputs[0] == "put"):
                    self.put(inputs[1])
                elif (inputs[0] == "get"):
                    print "get"
            elif data[0] == "list":
                print "list"
            elif data[0] == "exit":
                self.exit()
                break
        return True
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(5)
        self.receiver = RECEIVER(port)
        return
