from display_utils import COLORS, RESET, DIM
from display_refactor import group_data_under_same_id, format_affinity_items

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

    groups = group_data_under_same_id(ingredients)

    for group in groups:

        affinity_list = []

        for ingredient in group:
            ingredient_id = ingredient[0]
            name = ingredient[1]
            description = ingredient[2]
            level = ingredient[3]
            color = ingredient[4]
            icon = ingredient[5]
            value = ingredient[6]

            if icon is not None:
                affinity_list.append((icon, value))

        sorted_affinity_list = sorted(affinity_list, key=lambda x: x[1], reverse=True)
        
        affinity_text = format_affinity_items(sorted_affinity_list)
                    
        print(f"{ingredient_id:<2} - {COLORS[color]}{name}{RESET}  {affinity_text}  - {DIM}{description}{RESET}") #- {DIM}Niv. {level}{RESET} à rajouter si besoin
