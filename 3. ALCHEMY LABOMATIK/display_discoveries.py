from display_colors_and_rarities import COLORS, RESET, YELLOW
from display_refactor import group_data_under_same_id, format_affinity_items



def display_all_discoveries(cursor):

    cursor.execute("""
        SELECT
            recipe_discovery.recipe_id,
            recipes.name,
            rarities.color,
            recipe_types.id,
            recipe_discovery.number_of_ingredients,
            affinities.icon,
            recipe_discovery.value
        FROM recipe_discovery
        JOIN recipes
            ON recipes.id = recipe_discovery.recipe_id
        JOIN rarities
            ON rarities.id = recipes.rarity_id
        JOIN recipe_types
            ON recipe_types.id = recipes.type_id
        JOIN affinities
            ON affinities.id = recipe_discovery.affinity_id
        ORDER BY recipe_types.id, recipes.rarity_id ASC
        """)
   
    result = cursor.fetchall()
    display_discovery(result)
    return(result)


def display_discovery(recipe_discovery):

    groups = group_data_under_same_id(recipe_discovery)

    for group in groups:

        affinity_list = []

        for discovery in group:

            discovery_id = discovery[0]
            name = discovery[1]
            color = discovery[2]
            number_of_ingredients = discovery[4]
            affinity_icon = discovery[5]
            affinity_value = discovery[6]

            if affinity_icon is not None:
                affinity_list.append((affinity_icon, affinity_value))

        affinity_text = format_affinity_items(affinity_list)

        print(
                f'{discovery_id:<2} - {COLORS[color]}{name}{RESET} - '
                f'{YELLOW}Ingrédients : {number_of_ingredients}{RESET} - {affinity_text}')