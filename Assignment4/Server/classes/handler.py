import os
import multiprocessing
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
        while (data[0]):
            afile.write(data[0])
            data = sender.receive_data()
        afile.close()

    def not_implemented(self, sender, data):
        print "Not implemented"

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

    def list(self, user, sender):
        path = PATHS.directory_root + user
        try:
            file_names = [x[0] for x in os.walk(path)]
            if (len(file_names) == 0):
                return
            file_names.pop(0)
            for name in file_names:
                files = os.walk(name).next()[2]
                output = name.split("/")[-1] + " "
                for afile in files:
                    output += afile + " "
                sender.send(output)
                sender.receive()
            return
        except IOError:
            print ERRORS.invalid_file
        except Exception as e:
            print ERRORS.server
            print e

    def get(self, user, file_name, part, sender):
        path = PATHS.directory_root + user + "/" + file_name + "/"
        try:
            for afile in os.listdir(path):
                if (afile == "."+part):
                    print path+afile
                    self.send_file(sender, open(path + afile))
                    sender.close()
            return
        except IOError:
            print ERRORS.invalid_file
        except Exception as e:
            print ERRORS.server
            print e

    def close(self, sender):
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
            if (user not in CONFIG.logins):
                print "Unauthorized login attempt"
                receiver.send("UAD")
            if (CONFIG.logins[user] != password):
                print "Unauthorized login attempt"
                receiver.send("UAD")
                return
            else:
                receiver.send("ACK")
                receiver.receive()
            part = "-1"
            if (len(request) == 5):
                part = request[4]

            print [ip, port], "~ is requesting", file_name
            print [ip, port], "~ using method", operation

            if (operation == "GET"):
                self.get(user, file_name, part, receiver)
            elif (operation == "PUT"):
                self.put(user, file_name, part, receiver)
            elif (operation == "LIST"):
                self.list(user, receiver)
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
