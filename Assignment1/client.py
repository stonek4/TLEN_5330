import sys
from classes.constant import CONSTANT
from classes.sender import SENDER

def main():
    if (len(sys.argv) != 3):
        print CONSTANT.invalid_arguments
        sys.exit(2)
    else:
        sender = SENDER(1024)
        sender.send("hi", sys.argv[1], int(sys.argv[2]))

main()
