from display.display_utils import COLORS, RESET, YELLOW, display_recipe_description


def display_player_shop(cursor):

    cursor.execute("""
        SELECT
            recipes.name,
            recipes.description,
            recipe_types.name,
            recipe_rarity.color,
            recipes.selling_price, 
            shop_inventory.quantity
            
        FROM shop_inventory
    
        JOIN recipes
            ON recipes.id = shop_inventory.recipe_id
    
        JOIN recipe_types
            ON recipe_types.id = recipes.type_id
    
        JOIN rarities AS recipe_rarity
            ON recipe_rarity.id = recipes.rarity_id
    
        ORDER BY recipe_types.id ASC, recipe_rarity.id ASC
    """)

    result = cursor.fetchall()

    for display_number, (name, description, recipe_type, color, selling_price, quantity) in enumerate (result, start=1):
        print(f'{display_number:<2} - {COLORS[color]}{name}{RESET} - {YELLOW}{recipe_type}{RESET} - x{quantity}')
        display_recipe_description(description)
        print(f"     Prix de vente : {selling_price} pièces")
        print()

    return result