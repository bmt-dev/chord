#! /usr/bin/python3

import socket
import sys
from chord_tools import *

port = int(sys.argv[1])

chord_data = {}

nb_get = 0
nb_update = 0
nb_gestion = 0


def get(key, ip, port):
    global nb_get
    data = chord_data.get(key)
    if data:
        json_send(ip, port, {'type': 'resp', 'key': key, 'val': data})
    else:
        json_send(ip, port, {'type': 'resp', 'key': key, 'val': -1})
    nb_get += 1


def update(key, value, ip=None, port=None):
    global nb_update
    chord_data[key] = value
    print(f'Key {key} updated')

    if ip and port:
        # send ACK
        json_send(ip, port, {'type': 'respUpdateAck', 'key': key})
        nb_update += 1


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind(('', port))
    serversocket.listen(5)
    print('listening on port:', serversocket.getsockname()[1])
    while True:
        (clientsocket, address) = serversocket.accept()
        json_data = json_recv(clientsocket)
        print(json_data)

        type = json_data['type']

        if type == 'get':
            key_requested = json_data['key']
            print(f'Key {key_requested} requested')
            origin_ip = json_data['ip']
            origin_port = json_data['port']
            get(key_requested, origin_ip, origin_port)

        elif type == 'update':
            key_to_update = json_data['key']
            new_value = json_data['val']
            origin_ip = json_data['ip']
            origin_port = json_data['port']
            update(key_to_update, new_value, origin_ip, origin_port)

        elif type == 'quit':
            client_ip = json_data['ip']
            client_port = json_data['port']
            json_send(client_ip, client_port, {
                      'type': 'stat', 'get': nb_get, 'update': nb_update, 'gestion': nb_gestion, 'v': 1})
