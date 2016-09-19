from classes.listener import LISTENER

def main():
    listener = LISTENER(5000, 1024)
    listener.start()

main();
