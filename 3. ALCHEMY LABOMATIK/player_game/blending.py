from display.display_equipment_and_equipment_craft import display_all_available_mixing_tools
from display.display_inventories import display_inventory
from display.display_refactor import group_data_under_same_id
from display.display_utils import COLORS, RESET

from player_game.initialization import initialize_player_equipment
from player_game.recipe_research import get_unknown_recipes

from data_management.discoveries import get_discovery_affinity_signature

def pick_mixing_tool(cursor):

    mixing_tools = display_all_available_mixing_tools(cursor)

    if not mixing_tools:
        print("Vous ne possédez aucun instrument de mélange. Essayez d'en fabriquer un !")
        return
    
    while True:
            
        choix = input("Instrument de mélange choisi (Entrée pour revenir) : ")

        if not choix:
            return
    
        # récupération de l'equipment_id
        if choix.isdigit() and 1 <= int(choix) <= len(mixing_tools):
            mixing_tool_id = mixing_tools[int(choix) - 1][0]
            break
    
        print("choix invalide")

    return mixing_tool_id


def return_mixing_tool_capacity(cursor, mixing_tool_id):

    # récupération capacity
        cursor.execute("""
            SELECT capacity
            FROM mixing_tools
            WHERE equipment_id = ?
            """, (mixing_tool_id,))
                
        result = cursor.fetchone()

        if result is None:
            return
        
        capacity = result[0]

        if capacity is None:
            return
        
        return capacity


def pick_ingredients_to_blend(cursor, capacity):
 
    ingredients = display_inventory(cursor)

    if not ingredients:
        print("Votre inventaire est vide.")
        return

    ingredient_groups = group_data_under_same_id(ingredients)
    print()

    blending_ingredients = []

    for _ in range(capacity):

        while True:

            choice = input("Ingrédient choisi (q pour quitter): ")

            if choice == "q":
                return

            if choice.isdigit() and 1 <= int(choice) <= len(ingredient_groups):

                group = ingredient_groups[int(choice) - 1]

                ingredient_id = group[0][0]

                cursor.execute("""
                    SELECT
                        ingredients.name,
                        rarities.color
                    FROM ingredients
                    JOIN rarities
                        ON rarities.id = ingredients.rarity_id
                    WHERE ingredients.id = ?
                    """, (ingredient_id,))

                result = cursor.fetchone()

                name = result[0]
                color = result[1]

                blending_ingredients.append(ingredient_id)

                print(f"{COLORS[color]}{name}{RESET}")
                print()

                break

            print("choix invalide")

        print(f"ID ingrédients du mélange : {blending_ingredients}")
        print()
    
    return blending_ingredients
    
# ---------------------------------------------------- Affinités du mélange ----------------------------------------------------------

def blend_affinities_result(cursor, capacity, blending_ingredients):

    blending_affinities = {}

    for ingredient_id in blending_ingredients:

        cursor.execute("""
            SELECT 
                ingredient_affinities.affinity_id, 
                ingredient_affinities.value,
                affinities.icon
            FROM ingredient_affinities
            JOIN affinities
                ON affinities.id = ingredient_affinities.affinity_id
            WHERE ingredient_id = ?
            """, (ingredient_id,))

        result = cursor.fetchall()

        for affinity_id, value, icon in result:
            if affinity_id in blending_affinities:
                total_value = value + blending_affinities[affinity_id][0]
                blending_affinities[affinity_id] = (total_value, icon)

            else:
                blending_affinities[affinity_id] = (value, icon)

    for affinity_id, (value, icon) in blending_affinities.items():
        blending_affinities[affinity_id] = (round(value / capacity, 2), icon)

    return blending_affinities

# -------------------------------------------- Mélanger ------------------------------------------------------------------------------

def blending(cursor):

    mixing_tool_id = pick_mixing_tool(cursor)

    if mixing_tool_id is None:
        return

    capacity = return_mixing_tool_capacity(cursor, mixing_tool_id)

    if capacity is None:
        return

    blending_ingredients = pick_ingredients_to_blend(cursor, capacity)

    if blending_ingredients is None:
        return

    blending_affinities = blend_affinities_result(
        cursor,
        capacity,
        blending_ingredients
    )

    if blending_affinities is None:
        return

    return blending_affinities, capacity

# ------------------------------------------------ Récupère la signature du mélange ----------------------------------------------------------------

def get_blend_affinity_signature(blending_affinities):

    signature = []

    for affinity_id, (value, icon) in blending_affinities.items():
        signature.append((icon, value))

    # on récupère le format de blending_affinities (affinity_id, (value, icon)) 
    # et on le transforme pour qu'il corresponde à la signature de la découverte (discovery_id, (icon, value))

    signature.sort(key=lambda x: x[1], reverse=True)
    print("Signature du mélange :")

    for icon, value in signature:
        print(f"{icon} : {value}")

    return signature


# ---------------------------------------------- Son rôle : chercher quelle recette correspond au mélange effectué --------------------------
# Effectue un mélange, récupère sa signature et recherche
# une recette dont le nombre d'ingrédients et les affinités
# correspondent aux conditions de découverte.
# Renvoie (recipe_id, recipe_name, difficulty_id) si trouvée,
# sinon None.

def join_corresponding_recipe_to_blend(cursor, connection, recipe_id=None):

    result = blending(cursor)

    if result is None:
        return

    blending_affinities, capacity = result

    blend_affinity_signature = get_blend_affinity_signature(blending_affinities)
    
    discoveries_affinities_signatures = get_discovery_affinity_signature(cursor)

    unknown_recipes = get_unknown_recipes(cursor)

    for unknown_recipe, recipe_data in unknown_recipes:
        number_of_ingredients = recipe_data[3]
        difficulty_number_of_affinities = recipe_data[5]
        signature = recipe_data[6]

        if capacity != number_of_ingredients:
            continue

        save_clues_to_player_recipe_research(unknown_recipe, difficulty_number_of_affinities, signature, blend_affinity_signature, cursor, connection)


    if recipe_id is None:
                
        for recipe_id, (recipe_name, recipe_type, recipe_color, discovery_number_of_ingredients, difficulty_id,
        difficulty_number_of_affinities, signature) in discoveries_affinities_signatures.items():

            if capacity != discovery_number_of_ingredients:
                #print("Pas de correspondance du nombre d'ingrédients.")
                continue

            result = compare_recipe_to_blend(recipe_id, recipe_name, difficulty_id, difficulty_number_of_affinities, signature,
            blend_affinity_signature)

            if result:
                return result

    else:
        recipe_data = discoveries_affinities_signatures[recipe_id]
        
        (recipe_name, recipe_type, recipe_color, discovery_number_of_ingredients, difficulty_id, 
        difficulty_number_of_affinities, signature) = recipe_data 

        if capacity != discovery_number_of_ingredients:
            #print("Pas de correspondance du nombre d'ingrédients.")
            return # on est pas dans une boucle comme plus haut

        result = compare_recipe_to_blend(recipe_id, recipe_name, difficulty_id, difficulty_number_of_affinities, signature,
        blend_affinity_signature)

        if result:
            return result
        
# ------------------------------------ Son rôle : déterminer si les affinités d'un mélange satisfont 
#                                        les conditions de découverte d'une recette précise -------------------------------------------

# Compare la signature du mélange à celle d'une recette.
# Vérifie les affinités exigées par la difficulté :
# nombre, icônes et ordre strictement décroissant des valeurs.
# Renvoie les informations de la recette si elle correspond,
# sinon None.

def compare_recipe_to_blend(recipe_id, recipe_name, difficulty_id, difficulty_number_of_affinities, signature, blend_affinity_signature):

    corresponding_affinities = 0

    required_signature = signature[:difficulty_number_of_affinities]
    blend_signature = blend_affinity_signature[:difficulty_number_of_affinities]
    
    if len(required_signature) != len(blend_signature): # nombre d'affinités prises en compte
        #print("Pas de correspondance du nombre d'affinités prises en compte.")
        return
    
    for i in range(len(required_signature)):# required_signature[i] = id affinité i-ème position
    
        discovery_affinity_icon = required_signature[i][0] # required_signature[i][0] = icône affinité (en premier dans la parenthèse (icon, value))
        blend_affinity_icon = blend_signature[i][0]
    
        if discovery_affinity_icon != blend_affinity_icon: # on vérifie les icônes
            #print("Pas de correspondance d'affinités.")
            break
    
        if i < len(blend_signature) - 1: # si ce n'est pas la dernière, valeur actuelle strictement supérieure à la suivante ?
            current_value = blend_signature[i][1]
            next_value = blend_signature[i + 1][1]
    
            if current_value <= next_value:
                #print("Ordre des valeurs incorrect.")
                break
    
        corresponding_affinities += 1
    
    if corresponding_affinities == len(required_signature):
        print("Correspondance trouvée ✅")
        return recipe_id, recipe_name, difficulty_id       
    
# ------------------------------------------------ Découverte recette ----------------------------------------------------------------

def discover_recipe(cursor, connection, recipe_id=None):

    result = join_corresponding_recipe_to_blend(cursor, connection, recipe_id)

    if result is None:
        return

    recipe_id, recipe_name, difficulty_id = result

    cursor.execute("""
        SELECT recipe_id
        FROM player_recipes
    """)

    player_recipes_ids_packed = cursor.fetchall()
    player_recipes_ids_unpacked = [recipe[0] for recipe in  player_recipes_ids_packed]

    if recipe_id not in player_recipes_ids_unpacked:
        
        cursor.execute("""
            SELECT 
                recipes.name,
                rarities.color
            FROM recipes
            JOIN rarities
                ON rarities.id = recipes.rarity_id
            WHERE recipes.id = ?
        """, (recipe_id,))

        recipe_name_color = cursor.fetchone()
        recipe_name = recipe_name_color[0]
        recipe_color = recipe_name_color[1]

        print(f"Vous découvrez {COLORS[recipe_color]}{recipe_name}{RESET} !")
        print()

        cursor.execute("""
            INSERT INTO player_recipes (recipe_id)
            VALUES (?)
        """, (recipe_id,))

        connection.commit()

        initialize_player_equipment(cursor, connection)

# ----------------------------------------------------- CLUES ----------------------------------------------------------------------

def compare_clues_to_blend(recipe_id, difficulty_number_of_affinities, signature, blend_affinity_signature):

    required_signature = signature[:difficulty_number_of_affinities]
    blend_signature = blend_affinity_signature[:difficulty_number_of_affinities]

    discovered_clues = []

    for i in range(min(len(required_signature), len(blend_signature))):
        discovery_affinity_icon = required_signature[i][0]
        blend_affinity_icon = blend_signature[i][0]

        if discovery_affinity_icon == blend_affinity_icon: # on vérifie les icônes
            clue_rank = i + 1
            discovered_clues.append((recipe_id, clue_rank))

    return discovered_clues


def save_clues_to_player_recipe_research(recipe_id, difficulty_number_of_affinities, signature, blend_affinity_signature, cursor, connection):

    discovered_clues = compare_clues_to_blend (recipe_id, difficulty_number_of_affinities, signature, blend_affinity_signature)

    for recipe_id, clue_rank in discovered_clues:
        cursor.execute("""
        INSERT OR IGNORE INTO player_recipe_research
        (recipe_id, clue_rank)
        VALUES (?, ?)
        """, (recipe_id, clue_rank))

        if cursor.rowcount == 1:
            print("Nouvel indice découvert !")

    connection.commit()