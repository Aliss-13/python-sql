from display.display_utils import YELLOW, LIGHT_PINK, RESET, COLORS, DIM, display_recipe_description
from display.display_refactor import group_data_under_same_id, format_affinity_items

from data_management.discoveries import get_number_of_discoveries

def menu_objectives(cursor):

    while True:
    
        print()
        print("📈 OBJECTIFS")
        display_objective_achievements(cursor)
        print()
        print("[1] 🧪 Laboratoire")
        print("[2] 🧫 La Popotte")
        print("[3] 🌀 Portails")
        print("[4] 🏅 Hauts-faits")
            
        print("[r] Retour")
    
        choix = input("> ")
        print()
    
        if choix == "1":
            display_objective_discovered_recipes(cursor)
            
        elif choix == "2":
            display_objective_crafted_recipes(cursor, crafted=1)
            print()
            display_objective_crafted_recipes(cursor, crafted=0)
            
        elif choix == "3":
            display_objective_unlocked_ingredients(cursor)
            print()
            display_objective_never_obtained_ingredients(cursor)

        elif choix == "4":
            display_objective_commercial_achievements(cursor)
    
        elif choix == "r":
            return
    
        else:
            print("Choix invalide")

#--------------------------------------------- BILAN --------------------------------------------------------------

def get_objective_achievements(cursor):

    cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.category,
            a.parent_id,
            CASE
                WHEN pa.achievement_id IS NOT NULL THEN 1
                ELSE 0
            END AS unlocked
        FROM achievements AS a

        LEFT JOIN player_achievements AS pa
            ON pa.achievement_id = a.id

        ORDER BY a.id
    """)

    return cursor.fetchall()


def display_objective_achievements(cursor):

    achievements = get_objective_achievements(cursor)

    for category, title in (
        ("victory", "🏆 OBJECTIFS DE VICTOIRE"),
        ("fun", "🎭 HAUTS FAITS COMMERCIAUX")
    ):

        print(f"\n{title}")

        for achievement_id, name, achievement_category, parent_id, unlocked in achievements:

            if achievement_category != category:
                continue

            if unlocked:
                status = "🏆" if parent_id is None else "✅"
            else:
                status = "🔒"

            indent = "   " if parent_id is not None else "\n"

            print(f"{indent}{status} {name}")

        print()

#------------------------------------------------ UTILE -----------------------------------------------------------------------

def get_total_recipes(cursor, type_id=None):

    if type_id is None:
        cursor.execute("""
            SELECT COUNT(DISTINCT recipe_id)
            FROM recipe_discovery
        """)
    else:
        cursor.execute("""
            SELECT COUNT(*)
            FROM recipes
            WHERE type_id = ?
        """, (type_id,))

    return cursor.fetchone()[0]

#--------------------------------------------- DECOUVERTES --------------------------------------------------------------

def get_objective_discovered_recipes(cursor):

# Pourquoi DISTINCT ?
# Parce que recipe_discovery contient aussi affinity_id et value. Une même recette peut donc apparaître plusieurs fois, une fois par affinité.
# Sans DISTINCT, tu risquerais de compter plusieurs fois la même recette.

    cursor.execute("""
    SELECT
        rd.number_of_ingredients,
        COUNT(DISTINCT rd.recipe_id) AS total_recipes,
        COUNT(DISTINCT pr.recipe_id) AS discovered_recipes

    FROM recipe_discovery AS rd

    LEFT JOIN player_recipes AS pr
        ON pr.recipe_id = rd.recipe_id

    GROUP BY rd.number_of_ingredients
    ORDER BY rd.number_of_ingredients
    """)

    result = cursor.fetchall()
    return result


def display_objective_discovered_recipes(cursor):

    result = get_objective_discovered_recipes(cursor)

    total = 0
    discovered = 0

    print("------------ Recettes découvertes ------------ ")
    print()

    for number_of_ingredients, total_recipes, discovered_recipes in result:
        percentage = round(discovered_recipes * 100 / total_recipes) if total_recipes else 0
        print(f"Mélanges à {number_of_ingredients} ingrédients : {discovered_recipes} / {total_recipes} - {percentage} %")
        total = total + total_recipes
        discovered = discovered + discovered_recipes

    print()
    print(f"{YELLOW}Total recettes découvertes : {discovered} / {total} - {round(discovered_recipes * 100 / total_recipes) if total_recipes else 0} %{RESET}")

#--------------------------------------------- CUISINE --------------------------------------------------------------

def get_objective_crafted_recipes(cursor, crafted):

    cursor.execute("""
    SELECT
            player_recipes.recipe_id,
            recipes.name,
            recipe_types.name,
            recipes.description,
            rarities.color
        FROM player_recipes

        JOIN recipes
            ON player_recipes.recipe_id = recipes.id

        JOIN recipe_types
            ON recipes.type_id = recipe_types.id

        JOIN rarities
            ON recipes.rarity_id = rarities.id

        WHERE player_recipes.crafted = ?

        ORDER BY recipe_types.id ASC, rarities.id ASC
    """, (crafted,))

    result = cursor.fetchall()
    return result


def display_objective_crafted_recipes(cursor, crafted):

    if crafted == 1:
        title = "Recettes fabriquées"
    else:
        title = "Recettes à fabriquer"

    result = get_objective_crafted_recipes(cursor, crafted)

    number_of_recipes = len(result)
    total = get_total_recipes(cursor, type_id=None)


    print(f"------------ {title} ({number_of_recipes} / {total}) ------------")
    print()

    for display_number, (recipe_id, recipe_name, recipe_type, recipe_description, recipe_rarity) in enumerate (result, start = 1):

        print(f"{display_number:<2} - {COLORS[recipe_rarity]}{recipe_name}{RESET} - {YELLOW}{recipe_type}{RESET}")
        display_recipe_description(recipe_description)
        print()


#--------------------------------------------- INGREDIENTS --------------------------------------------------------------

def get_objective_unlocked_ingredients(cursor):

# COUNT(*) compte tous les ingrédients.
# CASE WHEN unlock_discoveries = 1 THEN 1 END ne compte que ceux qui sont débloqués.
# Le nombre d'ingrédients verrouillés se calcule ensuite par soustraction.

    discovery_count = get_number_of_discoveries(cursor)

    cursor.execute("""
    SELECT
    COUNT(*) AS total_ingredients,
    COUNT(CASE WHEN unlock_discoveries <= ? THEN 1 END) AS unlocked_ingredients
    FROM ingredients
    """, (discovery_count,))

    result = cursor.fetchall()
    return result

def display_objective_unlocked_ingredients(cursor):

    result = get_objective_unlocked_ingredients(cursor)

    for total, unlocked in result:
        locked = total - unlocked
        percentage = round(unlocked * 100 / total) if total else 0
        print(f"Ingrédients débloqués : {unlocked} / {total} - {percentage} %")


def get_objective_never_obtained_ingredients(cursor):

# COUNT(*) compte tous les ingrédients.
# CASE WHEN unlock_discoveries = 1 THEN 1 END ne compte que ceux qui sont débloqués.
# Le nombre d'ingrédients verrouillés se calcule ensuite par soustraction.

    discovery_count = get_number_of_discoveries(cursor)

    cursor.execute("""
    SELECT
        ingredients.id,
        ingredients.name,
        ingredients.description,
        rarities.color,
        affinities.icon,
        ingredient_affinities.value
    FROM ingredients

    JOIN rarities
        ON ingredients.rarity_id = rarities.id
    
    JOIN ingredient_affinities
        ON ingredients.id = ingredient_affinities.ingredient_id

    JOIN affinities
        ON ingredient_affinities.affinity_id = affinities.id

    LEFT JOIN inventory
        ON ingredients.id = inventory.ingredient_id

    WHERE inventory.ingredient_id IS NULL
        AND ingredients.unlock_discoveries <= ?
    
    ORDER BY ingredients.id, affinities.id
    """, (discovery_count,))

    result = cursor.fetchall()
    return result


def display_objective_never_obtained_ingredients(cursor):

    result = get_objective_never_obtained_ingredients(cursor)

    groups = group_data_under_same_id(result)

    display_number = 0

    print("------------ Ingrédients débloqués non lootés ------------ ")
    print()

    for group in groups:

        affinity_list = []

        for ingredient in group:
            ingredient_id = ingredient[0]
            name = ingredient[1]
            description = ingredient[2]
            color = ingredient[3]
            icon = ingredient[4]
            value = ingredient[5]

            if icon is not None:
                affinity_list.append((icon, value))

        sorted_affinity_list = sorted(affinity_list, key=lambda x: x[1], reverse=True)
        
        affinity_text = format_affinity_items(sorted_affinity_list)

        display_number +=1
                    
        print(f"{display_number:<2} - {COLORS[color]}{name}{RESET}  {affinity_text}  ")
        print(f"     {DIM}{description}{RESET}") 
        print()

    # Pourquoi group[0] ?
    # Parce que toutes les lignes d'un groupe concernent le même ingrédient. On peut donc récupérer son nom, sa description et sa rareté à partir de la première ligne.
    # Le *_ permet simplement d'ignorer les trois dernières valeurs pour le moment.


#--------------------------------------------- COMMERCIAL --------------------------------------------------------------

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


def get_objective_required_recipes(cursor, achievement_id):

    required_recipes = commercial_achievements[achievement_id]

    placeholders = ",".join("?" for _ in required_recipes)

    cursor.execute(f"""
        SELECT
            recipes.id,
            recipes.name,
            CASE
                WHEN pr.recipe_id IS NOT NULL THEN 1
                ELSE 0
            END AS discovered

        FROM recipes

        LEFT JOIN player_recipes AS pr
            ON pr.recipe_id = recipes.id

        WHERE recipes.id IN ({placeholders})
        ORDER BY recipes.id
    """, tuple(required_recipes))

# Comment ça fonctionne ?

# On a fait cette jointure :
# LEFT JOIN player_recipes AS pr
# ON pr.recipe_id = r.id
#
# Elle permet de récupérer toutes les recettes demandées, même celles que le joueur n'a pas encore découvertes.
#
# Dans A-LAB, une recette présente dans player_recipes est une recette découverte.
# 
# Donc :
# - WHEN pr.recipe_id IS NOT NULL : la recette existe dans player_recipes, elle est découverte.
# - THEN 1 : on renvoie 1 pour indiquer « découverte ».
# - ELSE 0 : sinon, on renvoie 0 pour « non découverte ».
# - END AS discovered : on donne le nom discovered à cette colonne calculée.

    return cursor.fetchall()


def display_objective_required_recipes(cursor, achievement_id):

    recipes = get_objective_required_recipes(cursor, achievement_id)
    sold_recipes = get_objective_specific_sales(cursor)

    for recipe_id, recipe_name, discovered in recipes:

        if recipe_id in sold_recipes:
            print(f"   ✅ {recipe_name}")

        elif discovered:
            print(f"   🔒 {recipe_name}")

        else:
            print("   ❔ ???")


def get_objective_commercial_achievements(cursor):

    cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.description,
            CASE
                WHEN pa.achievement_id IS NOT NULL THEN 1
                ELSE 0
            END AS unlocked

        FROM achievements AS a

        LEFT JOIN player_achievements AS pa
            ON pa.achievement_id = a.id

        WHERE a.category = 'fun'
        ORDER BY a.id
    """)

    return cursor.fetchall()


def display_objective_commercial_achievements(cursor):

    achievements = get_objective_commercial_achievements(cursor)

    print("🎭 HAUTS FAITS COMMERCIAUX")
    print()

    sold_recipes = get_objective_specific_sales(cursor)

    for achievement_id, name, description, unlocked in achievements:

        status = "🏆" if unlocked else "🔒"
        
        required_recipes = commercial_achievements.get(achievement_id, set())

        sold_count = len(required_recipes & sold_recipes)
        total_count = len(required_recipes)

        print(f"{status} {LIGHT_PINK}{name} ({sold_count} / {total_count}){RESET}")

        if description:
            print(f"   {DIM}{description}{RESET}")

        print()

        if achievement_id in commercial_achievements:
            display_objective_required_recipes(cursor, achievement_id)
            
        print()


