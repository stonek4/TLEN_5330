import sys
from classes.constant import CONSTANT
from classes.handler import CLIENT_HANDLER

def main():
    if (len(sys.argv) != 3):
        print CONSTANT.invalid_arguments
        sys.exit(2)
    else:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        handler = CLIENT_HANDLER(server_address, server_port)
        handler.start()

main()
