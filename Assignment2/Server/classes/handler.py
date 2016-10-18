import os
import threading
from constant import CONSTANT
from receiver import LISTENER
from receiver import RECEIVER
from sender import SENDER

class SERVER_HANDLER:
    def put(self, file_name, sender):
        return

    def get(self, file_name, sender, http_format):
        path = CONSTANT.server_file_location+file_name
        if path == CONSTANT.server_file_location+"/":
            path += "index.html"
        try:
            file_type = "."+path.split(".")[1]
            print file_type
            size = os.path.getsize(path)
            afile = open(path, "rb")
            header = http_format + " " + CONSTANT.http_OK + "\n"
            header += "Content-Type: " + CONSTANT.content_types[file_type] + "\n"
            header += "Content-Length: " + str(size) + "\n" + "\n"
            sender.send(header)
            data = afile.read(int(CONSTANT.packet_size))
            while (data):
                sender.send(data)
                data = afile.read(int(CONSTANT.packet_size))
            afile.close()
            return
        except IOError:
            print CONSTANT.file_error

    def list(self, sender):
        print CONSTANT.listing_files
        all_files = ""
        for afile in os.listdir(CONSTANT.server_file_location):
            all_files = all_files + afile + " "
        sender.send_message(all_files)

    def exit(self):
        print CONSTANT.exiting
        self.listener.close()

    def other(self, sender, command):
        print CONSTANT.unknown_cmd
        sender.send_message(command + CONSTANT.unknown_cmd)

    def thread_handler(self, conn, ip, port):
        print [ip, port], "~ has connected"
        while 1:
            receiver = RECEIVER(conn)
            data = receiver.receive()
            if (data == False):
                return
            else:
                request = data[0].split()
                print [ip, port], "~ issued", request[0], "command"
                if (request[0] == "GET"):
                    self.get(request[1], receiver, request[2])
        receiver.close()
        exit()

    def start(self):
        threads = []
        while 1:
            data = self.listener.accept()
            if (data == False):
                break
            else:
                thread = threading.Thread(target=self.thread_handler,
                                        args=(data[0], data[1], data[2]))
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()
        return True
    def __init__(self):
        self.listener = LISTENER()
        return
