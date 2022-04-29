# Pour lancer le programme il faut faire :

* `python chord_v3.py 10000` pour le cercle initial
* `python chord_v3.py 12000 127.0.0.1 10000` pour se joindre
  
# Si vous êtes sur Windows, lancer juste `script.cmd`.

* Spécifier dans le bloc `if` la valeur de `loopcount` qui correspond au nombre de noeuds souhaités.
* Spécifier dans `chord_version` la version souhaitée.

# Envoi de requêtes
Il suffit de faire `python chord_client.py`.
Enfin d'enregistrer les données pour la visualisation, il faut spécifier dans le bloc `with` la valeur de `nb_nodes` qui doit correspondre au nombre de noeuds lancés.

# Visualisation
`python plotter.py`
