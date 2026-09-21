# Alchemy Labomatik

Alchemy Labomatik est un projet personnel développé en **Python** et **SQLite** autour d'un **système d'alchimie** destiné à un jeu vidéo.

Le projet sert à expérimenter et construire progressivement différents systèmes de gameplay : gestion des ingrédients, inventaire, affinités, mélange, découverte de recettes, fabrication et progression.

Le projet est actuellement en développement.


## Technologies

- Python
- SQLite
- Git / GitHub


## Fonctionnalités actuelles


### Gestion des ingrédients

Les ingrédients possèdent notamment :

- un nom ;
- une description ;
- un niveau ;
- une rareté ;
- une ou plusieurs affinités.

Les **affinités** sont associées aux ingrédients par une **relation many-to-many** via une table de liaison.

Chaque association possède une valeur représentant la contribution de l'ingrédient à l'affinité concernée.


### Raretés

Les ingrédients et équipements utilisent un **système de rareté**.

Chaque rareté possède :

- un nom ;
- une couleur d'affichage ;
- un poids utilisé pour les sélections aléatoires.

Les **poids** permettent notamment de réaliser une **sélection aléatoire pondérée** lors de la récupération d'ingrédients.


### Inventaire

L'inventaire conserve les quantités actuellement possédées par le joueur.

Les ingrédients sont identifiés par leur ingredient_id et leur quantité.

Le système permet notamment d'ajouter des quantités à l'inventaire et prépare leur consommation lors des mélanges et fabrications.


### Portails

Les portails permettent au joueur de **récupérer des ingrédients**.

Chaque portail est associé à une **affinité**.

La sélection des ingrédients disponibles dépend notamment :

- de l'affinité du portail ;
- du niveau du joueur ;
- de la valeur d'affinité de l'ingrédient ;
- de la rareté.

Les ingrédients sont sélectionnés aléatoirement avec une pondération basée sur leur rareté.


## Matériel d'alchimie

Le matériel est organisé en plusieurs catégories :

- Instruments ;
- Creusets ;
- Feux ;
- Contenants.

Le matériel possède un **catalogue de référence** décrivant ses caractéristiques.

Certains instruments de mélange possèdent également une capacité définissant le nombre d'ingrédients qu'ils peuvent accepter.

### Mélange

Le système de mélange permet au joueur :

- de choisir un instrument ;
- de sélectionner les ingrédients ;
- de mélanger les ingrédients ;
- de calculer la signature d'affinités du mélange.

La **capacité de l'instrument*** détermine le **nombre d'ingrédients** pouvant être mélangés.

Les valeurs d'affinité des ingrédients sélectionnés sont additionnées puis normalisées afin d'obtenir la signature finale du mélange.


### Recettes

Les recettes possèdent notamment :

- un nom ;
- un type ;
- une cible ;
- une description ;
- un effet ;
- une rareté ;
- un éventuel feu requis ;
- un éventuel creuset requis.

Les types de recettes actuellement prévus sont **Potion**, **Élixir** et **Pentagramme**.

Les cibles actuellement disponibles sont Soi, Allié, Équipe, Ennemi, Tous les ennemis.


### Découverte de recettes

La découverte d'une recette repose sur la **signature d'affinités du mélange** et sur le **nombre d'ingrédients utilisés**.

Les conditions de découverte sont stockées séparément des recettes afin de pouvoir définir des critères de découverte indépendamment de leur fabrication.

La fabrication d'une recette constitue une étape distincte de sa découverte.


## Structure de la base de données

La base de données SQLite contient actuellement plusieurs tables permettant de séparer les différentes responsabilités du système.

### Principales tables :

```bash
affinities
ingredients
ingredient_affinities
rarities
inventory

equipment
equipment_categories
equipment_craft
mixing_tools

recipe_types
targets
recipes
recipe_discovery
```
### Liaisons :

Le projet utilise des clés étrangères pour maintenir les relations entre les différentes tables.

Les tables de liaison permettent notamment de représenter les relations entre :

- ingrédients et affinités ;
- équipements et ingrédients utilisés pour leur fabrication.
- Catalogue, disponibilité et possession

Le projet distingue progressivement trois notions :

```bash
CATALOGUE
    |
    | définition de l'objet
    v
DISPONIBILITÉ
    |
    | progression / déblocage
    v
INVENTAIRE
    |
    | quantité possédée
    v
UTILISATION
```

**Le catalogue** décrit les objets existant dans le jeu.

**La disponibilité** détermine quels objets sont accessibles au joueur.

**L'inventaire** représente les objets actuellement possédés et disponibles pour être utilisés.

Cette distinction sera notamment utilisée pour les **contenants**, qui peuvent être fabriqués puis utilisés comme composants lors de la fabrication d'autres objets.


## État du projet

Le projet est actuellement au stade de prototypage et de développement du modèle de données.

Les principaux systèmes déjà mis en place sont :

- Base de données SQLite
- Données de référence
- Affinités
- Ingrédients
- Raretés
- Inventaire
- Portails
- Matériel d'alchimie
- Catégories de matériel
- Outils de mélange
- Calcul de la signature d'affinités
- Types de recettes
- Cibles
- Recettes
- Conditions de découverte des recettes
- Consommation des ingrédients
- Fabrication des contenants
- Fabrication des recettes
- Système de disponibilité du matériel
- Progression du joueur
- Système complet de découverte des recettes
- Sauvegarde de la base de données

La base SQLite utilisée pendant le développement est conservée localement et n'est pas versionnée directement.

Un **dump SQL** de la base est utilisé pour conserver des snapshots versionnés de son état :

```bash
database.db
     |
     | dump SQL
     v
database_backup.sql
     |
     v
Git / GitHub
```

Cela permet de conserver une version reconstruisible de la base tout en gardant la base SQLite de travail hors du dépôt Git.

## À venir

Les prochaines étapes concernent notamment :

- la consommation des ingrédients lors des mélanges ;
- la fabrication et le stockage des contenants dans l'inventaire ;
- la fabrication et le stockage du matériel dans une table dédiée ;
- la gestion de la disponibilité du matériel ;
- la fabrication des recettes ;
- la finalisation du système de découverte ;
- la progression du joueur ;
- l'enrichissement du contenu alchimique.

Le projet servira de base à une intégration ultérieure dans Funky Final Fantasy (FFF) pour alimenter un artisanat.