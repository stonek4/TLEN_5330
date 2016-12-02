class CONSTANT:
    @staticmethod
    def read_config(file_name):
        f = open(file_name, 'r')
        for line in f:
            configuration = line.split()
            if configuration[0] == "ListenPort":
                CONSTANT.port = configuration[1]
            elif configuration[0] == "Address":
                CONSTANT.ip_address = configuration[1]
            elif configuration[0] == "DocumentRoot":
                CONSTANT.document_root = configuration[1]
            elif configuration[0] == "DirectoryIndex":
                for index in configuration.pop(0):
                    CONSTANT.directory_indexes.append(index)
            elif configuration[0] == "ContentType":
                CONSTANT.content_types[configuration[1]] = configuration[2]
            elif configuration[0] == "KeepAliveTime":
                CONSTANT.keep_alive_time = configuration[1]
            elif configuration[0] == "PacketSize":
                CONSTANT.packet_size = configuration[1]
            elif configuration[0] == "MaxConnections":
                CONSTANT.max_connections = configuration[1]
        f.close()
    keep_alive_time = 0
    content_types = {}
    directory_indexes = []
    ip_address = ""
    port = 0
    stay_awake = 30
    document_root = ""
    invalid_arguments = "Invalid Arguments: (python <client.py> <ip address> <port number>)"
    invalid_port_number = "Invalid Arguments: port number must be larger than 5000"
    no_server_response = "No response from the server"
    no_server_response_ping = "Initial server contact failed, if server is started, maybe try using a different port?"
    no_client_response = "No response from the client"
    file_error = "File could not be found/opened"
    server_starting = "Server started..."
    client_starting = "Client started, available commands are:"
    listing_files = "Sending file list..."
    exiting = "Request to kill server session received, exiting..."
    sending_file = "Sending file..."
    finished_sending_file = "File send completed"
    receiving_file = "Receiving file..."
    finished_receiving_file = "File reception completed"
    timeout_failure = "Failed after multiple timeouts"
    retrying = "Retrying..."
    connected = " contacted server"
    put_cmd = "put"
    get_cmd = "get"
    list_cmd = "list"
    exit_cmd = "exit"
    unknown_cmd = " command is not recognized by the server"
    file_example = "[file_name]"
    ack = "ACK"
    received = "received_"
    server_file_location = "www"
    client_file_location = "Client_Files"
    escape_code = "$$$done$$$"
    packet_size = 1024
    max_connections = 1
    http_OK = "200 OK"
    def __init__(self):
        return
