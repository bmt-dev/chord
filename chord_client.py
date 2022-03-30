#! /usr/bin/python3

import socket
import threading
from chord_tools import *


def printer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind(('', 9000))
        serversocket.listen(5)
        print('listening on port:', serversocket.getsockname()[1])
        while True:
            (clientsocket, address) = serversocket.accept()
            json_data = json_recv(clientsocket)
            print(json_data)


printer_thread = threading.Thread(target=printer)
printer_thread.start()

# data = [{'test':22}, 'other test', 88]
data = [
    ['get', 0, 'localhost', 9000],
    ['update', 0, 'tata', 'localhost', 9000],
    ['get', 0, 'localhost', 9000]
]

for d in data:
    json_send('localhost', 8001, d)
