# The big picture
This repository is part of the ‘projet transverse’ of the [Advanced Master ValDom](http://www.enseeiht.fr/fr/formation/masteres-specialises/valorisation-des-donnees-massives.html) which is co-accredited by INP-ENSEEIHT and INSA Toulouse.

This year (2019/2020) the goal of the project is to develop a video analysis service. The main functionality is the recognition and tracking of vehicles in order to be able to estimate the emission rate (Co2) produced by traffic in the areas concerned.

# Module4: Suividesvéhicules
1. Objectif du module

Ce module permet de faire le lien entre les mêmes véhicules présents sur différentes images. Un identifiant est généré pour chaque véhicule et lui sera attribué de la première image liée à son apparition jusqu’à la dernière image liée à sa disparition.

2. Fonctionnement du module

Le module va chercher aux chemins désignés:
* un ensemble d'images.
* les détections de véhicules associées à ces images.

//todo explication tracker

3. API du module

Une interface de type REST (GET), qui prends en argument les chemins vers les images et les véhicules détectés.
Renvoi en sortie, un fichier json, qui contient image par image, les identifiants uniques des véhicules détectés:
```json
{
  "frame 0": [0,1],
  "frame 1": [0,1],
  "frame 2": [1],
  "frame 3": [2],
  "frame 4": [2,3],
  "frame 5": []
 }
```


4. Déploiement du module

* Via docker:
```shell script
bash run_container.sh
```

* En local:
```shell script
pip install -r requirements.txt
python run.py
```

Des requètes peuvent être envoyées au module via son addresse par défaut localhost:5000.
