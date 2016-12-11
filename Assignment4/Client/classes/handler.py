import os
import math
from constant import CONFIG
from constant import PATHS
from constant import ERRORS
from constant import INFO
from constant import PARTS
from receiver import RECEIVER



class CONNECTION_HANDLER:
    # send the file to the client
    def send_file(self, sender, data):
        chunks = [data[x:x+100] for x in range(0, len(data), int(CONFIG.packet_size))]
        for chunk in chunks:
            sender.send(chunk)

    def recv_file(self, sender, afile):
        data = sender.receive()
        while (data):
            afile.write(data[0])
            data = sender.receive()
        afile.close()

    def list(self):
        return

    def get(self, file_name):
        return

    def put(self, file_name):
        try:
            afile = open(file_name, "rb")
            part_size = int(math.ceil(os.path.getsize(file_name)/len(CONFIG.servers)))
            data = afile.read(part_size)
            parts = []
            while(data):
                parts.append(data)
                data = afile.read(part_size)
            for receiver in self.receivers:
                file_name = os.path.basename(afile.name)
                needed = PARTS.get_parts(file_name, receiver.name)
                for need in needed:
                    receiver.connect()
                    if (receiver.connected):
                        if (need == 0):
                            need = 4
                        receiver.send("PUT"+" "+file_name+" "+CONFIG.username+" "+CONFIG.password + " " + str(need))
                        need -= 1
                        if (receiver.receive()):
                            self.send_file(receiver, parts[need])
                        receiver.receive()
                        receiver.close()
            afile.close()

        except IOError:
            print ERRORS.invalid_file


    def __init__(self):
        self.receivers = []
        for name, address in CONFIG.servers.items():
            address = address.split(":")
            ip = address[0]
            port = int(address[1])
            receiver = RECEIVER(name, ip, port)
            self.receivers.append(receiver)
        return

class CLIENT_HANDLER:
    def start(self):
        try:
            while 1:
                command = raw_input("Enter a command: ")
                operation = command.split()
                if (operation[0].lower() == "list"):
                    self.handler.list()
                if (operation[0].lower() == "get"):
                    self.handler.get(operation[1])
                if (operation[0].lower() == "put"):
                    self.handler.put(operation[1])
        except KeyboardInterrupt:
            return True
    def __init__(self):
        self.handler = CONNECTION_HANDLER()
        return
