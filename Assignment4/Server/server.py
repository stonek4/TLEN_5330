import sys
import os
from classes.constant import CONFIG
from classes.constant import ERRORS
from classes.constant import PATHS
from classes.constant import INFO
from classes.handler import SERVER_HANDLER

def main():
    if (CONFIG.read_config(PATHS.config) == False):
        return
    if (len(sys.argv) != 3):
        print ERRORS.invalid_arguments
        sys.exit(2)
    path = sys.argv[1]
    if not os.path.exists("."+path):
        os.makedirs("."+path)
    port = sys.argv[2]

    if (int(port) <= 5000 or int(port) >= 65535):
        print ERRORS.invalid_port
        sys.exit(2)

    CONFIG.port = port
    CONFIG.document_root = path+"/"
    handler = SERVER_HANDLER()
    print INFO.starting
    handler.start()
main()
