import sys
from classes.constant import CONSTANT
from classes.handler import SERVER_HANDLER

def main():
    if (len(sys.argv) != 2):
        print CONSTANT.invalid_arguments
        sys.exit(2)
    elif (int(sys.argv[1]) <= 5000):
        print CONSTANT.invalid_port_number
        return
    handler = SERVER_HANDLER(int(sys.argv[1]))
    print CONSTANT.server_starting
    handler.start()
main()
