import sys
from classes.constant import CONSTANT

def main():
    if (len(sys.argv) != 3):
        print CONSTANT.invalid_arguments
        sys.exit(2)

    print "ok"

main()
