#! /usr/bin/python3

import socket
from chord_tools import *

chord_data = {}


def get(key, ip, port):
    data = chord_data.get(key)
    if data:
        json_send(ip, port, data)
    else:
        json_send(ip, port, -1)


def update(key, value, ip=None, port=None):
    chord_data[key] = value

    if ip and port:
        json_send(ip, port, "updated")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind(('', 8001))
    serversocket.listen(5)
    print('listening on port:', serversocket.getsockname()[1])
    while True:
        (clientsocket, address) = serversocket.accept()
        json_data = json_recv(clientsocket)
        print(json_data)

        if json_data[0] == 'get':
            get(json_data[1], json_data[2], json_data[3])
        elif json_data[0] == 'update':
            update(json_data[1], json_data[2], json_data[3], json_data[4])

        # json_send('localhost', 9000, 42)
