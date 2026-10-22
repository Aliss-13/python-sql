from display.display_utils import YELLOW, RESET, COLORS, DIM, display_recipe_description
from display.display_refactor import group_data_under_same_id, format_affinity_items

def menu_objectives(cursor):

    while True:
    
        print()
        print("📈 OBJECTIFS")
        print("[1] 🧪 Laboratoire")
        print("[2] 🧫 La Popotte")
        print("[3] 🌀 Portails")
        print("[5] 🏅 Hauts-faits")
            
        print("[r] Retour")
    
        choix = input("> ")
        print()
    
        if choix == "1":
            objective_discovered_recipes(cursor)
            
        elif choix == "2":
            objective_crafting_recipes(cursor, crafted=1)
            print()
            objective_crafting_recipes(cursor, crafted=0)
            
        elif choix == "3":
            objective_unlocked_ingredients(cursor)
            print()
            objective_never_obtained_ingredients(cursor)

        elif choix == "4":
            print("🏅 En construction")
    
        elif choix == "r":
            return
    
        else:
            print("Choix invalide")

#-----------------------------------------------------------------------------------------------------------------------

def get_total_recipes(cursor):
    cursor.execute("""
        SELECT COUNT(DISTINCT recipe_id)
        FROM recipe_discovery
    """)
    return cursor.fetchone()[0]

#--------------------------------------------- DECOUVERTES --------------------------------------------------------------

def objective_discovered_recipes(cursor):

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

    total = 0
    discovered = 0

    print("------------ Recettes découvertes ------------ ")
    print()

    for number_of_ingredients, total_recipes, discovered_recipes in result:
        percentage = round(discovered_recipes * 100 / total_recipes)
        print(f"Mélanges à {number_of_ingredients} ingrédients : {discovered_recipes} / {total_recipes} - {percentage} %")
        total = total + total_recipes
        discovered = discovered + discovered_recipes

    print()
    print(f"{YELLOW}Total recettes découvertes : {discovered} / {total} - {round(discovered*100 / total)} %{RESET}")

#--------------------------------------------- CUISINE --------------------------------------------------------------

def objective_crafting_recipes(cursor, crafted):

    if crafted == 1:
        title = "Recettes fabriquées"
    else:
        title = "Recettes à fabriquer"

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
    number_of_recipes = len(result)
    total = get_total_recipes(cursor)


    print(f"------------ {title} ({number_of_recipes} / {total}) ------------")
    print()

    for display_number, (recipe_id, recipe_name, recipe_type, recipe_description, recipe_rarity) in enumerate (result, start = 1):

        print(f"{display_number:<2} - {COLORS[recipe_rarity]}{recipe_name}{RESET} - {YELLOW}{recipe_type}{RESET}")
        display_recipe_description(recipe_description)
        print()


#--------------------------------------------- INGREDIENTS --------------------------------------------------------------

def objective_unlocked_ingredients(cursor):

# COUNT(*) compte tous les ingrédients.
# CASE WHEN unlock_discoveries = 1 THEN 1 END ne compte que ceux qui sont débloqués.
# Le nombre d'ingrédients verrouillés se calcule ensuite par soustraction.

    cursor.execute("""
    SELECT COUNT(*)
    FROM player_recipes
    """)
    
    discovered = cursor.fetchone()[0]

    cursor.execute("""
    SELECT
    COUNT(*) AS total_ingredients,
    COUNT(CASE WHEN unlock_discoveries <= ? THEN 1 END) AS unlocked_ingredients
    FROM ingredients
    """, (discovered,))

    result = cursor.fetchall()

    for total, unlocked in result:
        locked = total - unlocked
        percentage = round(unlocked * 100 / total)
        print(f"Ingrédients débloqués : {unlocked} / {total} - {percentage} %")


def objective_never_obtained_ingredients(cursor):

# COUNT(*) compte tous les ingrédients.
# CASE WHEN unlock_discoveries = 1 THEN 1 END ne compte que ceux qui sont débloqués.
# Le nombre d'ingrédients verrouillés se calcule ensuite par soustraction.

    cursor.execute("""
    SELECT COUNT(*)
    FROM player_recipes
    """)
    
    discovered = cursor.fetchone()[0]

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
    """, (discovered,))

    result = cursor.fetchall()

    groups = group_data_under_same_id(result)

    display_number = 0

    print("------------ Ingrédients non lootés ------------ ")
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

