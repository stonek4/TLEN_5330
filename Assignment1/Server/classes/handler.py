import socket
import os
from constant import CONSTANT
from receiver import RECEIVER
from sender import SENDER

class SERVER_HANDLER:
    def put(self, file_name, sender):
        try:
            afile = open(CONSTANT.server_file_location+"/"+file_name, "wb")
        except:
            print CONSTANT.file_error
            return False
        receive_file(afile, sender, self.receiver)

    def get(self, file_name, sender):
        try:
            afile = open(CONSTANT.server_file_location+"/"+file_name, "rb")
        except:
            print CONSTANT.file_error
            sender.send_message(CONSTANT.file_error)
            return False
        send_file(afile, sender, self.receiver)

    def list(self, sender):
        all_files = ""
        for afile in os.listdir(CONSTANT.server_file_location):
            all_files = all_files + afile + " "
        sender.send_message(all_files)

    def exit(self):
        self.socket.close()

    def start(self):
        while 1:
            data = self.receiver.receive(1000)
            inputs = data[0].split()
            sender = SENDER(data[1][0], data[1][1])
            sender.send_ack()
            if len(inputs) > 1:
                if (inputs[0] == CONSTANT.put_cmd):
                    self.put(inputs[1], sender)
                elif (inputs[0] == CONSTANT.get_cmd):
                    self.get(inputs[1], sender)
                else:
                    sender.send_message(data[0] + CONSTANT.unknown_cmd)
            elif data[0] == CONSTANT.list_cmd:
                self.list(sender)
            elif data[0] == CONSTANT.exit_cmd:
                self.exit()
                break
            elif data[0] == CONSTANT.ack:
                print data[1][0] + CONSTANT.connected
            else:
                sender.send_message(data[0] + CONSTANT.unknown_cmd)
            print ""
        return True
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(5)
        self.receiver = RECEIVER(port)
        return

def send_file(afile, sender, receiver):
    packet = afile.read(CONSTANT.packet_size)
    except_count = 0
    print CONSTANT.sending_file
    while packet:
        if (except_count > 5):
            print CONSTANT.timeout_failure
            return False
        sender.send_message(packet)
        if (receiver.receive(5)):
            packet = afile.read(CONSTANT.packet_size)
        else:
            print CONSTANT.retrying
            except_count += 1
    print CONSTANT.finished_sending_file
    sender.send_message(CONSTANT.escape_code)
    receiver.receive(5)

def receive_file(afile, sender, receiver):
    print CONSTANT.receiving_file
    except_count = 0
    while 1:
        if (except_count > 5):
            print CONSTANT.timeout_failure
            return False
        output = receiver.receive(5)
        if(output):
            if (output[0] == CONSTANT.escape_code):
                sender.send_ack()
                break
            elif (output[0] == CONSTANT.file_error):
                print "Server: " + CONSTANT.file_error
                os.remove(afile.name)
                return False
            afile.write(output[0])
            sender.send_ack()
        else:
            print CONSTANT.retrying
            except_count += 1
    print CONSTANT.finished_receiving_file
