import hashlib

class CONFIG:
    # parses the configuration file
    @staticmethod
    def read_config(file_name):
        try:
            f = open(file_name, 'r')
            for line in f:
                configuration = line.split()
                if configuration[0] == "Server":
                    CONFIG.servers[configuration[1]] = configuration[2]
                elif configuration[0] == "ServerTimeout":
                    CONFIG.timeout = configuration[1]
                elif configuration[0] == "PacketSize":
                    CONFIG.packet_size = configuration[1]
                elif configuration[0] == "Username":
                    CONFIG.username = configuration[1]
                elif configuration[0] == "Password":
                    CONFIG.password = configuration[1]
                elif configuration[0] == "KeepAliveTime":
                    CONFIG.keep_alive_time = configuration[1]
                elif configuration[0] == "Redundancy":
                    CONFIG.redundancy = configuration[1]
            f.close()
        except IOError:
            print ERRORS.no_config
            return False
        return True
    redundancy = 0
    timeout = 0
    servers = {}
    packet_size = 1024
    username = ""
    password = ""
    keep_alive_time = 2
    def __init__(self):
        return

class PARTS:
    @staticmethod
    def get_parts(file_name, server_name):
        new_hash = hashlib.md5(file_name)
        x = int(new_hash.hexdigest(), 16) % len(CONFIG.servers)
        i = 1
        parts = []
        while (i <= len(CONFIG.servers)):
            part = (len(CONFIG.servers)+i-x)%len(CONFIG.servers)
            parts.append(part)
            i += 1
        server = int(server_name[-1])
        i = 0
        count = 0
        red_parts = []
        while (i < int(CONFIG.redundancy)):
            if (server-1+count == len(CONFIG.servers)):
                server = 1
                count = 0
            red_parts.append(parts[(server-1)+count])
            count += 1
            i += 1
        return red_parts
    def __init__(self):
        return

class ERRORS:
    server = "Unknown server error"
    bad_conn = "Connection to server failed"
    invalid_port = "Invalid port number"
    busy_port = "Port is busy, try another"
    invalid_file = "File not found or cannot be opened"
    invalid_arguments = "Invalid Arguments: (python <client.py> <ip address> <port number>)"
    invalid_command = "Bad request received"
    invalid_http = "The command received was not an http request"
    no_config = "The configuration file could not be found or opened"
    not_supported = "This file type is not supported"
    html_not_supported = "Must configure for .html support for errors to be served"
    client_pipe_down = "The pipe to the client closed before the data could send"
    unknown_socket_error = "An unknown socket error occured"
    invalid_server_file = "The file was not found on the servers"
    invalid_parts = "The file is unavailable due to a lack of parts"
    unauthorized = "The credentials provided are invalid"
    too_small_file = "The file is too small to effectively split amongst servers"

    def __init__(self):
        return

class INFO:
    timeout = "Connection timed out"
    starting = "Client starting..."
    client_keep_alive = "The client is pinging the server to keep it alive"
    closing_connection = "Closing connection..."
    cleaning_processes = "Cleaning up processes, press ctrl-c again to force quit"
    killing_process = "User initiated server shutdown, exiting process..."
    lack_of_servers = "Not enough servers, the file was uploaded to whatever servers were available."
    enter_command = "Enter a command: "

    def __init__(self):
        return

class COMMANDS:
    ack = "ACK"
    unauthorized = "UAD"
    incomplete = "[INCOMPLETE]"
    get = "GET"
    put = "PUT"
    lstall = "LIST all"
    lst = "LIST"

    def __init__(self):
        return

class PATHS:
    directory_root = ""
    not_found = directory_root + "/errors/not_found.html"
    bad_request = directory_root + "/errors/bad_request.html"
    server_error = directory_root + "/errors/server_error.html"
    not_implemented = directory_root + "/errors/not_implemented.html"
    config = "./dfc.conf"

    def __init__(self):
        return
