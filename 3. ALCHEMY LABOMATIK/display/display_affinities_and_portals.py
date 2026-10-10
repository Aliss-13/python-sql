from display.display_utils import COLORS, RESET

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