import sys
from classes.constant import CONSTANT
from classes.handler import SERVER_HANDLER

def main():
    CONSTANT.read_config("./ws.conf")
    if (len(sys.argv) != 1):
        print CONSTANT.invalid_arguments
        sys.exit(2)

    elif (int(CONSTANT.port) <= 5000 or int(CONSTANT.port) >= 65535):
        return

    handler = SERVER_HANDLER()
    print CONSTANT.server_starting
    handler.start()
main()
