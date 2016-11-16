import os
import multiprocessing
import shutil
import tempfile
import signal
import urlparse
import socket
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

    # add a message to file (Looks for class="text" while writing to new file
    # then replaces the next line with the input value of the post. When
    # finished it will move the temporary file where the old one used to be
    def add_post(self, path, post_data):
        afile = open(path)
        handler, temp_path = tempfile.mkstemp()
        tfile = open(temp_path, "w")
        up_next = 0
        for line in afile:
            if up_next == 1:
                tfile.write(post_data + "\n")
                up_next = 0
            else:
                if 'class="text"' in line:
                    up_next = 1
                tfile.write(line)
        afile.close()
        tfile.close()
        os.close(handler)
        shutil.move(temp_path, path)

    def not_found(self, sender, url):
        path = PATHS.directory_root + PATHS.not_found
        self.add_post(path, "404 NOT FOUND: " + url)
        header = self.messages.get_header(path,".html",404)
        sender.send(header)
        self.send_file(sender, open(path,"rb"))

    def server_error(self, sender):
        path = PATHS.directory_root + PATHS.server_error
        header = self.messages.get_header(path,".html",500)
        sender.send(header)
        self.send_file(sender, open(path,"rb"))

    def bad_request(self, sender, issue, data):
        path = PATHS.directory_root + PATHS.bad_request
        if (issue == "method"):
            self.add_post(path, "400 BAD REQUEST METHOD: " + data)
        elif (issue == "url"):
            self.add_post(path, "400 BAD REQUEST URL: " + data)
        elif (issue == "http"):
            self.add_post(path, "400 BAD REQUEST HTTP: " + data)
        else:
            self.add_post(path, "400 BAD REQUEST")
        header = self.messages.get_header(path,".html",400)
        sender.send(header)
        self.send_file(sender, open(path,"rb"))

    def not_implemented(self, sender, data):
        path = PATHS.directory_root + PATHS.not_implemented
        self.add_post(path, "501 NOT IMPLEMENTED: " + data)
        header = self.messages.get_header(path,".html",404)
        sender.send(header)
        self.send_file(sender, open(path,"rb"))

    def post(self, file_name, sender, data):
        path = PATHS.directory_root + file_name
        if path == PATHS.directory_root + "/":
            for name in CONFIG.directory_indexes:
                if (os.path.isfile(path+name)):
                    path += name
                    break
        try:
            ftype = "."+path.split(".")[2]
            CONFIG.content_types[ftype]
            open(path)
            self.add_post(path, data)
            header = self.messages.get_header(path, ftype, 200)
            sender.send(header)
            self.send_file(sender, open(path,"rb"))
            return
        except IOError:
            print ERRORS.invalid_file
            self.not_found(sender, path)
        except KeyError:
            print ERRORS.not_supported
            self.not_implemented(sender, ftype)
        except Exception as e:
            print ERRORS.server
            print e
            self.server_error(sender)
        return

    def put(self, sender):
        self.not_implemented(sender, "PUT")
        return

    def delete(self, sender):
        self.not_implemented(sender, "DELETE")
        return

    def get(self, request, server, client):
        try:
            server.send(request)
            while 1:
                data = server.receive()
                if (data[0] != ""):
                    client.send(data[0])
                else:
                    break
            return
        except IOError:
            print ERRORS.invalid_file
            self.not_found(client, request)
        except Exception as e:
            print ERRORS.server
            print e
            self.server_error(client)

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
            receiver = RECEIVER()
            receiver.add_connection(conn)
            while 1:
                data = receiver.receive()
                if (data[0] == ""):
                    print [ip, port], "~", INFO.timeout
                    break
                print data
                request = data[0].split('\r\n')
                operation = request[0].split()
                connection = "Close"

                for part in request:
                    if "Connection:" in part:
                        connection = part.split()[1]

                if (len(operation) >= 3):
                    if (operation[2] != "HTTP/1.1" and operation[2] != "HTTP/1.0"):
                        self.bad_request(receiver, "http", operation[2])
                        break
                    print [ip, port], "~", operation[0], "command"
                    self.messages = MESSAGES(operation[2])

                    if (operation[0] == "GET"):
                        print [ip, port], "~ is requesting", operation[1]
                        print [ip, port], "~ is using",operation[2]
                        url = urlparse.urlparse(operation[1])
                        url_ip = url.netloc
                        url_port = CONFIG.default_port
                        tmp_port = url.port
                        if (tmp_port != None):
                            url_port = int(tmp_port)
                        server = RECEIVER()
                        server.connect(url_ip, url_port)
                        self.get(data[0], server, receiver)
                        self.close(server)
                    elif (operation[0] == "POST"):
                        break
                        print [ip, port], "~ is requesting", operation[1]
                        print [ip, port], "~ is using",operation[2]
                        new_val = request[len(request)-1].split('=')[1]
                        self.post(operation[1], receiver, new_val)
                    elif (operation[0] == "PUT"):
                        self.put(receiver)
                    elif (operation[0] == "DELETE"):
                        self.delete(receiver)
                    else:
                        print ERRORS.invalid_command
                        self.bad_request(receiver, "method", operation[0])

                    if (connection.lower() != "keep-alive"):
                        break
                else:
                    self.bad_request(receiver, "unknown", "incorrect format")
                    break
        except KeyboardInterrupt:
            print "\n",[ip, port],"~",INFO.killing_process
        print [ip, port], "~", INFO.closing_connection
        self.close(receiver)
        exit()
    def __init__(self):
        self.messages = MESSAGES("HTTP/1.0")
        return

class SERVER_HANDLER:
    def start(self):
        processes = []
        try:
            while 1:
                data = self.listener.accept()
                if (data != False):
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
