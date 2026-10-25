# ALCHEMY LAB-O-MATIK (A-LAB pour les intimes)

## 🎮 Présentation du jeu

**ALCHEMY LAB-O-MATIK (A-LAB)** est un jeu de gestion et d'expérimentation alchimique en terminal, développé en **Python** avec une base de données **SQLite**.

Le joueur incarne un alchimiste chargé de découvrir des recettes, de fabriquer des préparations et de développer son laboratoire.

Pour progresser, il devra explorer des portails, récolter des ingrédients aux propriétés mystérieuses, expérimenter différentes combinaisons et améliorer son matériel.

Mais l'alchimie n'est pas qu'une affaire de science occulte : entre les fournisseurs douteux de Flamel Industries, les campagnes publicitaires invasives et les exigences commerciales de la Youtique©, le laboratoire devra également composer avec les absurdités du monde de l'entreprise.

## ⚗️ Fonctionnalités principales

### 🌀 Exploration des portails
- Explorer différents portails pour récolter des ingrédients.
- Découvrir des ressources de raretés et d'affinités variées.
- Faire face à des événements aléatoires au cours des explorations.

### 🧪 Laboratoire
- Expérimenter des mélanges d'ingrédients avec différents instruments.
- Exploiter les affinités alchimiques pour découvrir de nouvelles recettes.
- Consulter les indices de découverte dans le carnet de laboratoire.

### 🧫 La Popotte
- Fabriquer des potions, élixirs et pentagrammes à partir des recettes découvertes.
- Utiliser les ingrédients, produits intermédiaires et équipements requis.
- Conserver les créations dans l'inventaire ou les destiner à la vente.

### 🥽 La Fonderie
- Fabriquer des instruments de mélange, des feux et des creusets.
- Débloquer progressivement de nouveaux équipements.
- Développer les capacités de fabrication du laboratoire.

### 🌐 FlamelXpress©
- Acheter les contenants nécessaires aux préparations.
- Découvrir les offres et publicités de l'incontournable fournisseur alchimique.

### 🐍 La Youtique©
- Gérer les produits destinés à la vente.
- Transférer les préparations entre l'inventaire et la boutique.
- Générer des revenus grâce aux ventes.
- Consulter les statistiques commerciales : chiffre d'affaires, quantités vendues et classement des produits.

### 📈 Progression et objectifs

Le jeu propose un suivi détaillé de la progression du joueur :

- **Découvertes alchimiques :** statistiques sur les recettes découvertes, réparties selon la complexité des mélanges.
- **Fabrication :** suivi des préparations déjà réalisées et de celles restant à fabriquer.
- **Exploration :** suivi des ingrédients débloqués et de ceux qui n'ont jamais été récoltés.
- **Objectifs de victoire :** accomplissements à débloquer pour progresser vers la réussite du laboratoire.
- **Hauts faits commerciaux :** défis consistant à commercialiser des collections de préparations spécifiques.

Les objectifs affichent leur état d'avancement et permettent au joueur de consulter sa progression sans révéler les recettes qu'il n'a pas encore découvertes.

## 🕹️ Comment jouer

Le jeu se contrôle entièrement au clavier, à travers des menus numérotés.

1. **Explorez les portails** pour récolter vos premiers ingrédients.
2. **Rendez-vous au laboratoire** pour expérimenter des mélanges et découvrir des recettes.
3. **Fabriquez de nouveaux équipements** afin d'améliorer vos possibilités d'expérimentation.
4. **Préparez vos créations** dans la Popotte, en réunissant les ressources nécessaires.
5. **Développez votre activité commerciale** avec la Youtique©.
6. **Accomplissez les objectifs** pour progresser dans votre carrière d'alchimiste.

La progression est enregistrée dans une base de données SQLite. Une option du menu principal permet également de réinitialiser la partie.


## Installation et lancement

### Prérequis

- Python 3
- SQLite (intégré à la bibliothèque standard de Python)

### Lancement depuis le code source

Depuis le répertoire du projet, exécuter :

```bash
python main.py
```

Au démarrage, le programme se connecte à la base de données SQLite `database.db`, crée les tables manquantes et initialise les données nécessaires au joueur.

Le menu principal s'affiche ensuite et permet d'accéder aux différentes fonctionnalités du jeu.

### Sauvegarde

La progression du joueur est conservée dans la base de données SQLite `database.db`, située à la racine du projet.


# RUBRIQUE "SOUS LE CAPOT"

## 🛠️ Technologies utilisées

- Python 3
- SQLite
- Bibliothèque standard Python

## 🗄️ Architecture de la base de données

Le jeu utilise une base de données relationnelle SQLite
pour gérer les recettes, ingrédients, équipements,
inventaires, découvertes et progression du joueur.

![Schéma relationnel de la base de données](sql%20map.png)

## 📁 Organisation du projet
```bash
ALCHEMY LAB-O-MATIK/
├── database/                Création de la structure de la base et sauvegarde SQL
├── data_management/         Accès et gestion des données du jeu
├── display/                 Fonctions d'affichage dans le terminal
├── player_game/             Mécaniques de jeu : exploration, mélange, fabrication, commerce
│   └── game_functions/      Initialisation, gestion du temps, état et réinitialisation de la partie
├── database.db
├── database_backup.sql
├── main.py
├── menu.py
├── menu_data.py
├── utils.py
└── README.md
```