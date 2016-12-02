class CONFIG:
    # parses the configuration file
    @staticmethod
    def read_config(file_name):
        try:
            f = open(file_name, 'r')
            for line in f:
                configuration = line.split()
                if configuration[0] == "ListenPort":
                    CONFIG.port = configuration[1]
                elif configuration[0] == "Address":
                    CONFIG.ip_address = configuration[1]
                elif configuration[0] == "DocumentRoot":
                    PATHS.directory_root = configuration[1]
                elif configuration[0] == "DirectoryIndex":
                    configuration.pop(0)
                    for index in configuration:
                        CONFIG.directory_indexes.append(index)
                elif configuration[0] == "ContentType":
                    CONFIG.content_types[configuration[1]] = configuration[2]
                elif configuration[0] == "KeepAliveTime":
                    CONFIG.keep_alive_time = configuration[1]
                elif configuration[0] == "PacketSize":
                    CONFIG.packet_size = configuration[1]
                elif configuration[0] == "MaxConnections":
                    CONFIG.max_connections = configuration[1]
            f.close()
        except IOError:
            print ERRORS.no_config
            return False
        return True
    keep_alive_time = 0
    content_types = {}
    directory_indexes = []
    ip_address = ""
    port = 0
    stay_awake = 30
    poll_time = 10
    document_root = ""
    packet_size = 1024
    max_connections = 1
    def __init__(self):
        return

class ERRORS:
    server = "Unknown server error"
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
    unkown_socket_error = "An unknown socket error occured"
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
    config = "./ws.conf"

    def __init__(self):
        return
