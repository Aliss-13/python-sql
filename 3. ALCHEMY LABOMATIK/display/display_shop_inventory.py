from display.display_utils import COLORS, RESET, YELLOW, display_description


def display_shop_inventory(cursor):

    cursor.execute("""
        SELECT
            shop_inventory.recipe_id,
            recipes.name,
            recipe_rarity.color,
            recipes.description,
            shop_inventory.quantity,
            recipe_types.name,
            recipes.selling_price
            
        FROM shop_inventory
    
        JOIN recipes
            ON recipes.id = shop_inventory.recipe_id
            
        JOIN rarities AS recipe_rarity
            ON recipe_rarity.id = recipes.rarity_id
    
        JOIN recipe_types
            ON recipe_types.id = recipes.type_id

        WHERE shop_inventory.quantity > 0

        ORDER BY recipe_types.id ASC, recipe_rarity.id ASC
    """)

    result = cursor.fetchall()

    for display_number, (recipe_id, name, color, description, quantity, recipe_type, selling_price) in enumerate (result, start=1):
        print(f'{display_number:<2} - {COLORS[color]}{name}{RESET} - {YELLOW}{recipe_type}{RESET} - x{quantity}')
        display_description(description)
        print(f"     Prix de vente : {selling_price} pièces")
        print()

    return result