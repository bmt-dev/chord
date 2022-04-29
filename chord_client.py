#! /usr/bin/python3

import csv
import random
import socket
import sys
import threading
from chord_tools import *

random.seed(900)

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
                chord_version = json_data['v']
                nb_get = json_data['get']
                nb_update = json_data['update']
                nb_gestion = json_data['gestion']

                print(f'*** Statistiques CHORD VERSION {chord_version} ***')
                print(f'Requêtes get : {nb_get}')
                print(f'Requêtes update : {nb_update}')
                print(f'Gestion : {nb_gestion}')

                with open('stats.csv', 'a', newline='') as f:
                    nb_nodes = 32  # specifier le nb de noeud lancés
                    wr = csv.writer(f)
                    wr.writerow([nb_nodes, chord_version,
                                nb_get, nb_update, nb_gestion])

                sys.exit(0)


printer_thread = threading.Thread(target=printer)
printer_thread.start()

requests = []

keys = [random.randint(0, 100000) for _ in range(100)]

for i in range(100):
    request = {
        'type': 'update',
        'key': keys[i],
        'val': random.randint(0, 100000),
        'ip': 'localhost',
        'port': 9000
    }        

    requests.append(request)

for i in range(100):
    request = {
        'type': 'get',
        'key': keys[i],
        'ip': 'localhost',
        'port': 9000
    }        

    requests.append(request)

# quitter à la fin
requests.append(
    {
        'type': 'quit',
        'ip': 'localhost',
        'port': 9000
    }
)

for request in requests:
    json_send('localhost', 10000, request)
