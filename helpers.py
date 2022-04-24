import random
import threading

# k = 16
k = 4
MAX = 2**k  # 0 .. 2^k - 1


def get_keys_to_distribute(d, init, end):
    return {k: v for _, (k, v) in enumerate(d.items()) if betweenE(hash(k), init, end)}


def remove_key_from_dict(d, keys):
    for key in keys:
        del d[key]


def between(value, init, end):
    if init == end:
        return True
    elif init > end:
        shift = MAX - init
        init = 0
        end = (end + shift) % MAX
        value = (value + shift) % MAX
    return init < value < end


def betweenE(value, init, end):
    if value == end:
        return True
    else:
        return between(value, init, end)


def Ebetween(value, init, end):
    if value == init:
        return True
    else:
        return between(value, init, end)


def generate_random_data(amount: int = 5):
    if amount > MAX:
        print('5 keys generated')
        amount = 5
    keys = random.sample(range(0, MAX), amount)
    values = random.sample(range(0, 2**k * 15), amount)
    return dict(zip(keys, values))


def hash(key):
    try:
        return int(key) % MAX
    except:
        print('Bad key passed')


class NodeStat:
    '''
    Permet d'obtenir le nombre de communications par type de requêtes (get, update) ainsi que pour la gestion de
    l’infrastructure (communications dues à l’arrivée/au départ des noeuds).
    '''

    def __init__(self, version: int) -> None:
        self.version = version
        self.nb_get = 0
        self.nb_update = 0
        self.nb_gestion = 0

    def new_get(self):
        self.nb_get += 1

    def new_update(self):
        self.nb_update += 1

    def new_gestion(self):
        self.nb_gestion += 1


class InputThread(threading.Thread):
    def __init__(self, node_id, callback):
        super(InputThread, self).__init__()
        self.daemon = True
        # self.last_user_input = None
        self.id = node_id
        self.callback = callback

    def run(self):
        while True:
            print('--- Choisir une commande ---')
            print('[I]nfo')
            print('[P]rédecesseur')
            print('[S]uccesseur')
            print('[T]able de voisinage')
            print('[C]lés en ma possession')
            print('[Q]uitter')
            cmd = input('NODE_' + str(self.id) + '> ')
            self.callback(cmd)
