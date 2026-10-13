from player_game.blending import get_discovery_affinity_signature
from display.display_utils import COLORS, RESET, format_difficulty_stars, info_format_difficulty_stars


def get_recipe_research_clues(cursor, recipe_id):

    cursor.execute("""
        SELECT
            clue_rank
        FROM player_recipe_research
        WHERE recipe_id = ?
        ORDER BY clue_rank ASC
    """, (recipe_id,))

    clue_ranks = cursor.fetchall()

    clue_rank_unpacked = [clue_rank[0] for clue_rank in clue_ranks]
    
    return clue_rank_unpacked



def reveal_recipe_clues(cursor, recipe_id):

    clue_rank = get_recipe_research_clues(cursor, recipe_id)

    discoveries_affinities = get_discovery_affinity_signature(cursor)

    recipe_data = discoveries_affinities[recipe_id]

    (recipe_name, recipe_color, number_of_ingredients, difficulty_id, number_of_affinities, signature) = recipe_data
    
    
    info_format_difficulty_stars()

    print(clue_rank)
    print(number_of_affinities)
    print(signature)

    if 0 in clue_rank:
        print(f'{COLORS[recipe_color]}{recipe_name}{RESET}')
        print(f"Nombre d'ingrédients : {number_of_ingredients} - Difficulté : {format_difficulty_stars(difficulty_id)}")
    else:
        print(f"???")

    for clue in range (1, number_of_affinities + 1):

        if clue in clue_rank and clue <= len(signature):
            print(f"Affinité {clue} : {signature[clue - 1][0]}")

        elif clue_rank and clue > len(signature) and clue_rank[-1] == len(signature):
        # Je suis après la fin de la vraie signature ET le dernier rang découvert correspond au dernier rang réel.
            print(f"Affinité {clue} : aucune")

        else:
            print(f"Affinité {clue} : ???")
        
        




