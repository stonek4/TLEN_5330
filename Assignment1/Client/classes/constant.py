class CONSTANT:
    invalid_arguments = "Invalid Arguments: (python <client.py> <ip address> <port number>)"
    invalid_port_number = "Invalid Arguments: port number must be larger than 5000"
    no_server_response = "No response from the server"
    no_server_response_ping = "Initial server contact failed, if server is started, maybe try using a different port?"
    no_client_response = "No response from the client"
    file_error = "File could not be found/opened"
    server_starting = "Server started..."
    client_starting = "Client started, available commands are:"
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
    server_file_location = "Server_Files"
    client_file_location = "Client_Files"
    escape_code = "$$$done$$$"
    packet_size = 1024
    def __init__(self):
        return
