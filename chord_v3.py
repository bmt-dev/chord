#! /usr/bin/python3

# run command : (init) python chord_v3.py 10000 ; (join) python chord_v3.py 12000 127.0.0.1 10000

import sys
import socket
import json
from helpers import *


class Node:
    def __init__(self, node_id, node_ip='127.0.0.1', node_port=int(sys.argv[1])) -> None:
        self.id = node_id
        self.ip = node_ip
        self.port = node_port
        self.predecessor = self
        self.finger = {}
        self.start = {}
        for i in range(k):
            self.start[i] = (self.id+(2**i)) % (2**k)  # on génère les id + 2^i
        self.chord_data = {}
        self.stat = NodeStat(2)

    def get_successor(self):
        return self.finger[0]

    def get_predecessor(self):
        return self.predecessor

    def set_successor(self, node):
        self.finger[0] = node

    def set_predecessor(self, node):
        self.predecessor = node

    def show_finger(self):
        try:
            from prettytable import PrettyTable
            print('Table de voisinage noeud ' + str(self.id))
            t = PrettyTable(['Début', 'Successeur'])
            for i in range(k):
                t.add_row([self.start[i], self.finger[i].id])
            print(t)

        except:
            print('-----------')
            print('Table de voisinage noeud ' + str(self.id))
            print('début : successeur')
            for i in range(k):
                print(str(self.start[i]) + ' : ' + str(self.finger[i].id))
            print('-----------')

    def set_data(self, data):
        try:
            self.chord_data = {int(k): int(v)
                               for _, (k, v) in enumerate(data.items())}
        except:
            print('Incorrect data type')

    def get(self, key, ip, port):
        print(f'Responsible of {key}')
        data = self.chord_data.get(key)

        if data:
            self.send(ip, port, {'type': 'resp', 'key': key, 'val': data})
        else:
            self.send(ip, port, {'type': 'resp', 'key': key, 'val': -1})

    def update(self, key, value, ip=None, port=None):
        self.chord_data[key] = value
        print(f'Key {key} updated')

        if ip and port:
            # return ack
            self.send(ip, port, {'type': 'respUpdateAck', 'key': key})

    def console(self, cmd):
        if cmd.lower() == 'i':
            print('Je suis le noeud ' + str(self.id) + ', IP: ' + self.ip + ', PORT: ' + str(self.port))
        elif cmd.lower() == 'p':
            print('Mon prédecesseur :\n ID: ' + str(self.get_predecessor().id) + ', IP: ' + self.get_predecessor().ip + ', PORT: ' + str(self.get_predecessor().port))
        elif cmd.lower() == 's':
            print('Mon successeur :\n ID: ' + str(self.get_successor().id) + ', IP: ' + self.get_successor().ip + ', PORT: ' + str(self.get_successor().port))
        elif cmd.lower() == 't':
            self.show_finger()
        elif cmd.lower() == 'c':
            print('Je gère : ', self.chord_data)
        elif cmd.lower() == 'q':
            ...
        else:
            print('Mauvaise commande, Réessayer')

    def send(self, ip, port, data):
        print('Sending [' + data['type'] + '] request to ' +
              ip + ' ' + str(port))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.send(json.dumps(data).encode())

            type = data['type']

            if type == 'get':
                self.stat.new_get()

            if type == 'update':
                self.stat.new_update()

    def recv(self, clientsocket):
        data = b''
        while True:
            tmp = clientsocket.recv(1024)
            if tmp == b'':
                break
            data += tmp
        result = json.loads(data)
        print('[' + result['type'] + '] received')

        type = result['type']

        if type != 'get' and type != 'update':
            # other msg (plop, ok, nok, ...)
            self.stat.new_gestion()

        return result

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
            serversocket.bind((self.ip, self.port))
            serversocket.listen(5)
            print('Adresse IP: ' + self.ip + ', Port No: ' + str(self.port))
            # print('listening on port:', serversocket.getsockname()[1])

            if len(sys.argv) == 2:
                self.chord_data = generate_random_data(amount=50)
                print(f'Initial chord node ID : {self.id}')
                print('Stored keys : ', self.chord_data)

                for i in range(k):
                    self.finger[i] = self

            elif len(sys.argv) == 4:
                existing_node_ip = sys.argv[2]
                existing_node_port = int(sys.argv[3])
                print(f'Joining chord ring with ID : {self.id}')
                self.send(existing_node_ip, existing_node_port, {'type': 'joind',
                                                                 'id': self.id, 'ip': self.ip, 'port': self.port})

            else:
                print('Bad arguments passed')
                sys.exit(1)

            InputThread(self.id, self.console).start()

            while True:
                (clientsocket, address) = serversocket.accept()
                json_data = self.recv(clientsocket)
                print(json_data)

                type = json_data['type']

                if type == 'get':
                    key_requested = json_data['key']
                    print(f'Key {key_requested} requested')
                    origin_ip = json_data['ip']
                    origin_port = json_data['port']

                    # je verifie est ce que je gere la clé demandée
                    if betweenE(hash(key_requested), self.get_predecessor().id, self.id):
                        self.get(key_requested, origin_ip, origin_port)
                    else:
                        # sinon j'envoie la requete à mon successeur
                        print(f'I\'m not responsible of {key_requested}')
                        print('Sending request to successor Node ' +
                              str(self.get_successor().id))
                        self.send(self.get_successor().ip, self.get_successor().port, {
                            'type': 'get', 'key': key_requested, 'ip': origin_ip, 'port': origin_port})

                elif type == 'update':
                    key_to_update = json_data['key']
                    new_value = json_data['val']
                    origin_ip = json_data['ip']
                    origin_port = json_data['port']

                    if betweenE(hash(key_to_update), self.get_predecessor().id, self.id):
                        self.update(key_to_update, new_value,
                                    origin_ip, origin_port)
                    else:
                        print(f'I\'m not responsible of {key_to_update}')
                        print('Sending request to successor Node ' +
                              str(self.get_successor().id))
                        self.send(self.get_successor().ip, self.get_successor().port, {
                            'type': 'update', 'key': key_to_update, 'val': new_value, 'ip': origin_ip, 'port': origin_port})

                elif type == 'joind':
                    # un noeud veut se joindre
                    node_join_id = json_data['id']
                    node_join_ip = json_data['ip']
                    node_join_port = json_data['port']

                    if node_join_id == self.id:
                        self.send(node_join_ip, node_join_port,
                                  {'type': 'nok'})

                    elif betweenE(node_join_id, self.get_predecessor().id, self.id):
                        data_to_send = get_keys_to_distribute(
                            self.chord_data, self.get_predecessor().id, node_join_id)

                        if data_to_send:
                            print(
                                f'Migrating keys {list(data_to_send.keys())} to Node {node_join_id}')
                            # remove all the keys we do not own any more
                            remove_key_from_dict(
                                self.chord_data, data_to_send.keys())

                        self.send(node_join_ip, node_join_port, {
                            'type': 'ok', 'idp': self.get_predecessor().id, 'ipp': self.get_predecessor().ip, 'portp': self.get_predecessor().port, 'ids': self.id, 'ipps': self.ip, 'ports': self.port, 'data': data_to_send})

                        node = Node(node_join_id, node_join_ip, node_join_port)
                        self.set_predecessor(node)

                        print('Stored keys : ', self.chord_data)

                    else:
                        # send request to successor
                        self.send(self.get_successor().ip, self.get_successor().port, {
                            'type': 'joind', 'id': node_join_id, 'ip': node_join_ip, 'port': node_join_port})

                elif type == 'nok':
                    print('Cannot join the chord ring')

                    # try again with another id
                    # TODO

                elif type == 'ok':
                    # set predecessor
                    node = Node(json_data['idp'],
                                json_data['ipp'], json_data['portp'])
                    self.set_predecessor(node)

                    # init finger table
                    node = Node(json_data['ids'],
                                json_data['ipps'], json_data['ports'])
                    self.set_successor(node)  # finger 0

                    for i in range(1, k):
                        self.send(self.get_successor().ip, self.get_successor().port, {
                                  'type': 'ckikigere', 'key': self.start[i], 'ip': self.ip, 'port': self.port})

                    # set keys
                    self.set_data(json_data['data'])

                    print(f'Chord ring joined with ID : {self.id}')
                    print('Stored keys : ', self.chord_data)

                    # send plop
                    self.send(self.get_successor().ip, self.get_successor().port, {
                        'type': 'plop', 'id': self.id, 'ip': self.ip, 'port': self.port})

                elif type == 'plop':
                    plop_id = json_data['id']
                    plop_ip = json_data['ip']
                    plop_port = json_data['port']

                    if self.id != plop_id:
                        # on a pas fini de faire le tour du cercle
                        print(
                            f'Le noeud {plop_id} vient d\'arriver.\nBienvenue noeud {plop_id} !')

                        for i in range(k):
                            if betweenE(plop_id, self.id, self.finger[i].id):
                                # je mets à jour ma table
                                node = Node(plop_id, plop_ip, plop_port)
                                self.finger[i] = node

                        # send plop to the next node
                        self.send(self.get_successor().ip, self.get_successor().port, {
                            'type': 'plop', 'id': plop_id, 'ip': plop_ip, 'port': plop_port})

                    print('Mon prédécesseur : ', self.get_predecessor().id)
                    print('Mon successeur : ', self.get_successor().id)

                elif type == 'ckikigere':
                    requested_key = json_data['key']
                    origin_ip = json_data['ip']
                    origin_port = json_data['port']
                    if betweenE(requested_key, self.get_predecessor().id, self.id):
                        self.send(origin_ip, origin_port, {
                                  'type': 'jegere', 'key': requested_key, 'id': self.id, 'ip': self.ip, 'port': self.port})
                    else:
                        self.send(self.get_successor().ip, self.get_successor().port, {
                                  'type': 'ckikigere', 'key': requested_key, 'ip': origin_ip, 'port': origin_port})

                elif type == 'jegere':
                    key = json_data['key']
                    finger_id = json_data['id']
                    finger_ip = json_data['ip']
                    finger_port = json_data['port']

                    self.finger[list(self.start.keys())[list(self.start.values()).index(
                        key)]] = Node(finger_id, finger_ip, finger_port)

                elif type == 'quit':
                    # le client envoie la commande quit pour récupérer les statistiques et faire quitter les noeuds chord
                    # on doit connaitre l'id du noeud qui a recu le quit du client pour nous assurer de faire le tour du cercle
                    client_ip = json_data['ip']
                    client_port = json_data['port']
                    _id = json_data.get('id')

                    if _id:
                        # j'ai reçu le quit d'un noeud du cercle
                        if self.id != _id:
                            # on a pas fini de faire le tour du cercle
                            current_get = json_data['get']
                            current_update = json_data['update']
                            current_gestion = json_data['gestion']
                            self.send(self.get_successor().ip, self.get_successor().port, {'type': 'quit', 'ip': client_ip, 'port': client_port, 'id': _id, 'get': self.stat.nb_get + current_get,
                                      'update': self.stat.nb_update + current_update, 'gestion': self.stat.nb_gestion + current_gestion})

                            print(f'Closing Node {self.id}')
                            sys.exit(0)
                        else:
                            # le quit a fait le tour du cercle, j'envoie au client les statistiques
                            self.send(client_ip, client_port, {
                                'type': 'stat', 'get': json_data['get'], 'update': json_data['update'], 'gestion': json_data['gestion']})

                            print(f'Closing Node {self.id}')
                            sys.exit(0)

                    else:
                        # j'ai reçu le quit du client
                        self.send(self.get_successor().ip, self.get_successor().port, {
                            'type': 'quit', 'ip': client_ip, 'port': client_port, 'id': self.id, 'get': self.stat.nb_get, 'update': self.stat.nb_update, 'gestion': self.stat.nb_gestion})

                else:
                    print('BAD COMMAND')

                print('--- Choisir une commande ---')
                print('[I]nfo')
                print('[P]rédecesseur')
                print('[S]uccesseur')
                print('[A]fficher la table de voisinage')
                print('[C]lés en ma possession')
                print('[Q]uitter')
                print('NODE_' + str(self.id) + '> ', end='')


if __name__ == '__main__':
    node_id = random.randint(0, MAX - 1)
    n = Node(node_id)
    n.run()
