# Documentation

## *Le script reparateur.py*

&nbsp;

## Introduction

---

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ce script permet de modifier le fichier de sortie du logiciel ARX afin de le rendre compatible avec les metrics d'évaluation.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Il prend en paramètre un nom de fichier, sans l'extension .csv qui doit se trouver dans le répertoire /csv et créer un fichier dans ce même répertoire de la forme : "fichier_rep.csv".

&nbsp;

## Utilisation

---

1. Mettre le fichier que l'on souhate réparer dans le dosier **csv/**.

2. Régler les paramètre de réparation en modifiant le fichier **reparateur.conf**.

3. Lancer le script **reparateur.py** en précisant le nom du fichier que l'on réparer.
    * Exemple : pour le fichier anonyme.csv
        * `$ python reparateur.py anonyme`