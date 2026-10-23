# Type	                                   Objectifs	                                        Nombre

# Découvertes	                 Toutes les recettes à 2, 3, 4, 5 et 6 ingrédients	                   5
# Fabrication	              Toutes les potions, tous les élixirs, tous les pentagrammes	           3
# Récolte	                       Tous les ingrédients possibles	                                   1
# Hauts faits	                                  cf plus bas	                                       5
# Total		                                                                                          14

# La "Gastro explosive" : avoir vendu tous les articles provoquant des troubles digestifs sévères.
# La "4 grammes" : avoir vend un exemplaire de chaque article conduisant directement en cellule de dégrisement.
# La "Raclée de sa mère" : avoir vendu tous les articles en rapport avec une prise de branlée monumentale.
# Le "Trou de la Sécu" : avoir vendu tous les articles remboursés par la Société d'Equilibration de la Cupelle.
# La "Focus sur les quick win" : avoir vendu tous les articles prédictifs d'une reconversion post-burnout en élevage caprin dans le Cantal.


from player_game.objectives import get_objective_discovered_recipes, get_total_recipes


achievements = [
    (1, "Le Maître des Mélanges", "victory", None),
    (2, "Mélanges à 2 ingrédients", "victory", 1),
    (3, "Mélanges à 3 ingrédients", "victory", 1),
    (4, "Mélanges à 4 ingrédients", "victory", 1),
    (5, "Mélanges à 5 ingrédients", "victory", 1),
    (6, "Mélanges à 6 ingrédients", "victory", 1),

    (7, "Le Collectionneur Compulsif", "victory", None),

    (8, "La Popotte Étoilée", "victory", None),
    (9, "Fabriquer toutes les potions", "victory", 8),
    (10, "Fabriquer tous les élixirs", "victory", 8),
    (11, "Fabriquer tous les pentagrammes", "victory", 8),

    (12, "La Gastro Explosive", "fun", None),
    (13, "La 4 Grammes", "fun", None),
    (14, "La Raclée de sa Mère", "fun", None),
    (15, "Le Trou de la Sécu", "fun", None),
    (16, "Le Focus sur les Quick-Win", "fun", None),
]


commercial_descriptions = {
    12: "Avoir vendu tous les articles provoquant des troubles digestifs sévères.",
    13: "Avoir vendu un exemplaire de chaque article conduisant directement en cellule de dégrisement.",
    14: "Avoir vendu tous les articles en rapport avec une prise de branlée monumentale.",
    15: "Avoir vendu tous les articles remboursés par la Société d'Équilibration de la Cupelle.",
    16: "Avoir vendu tous les articles prédictifs d'une reconversion post-burnout en élevage caprin dans le Cantal."
}


def unlock_achievement(cursor, connection, achievement_id):

    cursor.execute("""
        INSERT OR IGNORE INTO player_achievements (achievement_id)
        VALUES (?)
    """, (achievement_id,))

    unlocked = cursor.rowcount == 1

    if unlocked:
        connection.commit()

        cursor.execute("""
            SELECT name
            FROM achievements
            WHERE id = ?
        """, (achievement_id,))

        achievement = cursor.fetchone()

        if achievement:
            print(f"🏆 Objectif validé : {achievement[0]} !")

    return unlocked


def check_parent_achievement(cursor, connection, parent_id):

# Comment ça fonctionne ?
# Prenons Le Maître des Mélanges, dont l'ID est 1.
# La première requête compte ses enfants dans achievements : 5 sous-objectifs.
# La deuxième compte combien de ces enfants figurent dans player_achievements.
# Si les deux nombres correspondent, le parent est débloqué.

    cursor.execute("""
        SELECT COUNT(*)
        FROM achievements
        WHERE parent_id = ?
    """, (parent_id,))

    total_children = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM achievements AS a
        JOIN player_achievements AS pa
            ON pa.achievement_id = a.id
        WHERE a.parent_id = ?
    """, (parent_id,))

    unlocked_children = cursor.fetchone()[0]

    if total_children > 0 and unlocked_children == total_children:
        unlock_achievement(cursor, connection, parent_id)

# --------------------------------------------------------- Maître des Mélanges (discoveries) -------------------------------------

def check_discovery_achievements(cursor, connection):

    results = get_objective_discovered_recipes(cursor)

    for number_of_ingredients, total_recipes, discovered_recipes in results:

        if total_recipes > 0 and discovered_recipes == total_recipes:
            unlock_achievement(cursor, connection, number_of_ingredients)

    check_parent_achievement(cursor, connection, 1)

# --------------------------------------------------------- La Popotte (préparation des recettes) -------------------------------------

def check_crafted_recipes_achievements(cursor, connection):

    for type_id in (1, 2, 3):

        total = get_total_recipes(cursor, type_id)

        cursor.execute("""
            SELECT COUNT(*)
            FROM player_recipes AS pr
            JOIN recipes AS r
                ON r.id = pr.recipe_id
            WHERE r.type_id = ?
                AND pr.crafted = 1
        """, (type_id,))

        crafted = cursor.fetchone()[0]

        if total > 0 and crafted == total:
            unlock_achievement(cursor, connection, type_id + 8)

    check_parent_achievement(cursor, connection, 8)

# --------------------------------------------------------- Ingrédients -------------------------------------

def get_objective_collected_ingredients(cursor):

    cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM ingredients),
            (SELECT COUNT(*) FROM inventory)
    """)

    return cursor.fetchone()


def check_ingredients_achievement(cursor, connection):

    total, collected = get_objective_collected_ingredients(cursor)

    if total > 0 and collected == total:
        unlock_achievement(cursor, connection, 7)


#------------------------------------------------------------ Hauts-faits ---------------------------------------

commercial_achievements = {
    12: {25, 39, 12, 18, 27, 41},
    13: {37, 40, 21, 22},
    14: {36, 24, 11, 16, 30},
    15: {20, 34, 35, 14, 6},
    16: {42, 45, 33, 38, 26}
}

def get_objective_specific_sales(cursor):

    cursor.execute("""
        SELECT DISTINCT recipe_id
        FROM sales_history
        WHERE quantity > 0
    """)

    sold_recipes = {row[0] for row in cursor.fetchall()}

    return sold_recipes


def check_commercial_achievements(cursor, connection):

    sold_recipes = get_objective_specific_sales(cursor)

    for achievement_id, required_recipes in commercial_achievements.items():

        if required_recipes.issubset(sold_recipes):
            unlock_achievement(cursor, connection, achievement_id)




