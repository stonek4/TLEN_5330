import socket
import os
from constant import CONSTANT
from receiver import RECEIVER
from sender import SENDER

class CLIENT_HANDLER:
    def put(self, file_name):
        try:
            afile = open(CONSTANT.client_file_location+"/" + file_name, "rb")
        except:
            print CONSTANT.file_error
            return False
        self.sender.send_message(CONSTANT.put_cmd + " " + file_name)
        if(self.receiver.receive(5) == False):
            print CONSTANT.no_server_response
            return False
        send_file(afile, self.sender, self.receiver)

    def get(self, file_name):
        self.sender.send_message(CONSTANT.get_cmd + " " + file_name)
        if(self.receiver.receive(5) == False):
            print CONSTANT.no_server_response
            return False
        try:
            afile = open(CONSTANT.client_file_location+"/" + CONSTANT.received + file_name, "wb")
        except:
            print CONSTANT.file_error
            return False
        receive_file(afile, self.sender, self.receiver)

    def list(self):
        self.sender.send_message(CONSTANT.list_cmd)
        if (self.receiver.receive(5) == False):
            print CONSTANT.no_server_response
            return

        files = self.receiver.receive(5)
        if (files):
            for afile in files[0].split():
                print afile
        else:
            print CONSTANT.no_server_response

    def exit(self):
        self.sender.send_message(CONSTANT.exit_cmd)

    def other(self, command):
        self.sender.send_message(command)
        if (self.receiver.receive(5)):
            output = self.receiver.receive(5)
            if (output):
                print output[0]
            else:
                print CONSTANT.no_server_response
        else:
            print CONSTANT.no_server_response

    def start(self):
        self.sender.send_ack()
        if (self.receiver.receive(5) == False):
            print CONSTANT.no_server_response_ping
        while 1:
            data = raw_input()
            inputs = data.split()
            if len(inputs) > 1:
                if inputs[0] == CONSTANT.get_cmd:
                    self.get(inputs[1])
                elif inputs[0] == CONSTANT.put_cmd:
                    self.put(inputs[1])
                else:
                    self.other(data)
            elif data == CONSTANT.list_cmd:
                self.list()
            elif data == CONSTANT.exit_cmd:
                self.exit()
            else:
                self.other(data)
            print ""
        return True

    def __init__(self, host, port):
        self.sender = SENDER(host, port)
        self.receiver = RECEIVER(-1)
        self.receiver.socket = self.sender.socket
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
