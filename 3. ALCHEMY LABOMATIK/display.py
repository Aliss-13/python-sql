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
        print(f'{aff_id} - {icon} - {name}')


#----------------------------------------------- AFFINITIES ----------------------------------------------------

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
        ORDER BY ingredients.rarity_id ASC
    """)

    result = cursor.fetchall()
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
                    
                print(f"{current_ingredient[0]} - {ingredient_color}{current_ingredient[1]}\033[0m ({affinity_text}) - Niv. {current_ingredient[3]} - Qté : {current_ingredient[2]}")
                

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
        
    print(f"{current_ingredient[0]} - {ingredient_color}{current_ingredient[1]}\033[0m ({affinity_text}) - Niv. {current_ingredient[3]} - Qté : {current_ingredient[2]}")



