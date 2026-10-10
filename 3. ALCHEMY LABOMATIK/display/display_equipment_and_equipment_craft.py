from display.display_utils import COLORS, RESET, DIM, YELLOW
from display.display_refactor import group_data_under_same_id, format_recipe_and_craft_items

#----------------------------------------------- MIXING TOOLS ----------------------------------------------------

def display_all_mixing_tools(cursor):

    cursor.execute("""
        SELECT
            equipment.id,
            equipment.name,
            rarities.color,
            mixing_tools.capacity
        FROM mixing_tools
        JOIN equipment
            ON equipment.id = mixing_tools.equipment_id
        JOIN rarities
            ON rarities.id = equipment.rarity_id
    """)

    result = cursor.fetchall()

    display_mixing_tool(result)

    return result

def display_mixing_tool(mixing_tools):

    groups = group_data_under_same_id(mixing_tools)

    display_number = 0

    for group in groups:

        display_number += 1

        mixing_tool = group[0]  # On prend le premier élément du groupe pour obtenir les informations de l'outil de mélange

        mixing_tool_name = mixing_tool[1]
        mixing_tool_color = mixing_tool[2]
        mixing_tool_capacity = mixing_tool[3]

        print(f"{display_number} - {COLORS[mixing_tool_color]}{mixing_tool_name}{RESET} - Nombre d'ingrédients : {mixing_tool_capacity}")
    
# ----------------------------------------------- EQUIPMENT ----------------------------------------------------

def display_all_equipment(cursor):

    cursor.execute("""
        SELECT
            equipment.id,
            equipment.name,
            equipment_categories.name,
            equipment.description,
            rarities.color,
            equipment.unlock_discoveries
        FROM equipment
        LEFT JOIN equipment_categories
            ON equipment.category_id = equipment_categories.id
        LEFT JOIN rarities
            ON rarities.id = equipment.rarity_id
        ORDER BY equipment_categories.id, equipment.rarity_id ASC
        
    """)
    
    equipment = cursor.fetchall()

    print()
    print("--- Matériel ---")
    for equipment_id, equipment_name, equipment_category, equipment_description, equipment_color, equipment_unlock_discoveries in equipment:
        color = COLORS[equipment_color]
        print(f'{equipment_id:<2} - {color}{equipment_name}{RESET} - {YELLOW}{equipment_category}{RESET} - Déblocage : {equipment_unlock_discoveries} découvertes')
        print(f'     {DIM}{equipment_description}{RESET}')
        print()

# ----------------------------------------------- EQUIPMENT CRAFT ----------------------------------------------------

def display_all_equipment_crafts(cursor):

    cursor.execute("""
    SELECT
        equipment.id,
        equipment.name,
        equipment.description,
        equipment_rarity.color,
        equipment_categories.name,
        ingredients.name,
        equipment_craft.quantity,
        ingredient_rarity.color
    FROM equipment_craft

    JOIN equipment
        ON equipment.id = equipment_craft.equipment_id

    JOIN rarities AS equipment_rarity
        ON equipment_rarity.id = equipment.rarity_id

    JOIN equipment_categories
        ON equipment_categories.id = equipment.category_id

    JOIN ingredients
        ON ingredients.id = equipment_craft.ingredient_id

    JOIN rarities AS ingredient_rarity
        ON ingredient_rarity.id = ingredients.rarity_id

    ORDER BY
        equipment.category_id ASC,
        equipment.rarity_id ASC,
        equipment.id ASC
    """)

    result = cursor.fetchall()
    print()
    print("--- Fabrication ---")
    display_equipment_craft(result)
    return result


def display_equipment_craft(equipment_craft):

    display_number = 0

    groups = group_data_under_same_id(equipment_craft)

    for group in groups:

        display_number += 1
        
        craft_list = []

        for equipment in group:

            equipment_id = equipment[0]
            equipment_name = equipment[1]
            equipment_description = equipment[2]
            equipment_color = equipment[3]
            equipment_category_name = equipment[4]
            ingredient_name = equipment[5]
            ingredient_quantity = equipment[6]    
            ingredient_color = equipment[7]

            if ingredient_name is not None:
                craft_list.append((ingredient_name, ingredient_quantity, ingredient_color))

        craft_text = format_recipe_and_craft_items(craft_list)
                        
        print(f"{display_number:<2} - {COLORS[equipment_color]}{equipment_name}{RESET} - {YELLOW}{equipment_category_name}{RESET} - {DIM}{equipment_description}{RESET}")
        print(f"     {craft_text}")
        print()