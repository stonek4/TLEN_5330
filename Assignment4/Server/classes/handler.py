import os
import multiprocessing
import shutil
import tempfile
import signal
from constant import CONFIG
from constant import PATHS
from constant import ERRORS
from constant import INFO
from receiver import LISTENER
from receiver import RECEIVER
from messages import MESSAGES



class CONNECTION_HANDLER:
    # send the file to the client
    def send_file(self, sender, afile):
        data = afile.read(int(CONFIG.packet_size))
        while (data):
            sender.send(data)
            data = afile.read(int(CONFIG.packet_size))
        afile.close()

    def recv_file(self, sender, afile):
        data = sender.receive_data()
        while (data):
            afile.write(data[0])
            data = sender.receive_data()
        afile.close()

    def not_found(self, sender, url):
        path = PATHS.directory_root + PATHS.not_found
        header = self.messages.get_header(path,".html",404)
        sender.send(header)
        self.send_file(sender, open(path,"rb"))

    def server_error(self, sender):
        path = PATHS.directory_root + PATHS.server_error
        header = self.messages.get_header(path,".html",500)
        sender.send(header)
        self.send_file(sender, open(path,"rb"))

    def not_implemented(self, sender, data):
        path = PATHS.directory_root + PATHS.not_implemented
        header = self.messages.get_header(path,".html",404)
        sender.send(header)
        self.send_file(sender, open(path,"rb"))

    def post(self, file_name, sender, data):
        self.not_implemented(sender, "DELETE")
        return

    def put(self, user, file_name, part, sender):
        path = PATHS.directory_root + user + "/" + file_name + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        sender.send("ACK")
        self.recv_file(sender, open(path+"."+part,"wb"))
        print "finished receiving file"

    def delete(self, sender):
        self.not_implemented(sender, "DELETE")
        return

    def list(self, user, file_name, sender):
        path = PATHS.directory_root + user + "/" + "." + file_name + "/"
        try:
            parts = ""
            for afile in os.listdir(path):
                parts += os.path.basename(afile.name) + " "
            sender.send(parts)
            return
        except IOError:
            print ERRORS.invalid_file
            self.not_found(sender, path)
        except Exception as e:
            print ERRORS.server
            print e
            self.server_error(sender)

    def get(self, user, file_name, sender):
        path = PATHS.directory_root + user + "/" + file_name + "/"
        try:
            for afile in os.listdir(path):
                open(path + afile)
                self.send_file(sender, open(path, "rb"))
            return
        except IOError:
            print ERRORS.invalid_file
            self.not_found(sender, path)
        except Exception as e:
            print ERRORS.server
            print e
            self.server_error(sender)

    def close(self, sender):
        header = self.messages.get_header("", "", 0)
        sender.send(header)
        sender.close()

    # upon connecting waits for certain time before closing connection
    # otherwise parses the message from the client and calls the appropriate
    # method
    def process_handler(self, conn, ip, port):
        try:
            print [ip, port], "~ has connected"
            receiver = RECEIVER(conn)
            data = receiver.receive()
            if (data == False):
                print [ip, port], "~", INFO.client_disconnect
                self.close(receiver)
                return
            request = data[0].split()
            print request
            operation = request[0]
            file_name = request[1]
            user = request[2]
            password = request[3]
            part = "-1"
            if (len(request) == 5):
                part = request[4]

            print [ip, port], "~ is requesting", file_name
            print [ip, port], "~ using method", operation

            if (operation == "GET"):
                self.get(user, file_name, receiver)
            elif (operation == "PUT"):
                self.put(user, file_name, part, receiver)
            elif (operation == "LIST"):
                self.list(user, file_name, receiver)
            else:
                print ERRORS.invalid_command
        except KeyboardInterrupt:
            print "\n",[ip, port],"~",INFO.killing_process
        except:
            print ERRORS.unknown_socket_error
        print [ip, port], "~", INFO.closing_connection
        self.close(receiver)
        exit()
    def __init__(self):
        self.messages = MESSAGES("HTTP/1.1")
        return

class SERVER_HANDLER:
    def start(self):
        processes = []
        try:
            while 1:
                data = self.listener.accept()
                if (data == False):
                    break
                else:
                    connection = CONNECTION_HANDLER()
                    process = multiprocessing.Process(target=connection.process_handler,
                                            args=(data[0], data[1], data[2]))
                    process.start()
                    processes.append(process)
        except KeyboardInterrupt:
            try:
                print "\n" + INFO.cleaning_processes
                for process in processes:
                    if process.is_alive():
                        process.join()
            except KeyboardInterrupt:
                for process in processes:
                    if process.is_alive():
                        process.terminate()
        return True
    def __init__(self):
        self.listener = LISTENER()
        return
