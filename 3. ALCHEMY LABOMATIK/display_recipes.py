from display_colors_and_rarities import COLORS, RESET, DIM, YELLOW, RED, CYAN, LIGHT_PINK


def display_all_recipes(cursor):

    cursor.execute("""
    SELECT

        recipes.id,
        recipes.name,
        recipe_types.id,
        targets.name,
        recipes.description,
        recipes.effect,
        rarities.color,
        fire.name,
        melting_pot.name,
        container.name

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

    LEFT JOIN equipment AS container
        ON container.id = recipes.container_equipment_id

    ORDER BY recipe_types.id ASC, recipes.rarity_id ASC
    """)
   
    result = cursor.fetchall()
    display_recipe(result)
    return(result)


def display_recipe(recipes):
    for recipe_id, name, type, target, description, effect, color, fire, melting_pot, container in recipes:
        print(
            f'{recipe_id:<2} - {COLORS[color]}{name}{RESET} - '
            f'{YELLOW}{type}{RESET} - {effect} ({target})'
            )
        
        print(f'     {RED}Feu : {fire or "Aucun"}{RESET} - {LIGHT_PINK}Creuset : {melting_pot or "Aucun"}{RESET} - '
              f'{CYAN}Contenant : {container or "Aucun"}{RESET}')
        print(f"     {DIM}{description}{RESET}")
        print()