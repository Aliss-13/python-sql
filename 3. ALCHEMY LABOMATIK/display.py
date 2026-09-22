YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
DIM = "\033[2m"
LIGHT_PINK = "\033[38;5;218m"
LIGHT_GREEN = "\033[38;5;120m"
PURPLE = "\033[95m"
ORANGE = "\033[38;5;208m"
RED = "\033[38;5;196m"
RESET = "\033[0m"


COLORS = {
    "white": "\033[37m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "reset": "\033[0m",
}

#----------------------------------------------- SQL INFO ----------------------------------------------------

def display_tables(cursor):
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tables = cursor.fetchall()

    for table in tables:
        print(table[0])


def display_tables_info(cursor):

    for table in ["rarities", "affinities", "ingredients", "ingredient_affinities", "inventory", "equipment", 
              "equipment_categories", "equipment_craft", "mixing_tools", "recipes", "recipe_types",
              "recipe_discovery"]:
        print(f"\n--- {table} ---")

        cursor.execute(f"PRAGMA table_info({table})")

        for column in cursor.fetchall():
            print(column)


def display_new_table_contents(cursor):
    print()
    print("=> Contenu de targets")
    cursor.execute("SELECT * FROM targets")
    print(cursor.fetchall())
    print()


def display_FK(cursor):
    print()
    print("=> Liste clés étrangères recipes")
    cursor.execute("""
        PRAGMA foreign_key_list(recipes)
    """)

    for row in cursor.fetchall():
        print(row)


#----------------------------------------------- DISCOVERIES ----------------------------------------------------

def display_all_discoveries(cursor):

    cursor.execute("""
    SELECT
        recipe_discovery.recipe_id,
        recipes.name,
        rarities.color,
        recipe_discovery.number_of_ingredients,
        affinities.icon,
        recipe_discovery.value
    FROM recipe_discovery
    JOIN recipes
        ON recipes.id = recipe_discovery.recipe_id
    JOIN rarities
        ON rarities.id = recipes.rarity_id
    JOIN affinities
        ON affinities.id = recipe_discovery.affinity_id
    ORDER BY recipes.name ASC
    """)
   
    result = cursor.fetchall()
    display_discovery(result)
    return(result)


def display_discovery(recipe_discovery):

    affinity_list = []
    current_id = None
    current_discovery = None


    for discovery in recipe_discovery:
        discovery_id = discovery[0]
        

        if current_id is None:
            current_id = discovery_id
            current_discovery = discovery

        if current_id != discovery_id:
            if current_discovery is not None:
                color = COLORS[current_discovery[2]]

                affinity_text = ""

                for icon, value in affinity_list:
                    if affinity_text:
                        affinity_text += " - "

                    affinity_text += f"{icon} {value}"

                print(f'{current_discovery[0]} - {color}{current_discovery[1]}{RESET} - '
                        f'{YELLOW}Ingrédients : {current_discovery[3]}{RESET} - '
                        f'Mélange : {affinity_text}'
                    )

            current_discovery = discovery
            current_id = discovery_id
            affinity_list = []
                
        icon = discovery[4]
        value = discovery[5]
                
        if icon is not None:
            affinity_list.append((icon, value))

    color = COLORS[current_discovery[2]]
                
    affinity_text = ""
                
    for icon, value in affinity_list:
        if affinity_text:
            affinity_text += " - "
                
        affinity_text += f"{icon} {value}"
                
    print(
        f'{current_discovery[0]} - {color}{current_discovery[1]}{RESET} - '
        f'{YELLOW}Ingrédients : {current_discovery[3]}{RESET} - '
        f'Mélange : {affinity_text}'
    )
        
#----------------------------------------------- RECIPES ----------------------------------------------------

def display_all_recipes(cursor):

    cursor.execute("""
    SELECT
        recipes.id,
        recipes.name,
        recipe_types.name,
        targets.name,
        recipes.description,
        recipes.effect,
        rarities.color,
        fire.name,
        melting_pot.name
    FROM recipes
    JOIN recipe_types
        ON recipe_types.id = recipes.type_id
    JOIN targets
        ON targets.id = recipes.target_id
    JOIN rarities
        ON rarities.id = recipes.rarity_id
    LEFT JOIN equipment AS fire
        ON fire.id = recipes.fire_equipment_id
    LEFT JOIN equipment AS melting_pot
        ON melting_pot.id = recipes.melting_pot_equipment_id
    ORDER BY recipes.name ASC
    """)
   
    result = cursor.fetchall()
    display_recipe(result)
    return(result)


def display_recipe(recipes):
    for id, name, type, target, description, effect, color, fire, melting_pot in recipes:
        print(
            f'{id} - {COLORS[color]}{name}{RESET} - '
            f'{YELLOW}{type}{RESET} - {effect} ({target}) - '
            f'{RED}Feu : {fire or "Aucun"}{RESET} - {LIGHT_PINK}Creuset : {melting_pot or "Aucun"}{RESET}'
        )
        print(f"{DIM}{description}{RESET}")


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
    ORDER BY rarities.id ASC
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
    display_number = 1

    for ingredient in inventory:
        ingredient_id = ingredient[0]

        if current_id is None:
            current_id = ingredient_id
            current_ingredient = ingredient
            display_number = 1

        if current_id != ingredient_id:

            if current_ingredient is not None:
                
                ingredient_color = COLORS[current_ingredient[4]]

                affinity_text = ""
                for icon, value in affinity_list:

                    if affinity_text:
                        affinity_text += " - "

                    affinity_text += f"{icon} {value}"
                    
                print(f"{display_number} - {ingredient_color}{current_ingredient[1]}{RESET} {YELLOW}x{current_ingredient[2]}{RESET} ({affinity_text}) - Niv. {current_ingredient[3]}")

            affinity_list = []
            current_id = ingredient_id
            current_ingredient = ingredient
            display_number += 1

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
        
    print(f"{display_number} - {ingredient_color}{current_ingredient[1]}{RESET} {YELLOW}x{current_ingredient[2]}{RESET} ({affinity_text}) - Niv. {current_ingredient[3]}")


def display_inventory_join_id_to_list_numbering(cursor):

    inventory = display_inventory(cursor)

    numbering = {}

    display_number = 1
    current_id = None

    for ingredient in inventory:
        ingredient_id = ingredient[0]

        if current_id is None:
            current_id = ingredient_id
            numbering[display_number] = ingredient_id

        if current_id != ingredient_id:
            current_id = ingredient_id
            display_number += 1
            numbering[display_number] = ingredient_id

    return numbering
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
        ORDER BY equipment_categories.id, equipment.rarity_id ASC
        
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

#----------------------------------------------- INSTRUMENTS : MIXING TOOLS ----------------------------------------------------

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

    current_id = None
    current_mixing_tool = None
    display_number = 1

    for mixing_tool in mixing_tools:
        mixing_tool_id = mixing_tool[0]

        if current_id is None:
            current_id = mixing_tool_id
            current_mixing_tool = mixing_tool
            display_number = 1

        if current_id != mixing_tool_id:
            if current_mixing_tool is not None:
                mixing_tool_color = COLORS[current_mixing_tool[2]]
                print(f"{display_number} - {mixing_tool_color}{current_mixing_tool[1]}{RESET} - Nombre d'ingrédients : {current_mixing_tool[3]}")

            current_id = mixing_tool_id
            current_mixing_tool = mixing_tool
            display_number += 1

        mixing_tool_color = COLORS[current_mixing_tool[2]]
    print(f"{display_number} - {mixing_tool_color}{current_mixing_tool[1]}{RESET} - Nombre d'ingrédients : {current_mixing_tool[3]}")
        
    
def display_mixing_tools_join_id_to_list_numbering(cursor):

    mixing_tools = display_all_mixing_tools(cursor)

    numbering = {}

    display_number = 1
    current_id = None

    for mixing_tool in mixing_tools:
        mixing_tool_id = mixing_tool[0]

        if current_id is None:
            current_id = mixing_tool_id
            numbering[display_number] = mixing_tool_id

        if current_id != mixing_tool_id:
            current_id = mixing_tool_id
            display_number += 1
            numbering[display_number] = mixing_tool_id

    return numbering