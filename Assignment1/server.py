import sys
from classes.constant import CONSTANT
from classes.listener import LISTENER

def main():
    if (len(sys.argv) != 2):
        print CONSTANT.invalid_arguments
        sys.exit(2)
    elif (int(sys.argv[1]) <= 5000):
        print CONSTANT.invalid_port_number
    listener = LISTENER(5000, 1024)
    listener.start()

main()
