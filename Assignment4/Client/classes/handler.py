import os
import math
from collections import defaultdict
from constant import CONFIG
from constant import ERRORS
from constant import INFO
from constant import COMMANDS
from constant import PARTS
from receiver import RECEIVER



class CONNECTION_HANDLER:
    '''
    SEND A FILE TO THE SERVER
    '''
    def send_file(self, sender, data):
        sender.send(data)

    '''
    RECEIVE A FILE FROM THE SERVER
    '''
    def recv_file(self, sender, afile):
        data = sender.receive()
        while (data[0]):
            afile.write(data[0])
            data = sender.receive()

    '''
    RETURN A DICTIONARY OF THE AVAILABLE FILES
    (returns False if an error occurs)
    '''
    def available_files(self):
        all_files = defaultdict(set)
        for receiver in self.receivers:
            receiver.connect()
            if receiver.connected:
                receiver.send(COMMANDS.lstall + " " + CONFIG.username + " " + CONFIG.password)
                if (not self.auth_check(receiver)):
                    receiver.close()
                    return False
                while 1:
                    newput = receiver.receive()
                    if (newput == False):
                        print ERRORS.unknown_socket_error
                        return False
                    if (newput[0]):
                        afile = newput[0].split()
                        name = afile.pop(0)
                        for bfile in afile:
                            all_files[name].add(bfile)
                        receiver.send(COMMANDS.ack)
                    else:
                        receiver.close()
                        break
        return all_files

    '''
    LIST THE AVAILABLE FILES
    '''
    def list(self):
        all_files = self.available_files()
        if (all_files == False):
            return
        for key, files in all_files.items():
            if len(files) == len(CONFIG.servers):
                print key
            else:
                print key + " " + COMMANDS.incomplete
        return

    '''
    GET THE FILE BY FILE NAME
    '''
    def get(self, file_name):
        all_files = self.available_files()
        if (all_files == False):
            return
        if (file_name not in all_files):
            print ERRORS.invalid_server_file
            return
        if (len(all_files[file_name]) != len(CONFIG.servers)):
            print (ERRORS.invalid_parts)
            return
        try:
            afile = open(file_name, "wb")
        except IOError:
            print ERRORS.invalid_file
            return
        parts_retrieved = 1
        while 1:
            part_wrote = False
            for receiver in self.receivers:
                needed = PARTS.get_parts(file_name, receiver.name)
                for need in needed:
                    if (need == 0):
                        need = len(CONFIG.servers)
                    if (need == parts_retrieved):
                        receiver.connect()
                        if (receiver.connected):
                            receiver.send(COMMANDS.get+" " +file_name+" "+CONFIG.username+" "+CONFIG.password+" "+str(need))
                            if (not self.auth_check(receiver)):
                                receiver.close()
                                afile.close()
                                return
                            self.recv_file(receiver, afile)
                            receiver.close()
                            parts_retrieved += 1
                            part_wrote = True
                            break
            if ( not part_wrote):
                print (ERRORS.invalid_parts)
            if (parts_retrieved == len(CONFIG.servers)+1):
                break
        afile.close()
        return

    '''
    CHECK WHETHER THE USER IS AUTHORIZED
    (receives response from server)
    '''
    def auth_check(self, sender):
        if (sender.receive()[0] == COMMANDS.unauthorized):
            print ERRORS.unauthorized
            return False
        else:
            sender.send("ACK")
            return True

    '''
    PUT THE FILE ONTO THE SERVERS
    '''
    def put(self, file_name):
        try:
            try:
                afile = open(file_name, "rb")
            except IOError:
                print ERRORS.invalid_file
                return
            part_size = int(math.ceil(os.path.getsize(file_name)/len(CONFIG.servers)))
            data = afile.read(part_size)
            servers_ul = 0
            parts = []
            while(data):
                parts.append(data)
                data = afile.read(part_size)
            if (len(parts) < len(CONFIG.servers)):
                print (ERRORS.too_small_file)
            for receiver in self.receivers:
                file_name = os.path.basename(afile.name)
                needed = PARTS.get_parts(file_name, receiver.name)
                for need in needed:
                    receiver.connect()
                    if (receiver.connected):
                        servers_ul += .5
                        if (need == 0):
                            need = len(CONFIG.servers)
                        receiver.send(COMMANDS.put+" "+file_name+" "+CONFIG.username+" "+CONFIG.password + " " + str(need))
                        if (not self.auth_check(receiver)):
                            receiver.close()
                            afile.close()
                            return
                        need -= 1
                        if (receiver.receive()):
                            self.send_file(receiver, parts[need])
                        receiver.close()
            if (servers_ul < len(CONFIG.servers)-1):
                print (INFO.lack_of_servers)
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
                command = raw_input(INFO.enter_command)
                operation = command.split()
                if (operation[0].upper() == COMMANDS.lst):
                    self.handler.list()
                if (operation[0].upper() == COMMANDS.get):
                    if (len(operation) == 2):
                        self.handler.get(operation[1])
                if (operation[0].upper() == COMMANDS.put):
                    if (len(operation) == 2):
                        self.handler.put(operation[1])
        except KeyboardInterrupt:
            return True
    def __init__(self):
        self.handler = CONNECTION_HANDLER()
        return
