import sys
import os
from classes.constant import CONFIG
from classes.constant import ERRORS
from classes.constant import PATHS
from classes.constant import INFO
from classes.handler import CLIENT_HANDLER

def main():
    if (CONFIG.read_config(PATHS.config) == False):
        return
    if (len(sys.argv) > 2 or len(sys.argv) < 1):
        print ERRORS.invalid_arguments
        sys.exit(2)
    if (len(sys.argv) == 2):
        PATHS.config = sys.argv[1]

    handler = CLIENT_HANDLER()
    print INFO.starting
    handler.start()
main()
