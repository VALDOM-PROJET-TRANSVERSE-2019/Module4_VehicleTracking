# The big picture
This repository is part of the ‘projet transverse’ of the [Advanced Master ValDom](http://www.enseeiht.fr/fr/formation/masteres-specialises/valorisation-des-donnees-massives.html) which is co-accredited by INP-ENSEEIHT and INSA Toulouse.

This year (2019/2020) the goal of the project is to develop a video analysis service. The main functionality is the recognition and tracking of vehicles in order to be able to estimate the emission rate (Co2) produced by traffic in the areas concerned.

# Module4: Suividesvéhicules
1. Objectif du module

Ce module permet de faire le lien entre les mêmes véhicules présents sur différentes images. Un identifiant est généré pour chaque véhicule et lui sera attribué de la première image liée à son apparition jusqu’à la dernière image liée à sa disparition.

2. Intégration et interactions avec les autres modules
Ce module prend en entrée un ensemble d’images du trafic routier, les métadonnées correspondantes ainsi que les données générées par le module de détection de véhicules. En sortie il génère une collection MongoDB associant pour chaque véhicule détecté sur les images, un identifiant unique permettant son suivi.

 3. Mise en application
Nous avons décidé qu’il était nécessaire que le module puisse détecter le sens des routes en utilisant les objets qui se déplacent. En détectant le sens des routes, il devient plus simple d’utiliser cette information pour le suivi des véhicules pour éviter les mauvaises correspondances.
Nous avons choisi que le module a besoin de deux modes distincts, en fonction du déplacement des véhicules dans la vidéo : Un mode circulation rapide et un mode embouteillage.
Lors du mode circulation rapide, nous considérons qu’un véhicule dont la position est déterminée par sa box générée par YOLO sur une image i1, sera le même que celui représenté par la box ayant la position la plus proche pour l’image i2. Lorsque la box est trop petite, on ne considère plus les nouvelles voitures potentielles pour éviter les inconsistances qui peuvent venir de la distance.
Le mode embouteillage doit garder un suivi plus précis sur les véhicules. En fonction de l’angle de la vidéo, il est possible d’avoir des véhicules qui se retrouvent cachés derrière d’autres et qui ne sont pas détectés par YOLO pendant un certain nombre de frame. Pour garder le suivit, il faut prendre une plus grande attention à la position de la bounding box, qui doit rester très proche d’une frame à l’autre, et faire attention aux véhicules qui disparaissent ou réapparaissent avant d’être éloignés.

4. Risques et limites
Pour l’implémentation de ce module, nous partons du principe que le nombre de frame par seconde extraits de la vidéo est suffisant pour faire un suivi des véhicules. En effet, la mise en place du suivi de véhicule est très dépendante du nombre de frame de la vidéo à la seconde. S’il est bas, il devient compliqué de suivre les véhicules en utilisant uniquement la proximité des bounding box.
Nous avons aussi considéré que la caméra était fixe. Si la caméra n’est pas fixe, le module de détection des routes ne fonctionne pas, et ne pourra par conséquent, pas être utilisé.
Dans le cas d’un accident ou d’une panne, les véhicules concernés vont être pris en compte un trop grand nombre de fois alors qu’ils sont à l’arrêt. Des solutions devront être implémentées comme une limite du nombre d’images consécutives ou une limite de temps pour la présence de chaque véhicule
