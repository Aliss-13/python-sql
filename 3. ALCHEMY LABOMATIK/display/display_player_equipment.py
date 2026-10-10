from display.display_utils import COLORS, RESET, DIM, YELLOW


def display_all_player_equipments(cursor):

    cursor.execute("""
    SELECT
        equipment.id,
        equipment.name,
        equipment.description,
        equipment_rarity.color,
        equipment_categories.name
     
    FROM player_equipment

    JOIN equipment
        ON equipment.id = player_equipment.equipment_id

    JOIN rarities AS equipment_rarity
        ON equipment_rarity.id = equipment.rarity_id

    JOIN equipment_categories
        ON equipment_categories.id = equipment.category_id

    WHERE player_equipment.crafted = 1

    ORDER BY
        equipment.category_id ASC,
        equipment.rarity_id ASC,
        equipment.id ASC
    """)

    result = cursor.fetchall()
    print()
    display_player_equipment(result)
    return result


def display_player_equipment(player_equipment):

    if not player_equipment:
        print("Vous ne possédez aucun équipement.")
        return

    for equipment in player_equipment:
        equipment_id = equipment[0]
        equipment_name = equipment[1]
        equipment_description = equipment[2]
        equipment_color = equipment[3]
        equipment_category_name = equipment[4]
            
                        
        print(f'{COLORS[equipment_color]}{equipment_name}{RESET} - {YELLOW}{equipment_category_name}{RESET}') 
        print(f'{DIM}{equipment_description}{RESET}')
        print()