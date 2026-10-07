from display_utils import COLORS, RESET, YELLOW, RED, CYAN, LIGHT_PINK, ORANGE, display_recipe_description, format_difficulty_stars


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
        container.name

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

    ORDER BY recipe_types.id ASC, recipes.rarity_id ASC
    """)
   
    result = cursor.fetchall()
    print()
    print(f'Difficulté découverte {LIGHT_PINK}(nb affinités){RESET} : ★ très facile {LIGHT_PINK}(2){RESET} - '
          f'★★ facile {LIGHT_PINK}(3){RESET} - ★★★ moyen {LIGHT_PINK}(4){RESET} - ★★★★ difficile {LIGHT_PINK}(5){RESET} - '
          f'★★★★★ très difficile {LIGHT_PINK}(6){RESET}')
    print()
    display_recipe(result)
    return(result)


def display_recipe(recipes):
    for recipe_id, name, type, target, description, effect, color, discovery_difficulty, fire, melting_pot, container in recipes:
        print(
            f'{recipe_id:<2} - {COLORS[color]}{name}{RESET} - '
            f'{YELLOW}{type}{RESET} - {format_difficulty_stars(discovery_difficulty)} - '
            f'{effect} ({target})'
            )
        
        print(f'     {RED}Feu : {fire or "Aucun"}{RESET} - {ORANGE}Creuset : {melting_pot or "Aucun"}{RESET} - '
              f'{CYAN}Contenant : {container or "Aucun"}{RESET}')
        display_recipe_description(description)
        print()


