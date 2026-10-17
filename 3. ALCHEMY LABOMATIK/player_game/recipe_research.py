from data_management.discoveries import get_discovery_affinity_signature
from display.display_utils import COLORS, YELLOW, RESET, format_difficulty_stars, info_format_difficulty_stars


def get_recipe_research_clues(cursor, recipe_id):

    cursor.execute("""
        SELECT
            clue_rank
        FROM player_recipe_research
        WHERE recipe_id = ?
        ORDER BY clue_rank ASC
    """, (recipe_id,))

    clue_ranks = cursor.fetchall()

    clue_rank_unpacked = [clue_rank[0] for clue_rank in clue_ranks]
    
    return clue_rank_unpacked



def show_recipe_research_clues(cursor, recipe_id):

    clue_rank = get_recipe_research_clues(cursor, recipe_id)

    discoveries_affinities = get_discovery_affinity_signature(cursor)

    recipe_data = discoveries_affinities[recipe_id]

    (recipe_name, recipe_type, recipe_color, number_of_ingredients, difficulty_id, number_of_affinities, signature) = recipe_data

    if 0 in clue_rank:
        print(f'{COLORS[recipe_color]}{recipe_name}{RESET} - {YELLOW}{recipe_type}{RESET}')
        print(f"Nombre d'ingrédients : {number_of_ingredients} - Difficulté : {format_difficulty_stars(difficulty_id)}")
    else:
        print(f"???")

    for clue in range (1, number_of_affinities + 1):

        if clue in clue_rank and clue <= len(signature):
            print(f"Affinité {clue} : {signature[clue - 1][0]}")

        elif clue_rank and clue > len(signature) and clue_rank[-1] == len(signature):
        # Je suis après la fin de la vraie signature ET le dernier rang découvert correspond au dernier rang réel.
            print(f"Affinité {clue} : aucune")

        else:
            print(f"Affinité {clue} : ???")



def get_max_capacity(cursor):

    cursor.execute("""
        SELECT MAX(mixing_tools.capacity) FROM player_equipment
    
        JOIN equipment
            ON equipment.id = player_equipment.equipment_id
        
        JOIN mixing_tools
            ON mixing_tools.equipment_id = equipment.id
    
        WHERE player_equipment.crafted = 1 AND equipment.category_id = 1""")
    
    result = cursor.fetchone()
    
    max_capacity = result[0]

    return max_capacity


def get_unknown_recipes(cursor):

    cursor.execute("""SELECT recipe_id FROM player_recipes""")
    player_recipes_ids = cursor.fetchall()
    player_recipes_ids = [recipe_id[0] for recipe_id in player_recipes_ids]

    discoveries_affinities = get_discovery_affinity_signature(cursor)

    unknown_recipes = []

    for recipe_id in discoveries_affinities:

        recipe_data = discoveries_affinities[recipe_id]
        #(recipe_name, recipe_type, recipe_color, number_of_ingredients, difficulty_id, number_of_affinities, signature) = recipe_data
        
        if recipe_id not in player_recipes_ids:
            unknown_recipes.append((recipe_id, recipe_data))

    unknown_recipes.sort(key=lambda recipe_data: recipe_data[1][3])

    return unknown_recipes



def menu_unknown_recipes(cursor):

    unknown_recipes = get_unknown_recipes(cursor)
    possible_number_of_ingredients, number_groups = group_by_number_of_ingredients(unknown_recipes)
    possible_number_of_ingredients = list(number_groups.keys())
    max_capacity = get_max_capacity(cursor)
    
    while True:

        print()
        print("📑 RECHERCHE DE RECETTE")

        info_format_difficulty_stars()

        for number, number_of_ingredients in enumerate(possible_number_of_ingredients, start=1):

            if number_of_ingredients > max_capacity:
                print(f"{YELLOW}[{number}] 🔒 Recettes à {number_of_ingredients} ingrédients{RESET}")

            else:
                print(f"{YELLOW}[{number}] Recettes à {number_of_ingredients} ingrédients{RESET}")
                print()
                show_unknown_recipes(cursor, number_of_ingredients)

        print("[r] Retour")

        choice = input("> ")
        print()
        
        if choice == "r":
            return

        elif choice.isdigit() and 1 <= int(choice) <= len(possible_number_of_ingredients):
            selected_group = possible_number_of_ingredients[int(choice)-1]
            
            if selected_group > max_capacity:
                print (f"Catégorie verrouillée 🔒")
                continue

        else:
            print("Choix invalide.")


def show_unknown_recipes(cursor, selected_group):

    unknown_recipes = get_unknown_recipes(cursor)
    possible_number_of_ingredients, number_groups = group_by_number_of_ingredients(unknown_recipes)
    recipes_to_show = number_groups[selected_group]

    for number, recipe_to_show in enumerate(recipes_to_show, start=1):

        recipe_to_show_id = recipe_to_show[0]
        
        print(f"[{number}]")
        show_recipe_research_clues(cursor, recipe_to_show_id)
        print()

    return recipes_to_show


def group_by_number_of_ingredients(items):
           
    possible_number_of_ingredients = [2, 3, 4, 5, 6]

    number_groups = {}

    for number in possible_number_of_ingredients:
        number_groups[number] = []

    for item in items:
        item_id = item[0]
        recipe_data = item[1]
        number_of_ingredients = recipe_data[3]

        number_groups[number_of_ingredients].append(item)

    return possible_number_of_ingredients, number_groups


        
        



    


        
        




