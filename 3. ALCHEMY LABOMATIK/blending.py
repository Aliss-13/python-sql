from display_equipment_and_equipment_craft import display_all_mixing_tools
from display_inventories import display_inventory
from display_refactor import group_data_under_same_id
from display_utils import COLORS, RESET

def pick_mixing_tool(cursor):

    mixing_tools = display_all_mixing_tools(cursor)
    print()

    if mixing_tools is None:
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
    ingredient_groups = group_data_under_same_id(ingredients)
    print()

    blending_ingredients = []

    for _ in range(capacity):

        while True:

            choix = input("Ingrédient choisi : ")

            if choix.isdigit() and 1 <= int(choix) <= len(ingredient_groups):

                group = ingredient_groups[int(choix) - 1]

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


def join_corresponding_recipe_to_blend(cursor):

    result = blending(cursor)

    if result is None:
        return

    blending_affinities, capacity = result

    blend_affinity_signature = get_blend_affinity_signature(blending_affinities)

    discoveries_affinities_signatures = get_discovery_affinity_signature(cursor)

    for recipe_id, (
        recipe_name, 
        difficulty_id, 
        difficulty_number_of_affinities, 
        signature
        ) in discoveries_affinities_signatures.items():

        corresponding_affinities = 0

        required_signature = signature[:difficulty_number_of_affinities]
        blend_signature = blend_affinity_signature[:difficulty_number_of_affinities]

        if len(required_signature) != len(blend_signature): # nombre d'affinités prises en compte
            print("Pas de correspondance du nombre d'affinités prises en compte.")
            continue

        for i in range(len(required_signature)):# required_signature[i] = id affinité i-ème position
           
            discovery_affinity_icon = required_signature[i][0] # required_signature[i][0] = icône affinité (en premier dans la parenthèse (icon, value))
            blend_affinity_icon = blend_signature[i][0]

            if discovery_affinity_icon != blend_affinity_icon: # on vérifie les icônes
                print("Pas de correspondance d'affinités.")
                break

            if i < len(blend_signature) - 1: # si ce n'est pas la dernière, valeur actuelle strictement supérieure à la suivante ?
                current_value = blend_signature[i][1]
                next_value = blend_signature[i + 1][1]

                if current_value <= next_value:
                    print("Ordre des valeurs incorrect.")
                    break

            corresponding_affinities += 1

        if corresponding_affinities == len(required_signature):
            print("Correspondance trouvée ✅")
            return recipe_id, recipe_name, difficulty_id


                

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




def discover_recipe(cursor, connection):

    result = join_corresponding_recipe_to_blend(cursor)

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



        
def get_discovery_affinity_signature(cursor):

    cursor.execute("""

        SELECT 
            recipes.id,
            recipes.name,
            recipes.discovery_difficulty_id,
            recipe_discovery_difficulty.number_of_affinities,
            affinities.icon,
            recipe_discovery.value
        FROM recipe_discovery

        JOIN recipes
            ON recipes.id = recipe_discovery.recipe_id

        JOIN recipe_discovery_difficulty
            ON recipe_discovery_difficulty.id = recipes.discovery_difficulty_id

        JOIN affinities
            ON affinities.id = recipe_discovery.affinity_id

        ORDER BY recipe_discovery.recipe_id
    """)

    result = cursor.fetchall()

    groups = group_data_under_same_id(result)

    discoveries_affinities = {}

    for group in groups:

        signature = []
        discovery_id = group[0][0] # id recette découverte > construction signature > tri > regroupement par id > signature
        discovery_name = group[0][1] # nom recette découverte
        difficulty_id = group[0][2] # difficulté recette découverte
        difficulty_number_of_affinities = group [0][3] # difficulté nb affinités recette découverte

        for _, _, _, _, icon, value in group:
            signature.append((icon, value))
        signature.sort(key=lambda x: x[1], reverse=True)
        
        discoveries_affinities[discovery_id] = (discovery_name, difficulty_id, difficulty_number_of_affinities, signature)

    return discoveries_affinities