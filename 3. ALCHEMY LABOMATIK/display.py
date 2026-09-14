YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
DIM = "\033[2m"
LIGHT_PINK = "\033[38;5;218m"
LIGHT_GREEN = "\033[38;5;120m"
PURPLE = "\033[95m"
RESET = "\033[0m"


COLORS = {
    "white": "\033[37m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "reset": "\033[0m",
}


#----------------------------------------------- INGREDIENTS ----------------------------------------------------

def display_all_ingredients(cursor):

    cursor.execute("""
    SELECT
        ingredients.id,
        ingredients.name,
        ingredients.description,
        ingredients.level,
        rarities.color,
        affinities.icon,
        ingredient_affinities.value
    FROM ingredients
    JOIN rarities
        ON rarities.id = ingredients.rarity_id
    LEFT JOIN ingredient_affinities
        ON ingredient_affinities.ingredient_id = ingredients.id
    LEFT JOIN affinities
        ON affinities.id = ingredient_affinities.affinity_id
    ORDER BY ingredients.id ASC
    """)
   

    result = cursor.fetchall()
    display_ingredient(result)
    return(result)


def display_ingredient(ingredients):

    affinity_list = []
    current_id = None
    current_ingredient = None

    for ingredient in ingredients:
        ingredient_id = ingredient[0]

        if current_id is None:
            current_id = ingredient_id
            current_ingredient = ingredient

        if current_id != ingredient_id:

            if current_ingredient is not None:
                
                ingredient_color = COLORS[current_ingredient[4]]

                affinity_text = ""
                for icon, value in affinity_list:

                    if affinity_text:
                        affinity_text += " - "

                    affinity_text += f"{icon} {value}"
                    

                print(f"{current_ingredient[0]} - {ingredient_color}{current_ingredient[1]}\033[0m ({affinity_text}) - Niv. {current_ingredient[3]}")
                print(f"{DIM}{current_ingredient[2]}{RESET}")

            current_ingredient = ingredient
            current_id = ingredient_id
            affinity_list = []

        icon = ingredient[5]
        value = ingredient[6]

        if icon is not None:
            affinity_list.append((icon, value))

    ingredient_color = COLORS[ingredient[4]]
        
    affinity_text = ""
    for icon, value in affinity_list:
        if affinity_text:
            affinity_text += " - "
        affinity_text += f"{icon} {value}"
        
    print(f"{current_ingredient[0]} - {ingredient_color}{current_ingredient[1]}\033[0m ({affinity_text}) - Niv. {current_ingredient[3]}")
    print(f"{DIM}{current_ingredient[2]}{RESET}")

#----------------------------------------------- AFFINITIES ----------------------------------------------------

def display_all_affinities(cursor):

    cursor.execute("""
    SELECT
        id,
        name,
        icon
    FROM affinities
    """)

    result = cursor.fetchall()
    display_affinity(result)
    return result


def display_affinity(affinities):
    for aff_id, name, icon in affinities:
        print(f'{aff_id} - {icon} {name}')


#----------------------------------------------- INVENTORY ----------------------------------------------------

def display_inventory(cursor):

    cursor.execute("""
        SELECT
            inventory.ingredient_id,
            ingredients.name,
            inventory.quantity,
            ingredients.level,
            rarities.color,
            affinities.icon,
            ingredient_affinities.value
        FROM inventory
        JOIN ingredients
            ON ingredients.id = inventory.ingredient_id
        JOIN rarities
            ON rarities.id = ingredients.rarity_id
        LEFT JOIN ingredient_affinities
            ON ingredient_affinities.ingredient_id = ingredients.id
        LEFT JOIN affinities
            ON affinities.id = ingredient_affinities.affinity_id
        ORDER BY inventory.ingredient_id ASC
    """)

    result = cursor.fetchall()
    print()
    print("📓 Inventaire")
    display_ingredient_from_inventory(result)
    return result


def display_ingredient_from_inventory(inventory):

    affinity_list = []
    current_id = None
    current_ingredient = None

    for ingredient in inventory:
        ingredient_id = ingredient[0]

        if current_id is None:
            current_id = ingredient_id
            current_ingredient = ingredient

        if current_id != ingredient_id:

            if current_ingredient is not None:
                
                ingredient_color = COLORS[current_ingredient[4]]

                affinity_text = ""
                for icon, value in affinity_list:

                    if affinity_text:
                        affinity_text += " - "

                    affinity_text += f"{icon} {value}"
                    
                print(f"{current_ingredient[0]} - {ingredient_color}{current_ingredient[1]}{RESET} {YELLOW}x{current_ingredient[2]}{RESET} ({affinity_text}) - Niv. {current_ingredient[3]}")

            current_ingredient = ingredient
            current_id = ingredient_id
            affinity_list = []

        icon = ingredient[5]
        value = ingredient[6]

        if icon is not None:
            affinity_list.append((icon, value))

    ingredient_color = COLORS[current_ingredient[4]]
        
    affinity_text = ""
    for icon, value in affinity_list:
        if affinity_text:
            affinity_text += " - "
        affinity_text += f"{icon} {value}"
        
    print(f"{current_ingredient[0]} - {ingredient_color}{current_ingredient[1]}{RESET} {YELLOW}x{current_ingredient[2]}{RESET} ({affinity_text}) - Niv. {current_ingredient[3]}")

#----------------------------------------------- PORTALS ----------------------------------------------------

def display_harvest_portal(cursor, quantity, ingredient_id):

    cursor.execute("""
        SELECT 
            ingredients.name,
            rarities.color
        FROM ingredients
        JOIN rarities
            ON rarities.id = ingredients.rarity_id
        WHERE ingredients.id = ?
    """, (ingredient_id,))
    
    ingredient = cursor.fetchone()
    
    ingredient_name = ingredient[0]
    ingredient_color = COLORS[ingredient[1]]
            
    print(f"{ingredient_color}{ingredient_name}{RESET} x{quantity}")

#----------------------------------------------- EQUIPMENT ----------------------------------------------------

def display_all_equipment(cursor):

    cursor.execute("""
        SELECT
            equipment.id,
            equipment.name,
            equipment_categories.name,
            equipment.description,
            rarities.color
        FROM equipment
        LEFT JOIN equipment_categories
            ON equipment.category_id = equipment_categories.id
        LEFT JOIN rarities
            ON rarities.id = equipment.rarity_id
        ORDER BY equipment.id ASC
    """)
    
    equipment = cursor.fetchall()

    print()
    print("--- Matériel ---")
    for equipment_id, equipment_name, equipment_category, equipment_description, equipment_color in equipment:
        color = COLORS[equipment_color]
        print(f'{equipment_id} - {color}{equipment_name}{RESET} - {YELLOW}{equipment_category}{RESET} - {DIM}{equipment_description}{RESET}')


def display_all_equipment_crafts(cursor):

    cursor.execute("""
    SELECT
        equipment.id,
        equipment.name,
        equipment.description,
        rarities.color,
        ingredients.name,
        equipment_craft.quantity
    FROM equipment_craft
    JOIN equipment
        ON equipment.id = equipment_craft.equipment_id
    JOIN rarities
        ON rarities.id = equipment.rarity_id
    JOIN ingredients
        ON ingredients.id = equipment_craft.ingredient_id
    ORDER BY equipment.id ASC
    """)

    result = cursor.fetchall()
    print()
    print("--- Fabrication ---")
    display_equipment_craft(result)


def display_equipment_craft(equipment_craft):

    current_id = None
    current_equipment = None
    craft_list = []
    
    for equipment in equipment_craft:
        equipment_id = equipment[0]
    
        if current_id is None:
            current_id = equipment_id
            current_equipment = equipment
    
        if current_id != equipment_id:

            if current_equipment is not None:  
                equipment_color = COLORS[current_equipment[3]]
    
                craft_text = ""

                for ingredient, quantity in craft_list:

                    if craft_text:
                        craft_text += " - "

                    craft_text += f"{ingredient} x{quantity}"
                        
                print(f"{current_equipment[0]} - {equipment_color}{current_equipment[1]}{RESET} : {craft_text}")
    
            current_equipment = equipment
            current_id = equipment_id
            craft_list = []
    
        ingredient = equipment[4]
        quantity = equipment[5]
    
        if ingredient is not None:
            craft_list.append((ingredient, quantity))
    
    equipment_color = COLORS[current_equipment[3]]
            
    craft_text = ""
    for ingredient, quantity in craft_list:
        if craft_text:
            craft_text += " - "
        craft_text += f"{ingredient} x{quantity}"
                                
    print(f"{equipment[0]} - {equipment_color}{equipment[1]}{RESET} : {craft_text}")