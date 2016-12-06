import sys
from classes.constant import CONFIG
from classes.constant import ERRORS
from classes.constant import PATHS
from classes.constant import INFO
from classes.handler import SERVER_HANDLER

def main():
    if (CONFIG.read_config(PATHS.config) == False):
        return
    if (len(sys.argv) > 3 or len(sys.argv) < 1):
        print ERRORS.invalid_arguments
        sys.exit(2)
    elif (len(sys.argv) == 2):
        CONFIG.port = sys.argv[1]
    elif (len(sys.argv) == 3):
        CONFIG.port = sys.argv[1]
        CONFIG.cache_timeout = int(sys.argv[2])
    if (int(CONFIG.port) <= 5000 or int(CONFIG.port) >= 65535):
        print ERRORS.invalid_port
        return
    handler = SERVER_HANDLER()
    print INFO.starting
    handler.start()
main()
