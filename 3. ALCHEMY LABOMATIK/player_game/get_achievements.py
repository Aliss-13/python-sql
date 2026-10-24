from player_game.objectives import get_objective_discovered_recipes, get_total_recipes, commercial_achievements, get_objective_specific_sales



#-----------------------------------------------------------------------------------------------------------------------------------

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

def check_commercial_achievements(cursor, connection):

    sold_recipes = get_objective_specific_sales(cursor)

    for achievement_id, required_recipes in commercial_achievements.items():

        if required_recipes.issubset(sold_recipes):
            unlock_achievement(cursor, connection, achievement_id)


