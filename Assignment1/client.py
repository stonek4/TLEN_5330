import sys
from classes.constant import CONSTANT
from classes.sender import SENDER

def main():
    if (len(sys.argv) != 3):
        print CONSTANT.invalid_arguments
        sys.exit(2)
    else:
        sender = SENDER()
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        while 1:
            commands = raw_input()
            sender.send_command(commands, server_address, server_port)
            sender.handle_command(commands, server_address, server_port)




main()
