from display.display_refactor import group_data_under_same_id, format_affinity_items
from display.display_utils import COLORS, RESET, DIM, YELLOW


def get_player_money(cursor):

    cursor.execute("""SELECT money
    FROM player
    WHERE id = 1""")
    
    money = cursor.fetchone()[0]
    print(f"💰 Bourse : {money} pièces.")


def return_inventory(cursor):

    cursor.execute("""
        SELECT
            inventory.ingredient_id,
            ingredients.name,
            inventory.quantity,
            ingredients.level,
            ingredients.description,
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
    return result


def display_inventory(cursor):

    result = return_inventory(cursor)

    print()
    print("🫧 Ingrédients")
    display_ingredient_from_inventory(result)
    return result


def display_ingredient_from_inventory(inventory):

    display_number = 0

    groups = group_data_under_same_id(inventory)

    for group in groups:

        affinity_list = []
        display_number += 1

        for ingredient in group:

            name = ingredient[1]
            quantity = ingredient[2]
            level = ingredient[3]
            description = ingredient[4]
            color = ingredient[5]
            affinity_icon = ingredient[6]
            affinity_value = ingredient[7]

            if affinity_icon is not None:
                affinity_list.append((affinity_icon, affinity_value))

        sorted_affinity_list = sorted(affinity_list, key=lambda x: x[1], reverse=True)
        
        affinity_text = format_affinity_items(sorted_affinity_list)

        
        print(f"{display_number:<2} - {COLORS[color]}{name}{RESET} {YELLOW}x{quantity}{RESET} {affinity_text} - {DIM}{description}{RESET}")

#----------------------------------------------- CONTAINER_INVENTORY ----------------------------------------------------

def display_container_inventory(cursor):

    cursor.execute("""
        SELECT
            container_inventory.equipment_id,
            equipment.name,
            rarities.color,
            equipment.description,
            container_inventory.quantity
        FROM container_inventory
        JOIN equipment
            ON equipment.id = container_inventory.equipment_id
        JOIN rarities
            ON rarities.id = equipment.rarity_id
        ORDER BY equipment.rarity_id ASC
    """)

    containers = cursor.fetchall()
    print()
    print("🫙 Contenants")
   
    display_container_from_container_inventory(containers)

    return containers


def display_container_from_container_inventory(container_inventory):

    display_number = 0

    groups = group_data_under_same_id(container_inventory)

    for group in groups:

        display_number += 1

        container = group[0]  # On prend le premier élément du groupe pour obtenir les informations du contenant

        container_name = container[1]
        container_color = COLORS[container[2]]
        container_description = container[3]
        container_quantity = container[4]

        print(f"{display_number} - {container_color}{container_name}{RESET} {YELLOW}x{container_quantity}{RESET} - {DIM}{container_description}{RESET}")

#----------------------------------------------- PRODUCT_INVENTORY ----------------------------------------------------

def display_product_inventory(cursor):

    cursor.execute("""
        SELECT
            product_inventory.recipe_id,
            recipes.name,
            rarities.color,
            recipes.description,
            product_inventory.quantity
        FROM product_inventory
        JOIN recipes
            ON recipes.id = product_inventory.recipe_id
        JOIN rarities
            ON rarities.id = recipes.rarity_id
        ORDER BY recipes.rarity_id ASC
    """)

    products = cursor.fetchall()
    print()
    print("🛍️ Produits fabriqués")
   
    display_product_from_product_inventory(products)

    return products


def display_product_from_product_inventory(product_inventory):

    groups = group_data_under_same_id(product_inventory)
    
    display_number = 0

    for group in groups:

        display_number += 1

        product = group[0]  # On prend le premier élément du groupe pour obtenir les informations du produit

        name = product[1]
        color = COLORS[product[2]]
        description = product[3]
        quantity = product[4]

        print(f"{display_number} - {color}{name}{RESET} {YELLOW}x{quantity}{RESET} - {DIM}{description}{RESET}")