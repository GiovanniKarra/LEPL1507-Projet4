### Comment faire fonctionner les programmes de répartition de satellites:

Avant de lancer quoi que ce soit, il est conseillé de lire les docs string des fonctions `spherical_satellites_repartition` et `euclidean_satellites_repartition`, toutes les informations quant aux arguments et aux sorties sont repris dedans.

## Programme basique:

En sachant que les fonctions prennent en entrée le nombre de satellites à placer et un chemin vers un CSV contenant les informations sur les villes dans le bon format. 

Il est possible de run nos fonction `spherical_satellites_repartition` et `euclidean_satellites_repartition` de deux façons differentes:

La première est d'exécuter les fichiers, avec un interpreteur python, contenant les fonctions et de mettre les arguments voulu dans la partie `if __name__ == "__main__":` qui se trouve en bas des dits des fichiers. Un exemple de la section main pour chaque fonction pourrait être les suivantes: 

```Python
if __name__ == "__main__":
    N_satellites = 10
    file = "../test.csv"
    satellites_coordinates, covered_population = spherical_satellites_repartition(N_satellites, file)
```

ou

```Python
if __name__ == "__main__":
    N_satellites = 10
    # file = "../test.csv"
    satellites_coordinates, covered_population = euclidean_satellites_repartition(N_satellites, file)  
```

La deuxieme façon pourrait être d'appeler ces mêmes fonctions depuis un fichier python différent. Dans ce cas, si vous avez réalisé l'import de façon correcte, exemple:

```Python
from spherical_satellites_repartition import *
```

ou

```Python
from euclidean_satellites_repartition import *
```

Vous pourrez appeller la fonction normalement, toujours en lui donnant des arguments correct. De cette façons ci:

```Python
satellites_coordinates, covered_population = spherical_satellites_repartition(N_satellites, file)
```

ou 

```Python
satellites_coordinates, covered_population = euclidean_satellites_repartition(N_satellites, file)
```

## Programme avec arguments additionnel:

En sachant que les fonctions prennent en entrée le nombre de satellites à placer et un chemin vers un CSV contenant les informations sur les villes dans le bon format. Nous pouvons rajouter le reste des arguments, ceux-ci sont pré-initialisé a des valeurs cohérente physiquement parlant ou utile. Pour le détail de chaque argument la docstring des fonctions est toujours la pour vous aider. NB: si vous avez un rayon (R) en km, il est possible de retrouvé la valeur de "radius_acceptable" en fixant le "h" et ce grâce a cette conversion: ``radius_acceptable = sqrt((R/6371)^2+(h-1)^2)``

De nouveau, il est possible de run nos fonction `spherical_satellites_repartition` et `euclidean_satellites_repartition` de deux façons differentes:

La première est d'exécuter les fichiers, avec un interpreteur python, contenant les fonctions et de mettre les arguments voulu dans la partie `if __name__ == "__main__":` qui se trouve en bas des dits des fichiers. Un exemple de la section main avec plusieurs argument supplémentaire serai pour chaque fonction pourrait être les suivantes: 

```Python
if __name__ == "__main__":
    N_satellites = 10
    file = "../test.csv"
    satellites_coordinates, covered_population = spherical_satellites_repartition(N_satellites, file, grid_size=1000, verbose=True, visualise=True)
```

ou

```Python
if __name__ == "__main__":
    N_satellites = 10
    # file = "../test.csv"
    satellites_coordinates, covered_population = euclidean_satellites_repartition(N_satellites, file, grid_size=1000, verbose=True, radius_acceptable_km=200)  
```

La deuxieme façon pourrait être d'appeler ces mêmes fonctions depuis un fichier python différent. Dans ce cas, si vous avez réalisé l'import de façon correcte, exemple:

```Python
from spherical_satellites_repartition import *
```

ou

```Python
from euclidean_satellites_repartition import *
```

Vous pourrez appeller la fonction normalement, toujours en lui donnant des arguments correct. De cette façons ci:

```Python
satellites_coordinates, covered_population = spherical_satellites_repartition(N_satellites, file, grid_size=1000, verbose=True, visualise=True)
```

ou 

```Python
satellites_coordinates, covered_population = euclidean_satellites_repartition(N_satellites, file, grid_size=1000, verbose=True, radius_acceptable_km=200)  
```

## Interface graphique 

L'interface graphique possède son propre README.md qu'il est conseillé de lire avant utilisation. 