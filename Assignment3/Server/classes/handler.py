import os
import sys
import multiprocessing
import shutil
import tempfile
import signal
import urlparse
import socket
import hashlib
import time
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

    def post(self, sender):
        self.not_implemented(sender, "POST")
        return

    def put(self, sender):
        self.not_implemented(sender, "PUT")
        return

    def delete(self, sender):
        self.not_implemented(sender, "DELETE")
        return

    def get(self, proc, hashstring, request, server, client):
        new_hash = hashlib.md5(hashstring)
        if (os.path.isfile(CONFIG.cache_root+new_hash.hexdigest())):
            print proc,"~", INFO.using_cache
            h_file = open(CONFIG.cache_root+new_hash.hexdigest()+"header", "r+")
            header = h_file.read()
            h_file.close()
            client.send(header+"\r\n\r\n")
            c_file = open(CONFIG.cache_root+new_hash.hexdigest(), "rb")
            packet = c_file.read(int(CONFIG.packet_size))
            while packet:
                client.send(packet)
                packet = c_file.read(int(CONFIG.packet_size))
            c_file.close()
            print proc,"~",INFO.finished_send
        else:
            print proc, "~", ERRORS.invalid_file
            print proc, "~", INFO.adding_cache
            new_file = open(CONFIG.cache_root+new_hash.hexdigest(), "wb")
            new_header = open(CONFIG.cache_root+new_hash.hexdigest()+"header", "w")
            server.send(request)
            first = True
            while 1:
                data = server.receive()
                if (data != ""):
                    if (first == True):
                        content = data.split('\r\n\r\n')
                        new_header.write(content[0])
                        new_file.write(content[1])
                        first = False
                    else:
                        new_file.write(data)
                    client.send(data)
                else:
                    new_file.close()
                    new_header.close()
                    print proc,"~",INFO.finished_send
                    break
        return

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
                if (data == ""):
                    print [ip, port], "~", INFO.timeout
                    break
                request = data.split('\r\n')
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
                        self.get([ip,port], operation[1], data, server, receiver)
                        self.close(server)
                    elif (operation[0] == "POST"):
                        self.post(receiver)
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
                still_alive = []
                for process in processes:
                    if process.is_alive():
                        still_alive.append(process)
                processes = still_alive
                print INFO.active_processes, len(processes)
                if (len(processes) == 0):
                    print INFO.cleaning_cache
                    rem_count = 0
                    for hashes in os.listdir(CONFIG.cache_root):
                        last_modified = os.path.getmtime(CONFIG.cache_root+hashes)
                        if (time.time() - last_modified) > CONFIG.cache_timeout:
                            os.remove(CONFIG.cache_root+hashes)
                            rem_count += 1
                    print INFO.files_cleaned, rem_count

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
