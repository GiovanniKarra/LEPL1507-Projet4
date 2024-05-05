### INTERFACE GRAPHIQUE

Pour run l'appli, il faut run `main.py` avec un interpréteur python, et avec les packages `PyQt5` et `matplotlib` installés.

Pour apprendre à utiliser l'appli, appuyez sur le bouton `Help` du menu du haut.

Pour run sans interpréteur, il faut build dans le dossier `build` en utilisant le Makefile. Il suffit d'utiliser la commande `make` pour compiler l'application, et puis run `dist/main/main`, et `make clean` pour nettoyer le dossier build. Pour build il faut avoir le package `pyinstaller`.