import socket
import multiprocessing
import os
import signal
import time

def port_listener(port, command):
    print(f"Port {port} listener started")
    
    # Listen loop
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.bind(('localhost', port))
    listener_socket.listen(1)   # No need for more than one connection in this application

    while True:
        # Waiting for an attempted connecti, and running our command
        connection, addr = listener_socket.accept()
        connection.close()

        print(f"port: {port} PINGED")
        os.system(f"{command}")


# Preparing our argument
arguments = []
with open("port_mapping.csv", "r") as f:
    lines = f.readlines()
    for line in lines[1:]:
        cells = line.split(',')
        arguments.append((int(cells[0]), cells[1].strip(),))

# Setting up our multiprocessing
# Signal handling from https://stackoverflow.com/questions/11312525/catch-ctrlc-sigint-and-exit-multiprocesses-gracefully-in-python
if __name__ == '__main__':
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = multiprocessing.Pool(len(arguments))
    signal.signal(signal.SIGINT, original_sigint_handler)

    pool.starmap(port_listener, arguments)