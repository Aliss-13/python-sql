from display.display_utils import COLORS, RESET, YELLOW, RED, CYAN, LIGHT_PINK, ORANGE, display_recipe_description, format_difficulty_stars, info_format_difficulty_stars


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
        recipe_discovery_difficulty.id,
        fire.name,
        melting_pot.name,
        container.name, 
        recipes.selling_price, 
        recipes.demand

    FROM recipes

    JOIN recipe_types
        ON recipe_types.id = recipes.type_id

    JOIN targets
        ON targets.id = recipes.target_id

    JOIN rarities
        ON rarities.id = recipes.rarity_id
    
    LEFT JOIN recipe_discovery_difficulty
        ON recipe_discovery_difficulty.id = recipes.discovery_difficulty_id

    LEFT JOIN equipment AS fire
        ON fire.id = recipes.fire_equipment_id

    LEFT JOIN equipment AS melting_pot
        ON melting_pot.id = recipes.melting_pot_equipment_id

    LEFT JOIN equipment AS container
        ON container.id = recipes.container_equipment_id

    ORDER BY recipe_types.id ASC, recipes.rarity_id ASC, recipes.selling_price ASC
    """)
   
    result = cursor.fetchall()
    print()
    info_format_difficulty_stars()
    display_recipe(result)
    return(result)


def display_recipe(recipes):
    for display_number, (recipe_id, name, recipe_type, target, description, effect, color, discovery_difficulty, fire, melting_pot, container, 
                         selling_price, demand) in enumerate (recipes, start=1):
        print(
            f'{display_number:<2} - {COLORS[color]}{name}{RESET} - '
            f'{YELLOW}{recipe_type}{RESET} - {format_difficulty_stars(discovery_difficulty)} - '
            f'{effect} ({target})'
            )
        
        print(f'     {RED}Feu : {fire or "Aucun"}{RESET} - {ORANGE}Creuset : {melting_pot or "Aucun"}{RESET} - '
              f'{CYAN}Contenant : {container or "Aucun"}{RESET}')
        display_recipe_description(description)
        print(f"     Prix de vente : {selling_price} pièces - Demande : {demand}")
        print()


