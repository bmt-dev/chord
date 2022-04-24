#! /usr/bin/python3

import socket
import sys
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

            if json_data['type'] == 'stat':
                print('*** Statistiques ***')
                print('Requêtes get : ', json_data['get'])
                print('Requêtes update : ', json_data['update'])
                print('Gestion : ', json_data['gestion'])

                sys.exit(0)


printer_thread = threading.Thread(target=printer)
printer_thread.start()

data = [
    {
        'type': 'get',
        'key': 3,
        'ip': 'localhost',
        'port': 9000
    },
    {
        'type': 'update',
        'key': 80000,
        'val': 11,
        'ip': 'localhost',
        'port': 9000
    },
    {
        'type': 'get',
        'key': 18215,
        'ip': 'localhost',
        'port': 9000
    },
    {
        'type': 'get',
        'key': 36094,
        'ip': 'localhost',
        'port': 9000
    },
    {
        'type': 'get',
        'key': 80000,
        'ip': 'localhost',
        'port': 9000
    },
    {
        'type': 'quit',
        'ip': 'localhost',
        'port': 9000
    }
]

for d in data:
    json_send('localhost', 10000, d)
