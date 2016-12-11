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
            f.close()
        except IOError:
            print ERRORS.no_config
            return False
        return True
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
        x = int(new_hash.hexdigest(), 16) % 4
        if (server_name == "DFS1"):
            return [(5-x)%4,(6-x)%4]
        if (server_name == "DFS2"):
            return [(6-x)%4,(7-x)%4]
        if (server_name == "DFS3"):
            return [(7-x)%4,(8-x)%4]
        if (server_name == "DFS4"):
            return [(8-x)%4,(5-x)%4]
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
    def __init__(self):
        return

class INFO:
    timeout = "Connection timed out"
    starting = "Server starting..."
    client_keep_alive = "The client is pinging the server to keep it alive"
    closing_connection = "Closing connection..."
    cleaning_processes = "Cleaning up processes, press ctrl-c again to force quit"
    killing_process = "User initiated server shutdown, exiting process..."

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
