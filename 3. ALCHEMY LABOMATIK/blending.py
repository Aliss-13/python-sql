from display_equipment_and_equipment_craft import display_all_mixing_tools
from display_inventories import display_inventory
from display_refactor import group_data_under_same_id
from display_colors_and_rarities import COLORS, RESET

def pick_mixing_tool(cursor):

    mixing_tools = display_all_mixing_tools(cursor)
    print()
    
    while True:
            
        choix = input("Instrument de mélange choisi (q pour revenir) : ")

        if choix.lower() == "q":
            return None
    
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
        capacity = result[0]
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
            return

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

    print("Affinités finales du mélange :")

    for affinity_id, (value, icon) in blending_affinities.items():
        print(f"{icon} : {value}")

    return blending_affinities



def blending(cursor):

    mixing_tool_id = pick_mixing_tool(cursor)

    if mixing_tool_id is None:
        return None, None

    capacity = return_mixing_tool_capacity(cursor, mixing_tool_id)

    blending_ingredients = pick_ingredients_to_blend(cursor, capacity)

    blending_affinities = blend_affinities_result(cursor, capacity, blending_ingredients)

    return blending_affinities, capacity


def join_corresponding_recipe_to_blend(cursor):

    blending_affinities, capacity = blending(cursor)

    cursor.execute("""
        SELECT 
            recipe_discovery.recipe_id, 
            recipe_discovery.number_of_ingredients,
            recipe_discovery.affinity_id,
            recipe_discovery.value
        FROM recipe_discovery
        WHERE number_of_ingredients = ?
        ORDER BY recipe_discovery.recipe_id
        """, (capacity,))
    
    result = cursor.fetchall()

    discoveries = group_data_under_same_id(result)

    for discovery in discoveries:

        discovery_id = discovery[0][0]

        disc_affinities_ids = []
        corresponding_affinities = 0

        for recipe_id, number_of_ingredients, affinity_id, disc_value in discovery:

            disc_affinities_ids.append(affinity_id)

            if affinity_id not in blending_affinities:
                continue

            blending_value, icon = blending_affinities[affinity_id]

            if blending_value == disc_value:
                corresponding_affinities += 1

        # Le mélange ne doit pas avoir d'affinité supplémentaire
        extra_affinity = False

        for blending_affinity in blending_affinities:
            if blending_affinity not in disc_affinities_ids:
                extra_affinity = True

        if not extra_affinity and corresponding_affinities == len(discovery):
            print("Correspondance trouvée !")
            return discovery_id

    return None