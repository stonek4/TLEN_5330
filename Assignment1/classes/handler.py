import socket
from constant import CONSTANT
from receiver import RECEIVER
from sender import SENDER

class CLIENT_HANDLER:
    def put(self, file_name):
        self.sender.send_message("put" + " " + file_name)
        if(self.receiver.receive(5) == False):
            print "No server response"
            return False
        try:
            afile = open("Client_Files/" + file_name, "rb")
        except:
            print "Couldn't open file"
            return False
        send_file(afile, self.sender, self.receiver)

    def get(self, file_name):
        self.sender.send_message("get" + " " + file_name)
        if(self.receiver.receive(5) == False):
            print "No server response"
            return False
        try:
            afile = open("Client_Files/" + file_name, "wb")
        except:
            print "Couldn't open file"
            return False
        receive_file(afile, self.sender, self.receiver)

    def start(self):
        while 1:
            data = raw_input()
            inputs = data.split()
            if len(inputs) > 1:
                if inputs[0] == "get":
                    self.get(inputs[1])
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
    def put(self, file_name, sender):
        try:
            afile = open("Server_Files/"+file_name, "wb")
        except:
            print "couldn't open file"
            return False
        receive_file(afile, sender, self.receiver)

    def get(self, file_name, sender):
        try:
            afile = open("Server_Files/"+file_name, "rb")
        except:
            print "couldn't open file"
            return False
        send_file(afile, sender, self.receiver)

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
                    self.put(inputs[1], sender)
                elif (inputs[0] == "get"):
                    self.get(inputs[1], sender)
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


def send_file(afile, sender, receiver):
    packet = afile.read(CONSTANT.packet_size)
    except_count = 0
    print "Sending file"
    while packet:
        if (except_count > 5):
            print "Gave up on sending file after multiple timeouts."
            return False
        sender.send_message(packet)
        if (receiver.receive(5)):
            packet = afile.read(CONSTANT.packet_size)
        else:
            print "Packet failed to send, retrying..."
            except_count += 1
    print "Finished sending file"
    sender.send_message("$$$done$$$")
    receiver.receive(5)

def receive_file(afile, sender, receiver):
    print "Receiving file"
    except_count = 0
    while 1:
        if (except_count > 5):
            print "Gave up on receiving file after multiple timeouts."
            return False
        output = receiver.receive(5)
        if(output):
            if (output[0] == "$$$done$$$"):
                sender.send_ack()
                break
            afile.write(output[0])
            sender.send_ack()
        else:
            print "Timed out, re-waiting"
            except_count += 1
    print "Finished receiving file"
