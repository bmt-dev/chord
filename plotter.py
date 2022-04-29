import matplotlib.pyplot as plt
from csv import reader
import json


# [nb_noeud, version, [get, put, gestion]]

nb_noeud = []

data = {}

with open('stats.csv', 'r') as read_obj:
    readed_line = 0
    csv_reader = reader(read_obj)
    for row in csv_reader:
        if readed_line == 10:
            break
        row = [int(elt) for elt in row]
        nb_noeud.append(row[0])
        try:
            data[row[0]][row[1]] = [row[2], row[3], row[4]]
        except:
            data[row[0]] = {}
            data[row[0]][row[1]] = [row[2], row[3], row[4]]
        # print(row)
        readed_line += 1

# print(data)


with open('data.json', 'w') as f:
    json.dump(data, f)


version_2 = 2
version_3 = 3

get_chart = plt.figure('Get')
plt.plot(nb_noeud, [data[n][version_2][0] for n in nb_noeud],
         marker='o', label='version ' + str(version_2))
plt.plot(nb_noeud, [data[n][version_3][0] for n in nb_noeud],
         marker='o', label='version ' + str(version_3))
plt.title('Nombre de get en fonction du nombre de noeuds')
plt.xlabel('Nb de noeuds')
plt.ylabel('Nb de get')
plt.legend(loc='best')
plt.savefig('get.png')

update_chart = plt.figure('Update')
plt.plot(nb_noeud, [data[n][version_2][1] for n in nb_noeud],
         marker='o', label='version ' + str(version_2))
plt.plot(nb_noeud, [data[n][version_3][1] for n in nb_noeud],
         marker='o', label='version ' + str(version_3))
plt.title('Nombre de update en fonction du nombre de noeuds')
plt.xlabel('Nb de noeuds')
plt.ylabel('Nb de update')
plt.legend(loc='best')
plt.savefig('update.png')

gestion_chart = plt.figure('Gestion')
plt.plot(nb_noeud, [data[n][version_2][2] for n in nb_noeud],
         marker='o', label='version ' + str(version_2))
plt.plot(nb_noeud, [data[n][version_3][2] for n in nb_noeud],
         marker='o', label='version ' + str(version_3))
plt.title('Nombre de gestion en fonction du nombre de noeuds')
plt.xlabel('Nb de noeuds')
plt.ylabel('Nb de gestion')
plt.legend(loc='best')
plt.savefig('gestion.png')

plt.show()
