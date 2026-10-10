from player_game.craft_recipe import check_inventory_for_ingredients_and_quantity
from player_game.initialization import initialize_player_equipment

from display.display_utils import COLORS, RESET
from display.display_equipment_and_equipment_craft import display_equipment_craft


#----------------------------------------------- craft feu et creuset ----------------------------------------

def pick_equipment(cursor):

    cursor.execute("""
        SELECT COUNT(*)
        FROM player_recipes
    """)

    discovery_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT

        equipment.id,
        equipment.name,
        equipment.description,
        rarities.color,
        equipment_categories.name,
        ingredients.name,
        equipment_craft.quantity,
        ingredient_rarity.color

    FROM equipment_craft

    JOIN equipment
        ON equipment.id = equipment_craft.equipment_id

    JOIN rarities
        ON rarities.id = equipment.rarity_id
    
    JOIN equipment_categories
        ON equipment_categories.id = equipment.category_id
        
    JOIN ingredients
        ON ingredients.id = equipment_craft.ingredient_id

    JOIN rarities AS ingredient_rarity
        ON ingredient_rarity.id = ingredients.rarity_id
        
    JOIN player_equipment
        ON player_equipment.equipment_id = equipment.id
    
    WHERE equipment.unlock_discoveries <= ?
    AND player_equipment.crafted = 0
    ORDER BY equipment_categories.id, equipment.rarity_id ASC
    """, (discovery_count,))

    equipment_to_craft = cursor.fetchall()

    print()
    print("--- Fabrication ---")
    display_equipment_craft(equipment_to_craft)


    available_equipment = []

    for equipment in equipment_to_craft:
        equipment_id = equipment[0]

        if equipment_id not in available_equipment:
            available_equipment.append(equipment_id)

    # choix du joueur

    while True:

        choice = input("Equipement à fabriquer (q pour revenir) : ") 

        if choice.lower() == "q":
            return None, None

        # récupération de l'identifiant de l'équipement

        if choice.isdigit() and 1 <= int(choice) <= len(available_equipment):
            equipment_id = available_equipment[int(choice) - 1]
            return equipment_id, equipment_to_craft

        print("Choix invalide.")



def craft_equipment(cursor, connection):

    equipment_id, equipment_to_craft = pick_equipment(cursor)

    if equipment_id is None:
        return

    inventory_has_required_ingredients, result_item_to_craft_ingredients = check_inventory_for_ingredients_and_quantity(
    cursor, "equipment_craft", "equipment_id", equipment_id, "cet équipement")

    if not inventory_has_required_ingredients:
        return

    equipment_name = None
    equipment_color = None

    for equipment in equipment_to_craft:

        if equipment[0] == equipment_id:
            equipment_name = equipment[1]
            equipment_color = equipment[3]
            break

    if equipment_name is None:
        print("Impossible de retrouver cet équipement.")
        return

    print(f"Vous fabriquez {COLORS[equipment_color]}{equipment_name}{RESET} !")
    print()
    
    for ingredient_id, required_quantity in result_item_to_craft_ingredients:
        cursor.execute("""
            UPDATE inventory
            SET quantity = quantity - ?
            WHERE ingredient_id = ?
        """, (required_quantity, ingredient_id))
   
    crafted_equipment_is_true(cursor, equipment_id)

    connection.commit()


def crafted_equipment_is_true(cursor, equipment_id):

    cursor.execute("""
        UPDATE player_equipment
        SET crafted = 1
    WHERE equipment_id = ?
    """, (equipment_id,))