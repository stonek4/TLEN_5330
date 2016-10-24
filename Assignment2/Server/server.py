import sys
from classes.constant import CONFIG
from classes.constant import ERRORS
from classes.constant import PATHS
from classes.constant import INFO
from classes.handler import SERVER_HANDLER

def main():
    if (CONFIG.read_config(PATHS.config) == False):
        return
    if (len(sys.argv) != 1):
        print ERRORS.invalid_arguments
        sys.exit(2)

    elif (int(CONFIG.port) <= 5000 or int(CONFIG.port) >= 65535):
        return

    handler = SERVER_HANDLER()
    print INFO.starting
    handler.start()
main()
