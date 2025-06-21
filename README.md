GESTION DE STOCK ET PLATEFORME DE TUTORAT
=========================================

DESCRIPTION DES PROJETS
-----------------------

1. PROJET GESTION DE STOCK (C)
-----------------------------
Ce programme console permet de gérer un inventaire de produits. Il fonctionne comme un système de base de données simple où vous pouvez :

- Enregistrer de nouveaux produits avec :
  * Un ID unique
  * Un nom de produit
  * Un prix
  * Une quantité en stock

- Modifier les informations existantes
- Supprimer des produits
- Rechercher des articles par ID ou nom
- Visualiser tout le stock trié par ordre alphabétique
- Sauvegarder automatiquement les données

Le programme vérifie que les entrées sont valides (pas de prix négatifs, ID uniques...) et garde les données entre deux utilisations grâce à un fichier de sauvegarde.

2. PLATEFORME DE TUTORAT (Python/Tkinter)
-----------------------------------------
Cette application graphique sert d'interface pour mettre en relation :

Les tuteurs peuvent :
- Créer un profil avec leurs informations
- Indiquer quelles matières ils enseignent
- Préciser leurs heures de disponibilité

Les étudiants peuvent :
- Rechercher des tuteurs par matière, niveau
- Voir les disponibilités de chaque tuteur
- Consulter l'historique des sessions passées

L'interface est conviviale et intuitive, avec des menus clairs et des options de filtrage pratiques.

COMMENT UTILISER
---------------

Gestion de stock :
1. Compiler : gcc Gestion_de_stock.c -o gestion_stock
2. Lancer : ./gestion_stock
3. Suivre les instructions du menu

Plateforme de tutorat :
1. Lancer : python tutorat.py
2. Utiliser les boutons et menus de l'interface

FICHIERS INCLUS
---------------
- Gestion_de_stock.c : Code source du programme C
- stock.txt : Fichier de sauvegarde des produits
- tutorat.py : Code source de l'application Python

ÉQUIPE
------
DEMBELE Gaethan Khaleb

 DRABO Amine Farel Isao

KABORE Albertine

KABORE Karelle Aurelie 2eme Jumelle

KABORE Tegwende Odiane Elia Aziliz
