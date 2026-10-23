from display.display_affinities_and_portals import display_all_affinities
from display.display_recipes import display_all_recipes
from display.display_discoveries import display_all_discoveries, display_discoveries_to_modify
from display.display_refactor import group_data_under_same_id

from utils import id_exists, ask_positive_int, ask_positive_float_0_1

from data_management.affinities import get_affinity_recipe_discovery_total_points



def menu_update_discovery(cursor, connection):

    while True:
        print()
        print("--- Modifier découverte ---")
        print("[1] Nombre d'ingrédients")
        print("[2] Réinitialiser affinités")
        
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            update_number_of_ingredients(cursor, connection)

        elif choix == "2":
            reset_discovery_affinities(cursor, connection)
            
        elif choix == "r":
            return

        else:
            print("Choix invalide")



def update_number_of_ingredients(cursor, connection):

    display_all_recipes(cursor)
    recipe_id = ask_positive_int("Recette choisie : ")

    if not id_exists(cursor, "recipes", recipe_id):
        print("Recette introuvable.")
        return
    
    allowed_number_of_ingredients = [2, 3, 4, 5, 6]
    
    number_of_ingredients = ask_positive_int("Nombre d'ingrédients (2, 3, 4, 5, 6) : ")
    
    if number_of_ingredients not in allowed_number_of_ingredients:
        print("Nombre d'ingrédients invalide.")
        return

    cursor.execute("""
        UPDATE recipe_discovery
        SET number_of_ingredients = ?
        WHERE recipe_id = ?
    """, (number_of_ingredients, recipe_id,))
    
    connection.commit()
    print("Nombre d'ingrédients mis à jour.")




def add_recipe_discovery(cursor, connection):

    recipes = display_discoveries_to_modify(cursor)
    choice = ask_positive_int("Recette choisie (666 pour quitter) : ")

    if 1 <= choice <= len(recipes):
        recipe_id = choice
        print(recipe_id)

    else:
        print("Choix invalide.")
        return
    
    allowed_number_of_ingredients = [2, 3, 4, 5, 6]

    number_of_ingredients = ask_positive_int("Nombre d'ingrédients (2, 3, 4, 5, 6) : ")

    if number_of_ingredients not in allowed_number_of_ingredients:
        print("Nombre d'ingrédients invalide.")
        return


    # entre 1 et 6 affinités différentes 

    affinities = display_all_affinities(cursor)

    while True:

        cursor.execute("""
            SELECT COUNT(*)
            FROM recipe_discovery
            WHERE recipe_id = ?
        """, (recipe_id,))

        count = cursor.fetchone()[0]
        print(count)

        if count >= 6:
            print("Ce mélange possède déjà le nombre maximum d'affinités.")
            break

    # pas deux fois la même affinité

        while True:

            affinity_id = input("Affinité à associer : ")

            if affinity_id.isdigit() and 1 <= int(affinity_id) <= len(affinities):
                affinity_id = int(affinity_id)

                cursor.execute("""
                    SELECT 1
                    FROM recipe_discovery
                    WHERE recipe_id = ?
                    AND affinity_id = ?
                """, (recipe_id, affinity_id))

                affinity = cursor.fetchone()

                if affinity is not None:
                    print("Cette affinité est déjà associée à ce mélange.")
                    continue

                break

            print("Choix invalide.")
            return

    # points à attribuer entre 0 et 1

        total_value = get_affinity_recipe_discovery_total_points(cursor, recipe_id)

        if total_value == 1:
            print("La somme des affinités est à son maximum.")
            return

        elif total_value > 1: 
            print("La somme des affinités ne doit pas dépasser 1.") 
            return

        remaining = round(1 - total_value, 2)
        print(f"Il reste {remaining} à répartir.")
        
        if count == 5:
            value = remaining
            print(f"Dernière affinité : {value}")

        else:
            while True:
                value = ask_positive_float_0_1("Valeur de l'affinité : ")

                if value > remaining:
                    print("La valeur saisie dépasse la quantité disponible.")
                    continue

                break

        cursor.execute("""
            INSERT INTO recipe_discovery (
                recipe_id,
                number_of_ingredients,
                affinity_id,
                value
            )
            VALUES (?, ?, ?, ?)
            """, (recipe_id, number_of_ingredients, affinity_id, value))

        connection.commit()

        total_value = get_affinity_recipe_discovery_total_points(cursor, recipe_id)

        if total_value == 1:
            print("Tous les points ont été répartis.")
            break

        remaining = round(1 - total_value, 2)
        print(f"Il reste {remaining} à répartir.")
        continue


def reset_discovery_affinities(cursor, connection):

    display_all_discoveries(cursor)

    while True:
            
        recipe_id = ask_positive_int("Découverte choisie : ")
        
        cursor.execute("""
            SELECT affinity_id, value
            FROM recipe_discovery
            WHERE recipe_id = ?
        """, (recipe_id,))
                
        result = cursor.fetchone()
        
        if result is not None:
            break
        
        print("Choix invalide.")
        return

    cursor.execute("""  
        DELETE FROM recipe_discovery
        WHERE recipe_id = ?
        """, (recipe_id,))

    print("Lignes supprimées :", cursor.rowcount)

    connection.commit()
    print("Affinités de la découverte supprimées.")



# ------------------------------------------------ Récupère les signatures des découvertes ----------------------------------------------------------------

def get_discovery_affinity_signature(cursor):

    cursor.execute("""

        SELECT 
            recipes.id,
            recipes.name,
            recipe_types.name,
            rarities.color,
            recipe_discovery.number_of_ingredients,
            recipes.discovery_difficulty_id,
            recipe_discovery_difficulty.number_of_affinities,
            affinities.icon,
            recipe_discovery.value
            
        FROM recipe_discovery

        JOIN recipes
            ON recipes.id = recipe_discovery.recipe_id

        JOIN recipe_types
            ON recipes.type_id = recipe_types.id

        JOIN rarities
            ON rarities.id = recipes.rarity_id

        JOIN recipe_discovery_difficulty
            ON recipe_discovery_difficulty.id = recipes.discovery_difficulty_id

        JOIN affinities
            ON affinities.id = recipe_discovery.affinity_id

        ORDER BY recipe_discovery.recipe_id
    """)

    result = cursor.fetchall()

    groups = group_data_under_same_id(result)

    discoveries_affinities = {}

    for group in groups:

        signature = []
        discovery_id = group[0][0] # id recette découverte > construction signature > tri > regroupement par id > signature
        discovery_name = group[0][1] # nom recette découverte
        discovery_type = group[0][2] # type recette découverte potion, élixir, pentagramme
        discovery_color = group[0][3] # couleur recette découverte
        discovery_number_of_ingredients = group[0][4] # nombre d'ingrédients à mélanger pour obtenir la découverte
        difficulty_id = group[0][5] # difficulté recette découverte
        difficulty_number_of_affinities = group [0][6] # difficulté nb affinités recette découverte
        

        for _, _, _, _, _, _, _, icon, value in group:
            signature.append((icon, value))
        signature.sort(key=lambda x: x[1], reverse=True)
        
        discoveries_affinities[discovery_id] = (discovery_name, discovery_type, discovery_color, discovery_number_of_ingredients, difficulty_id, difficulty_number_of_affinities, signature)

    return discoveries_affinities


def get_number_of_discoveries(cursor):

    cursor.execute("""
        SELECT COUNT(*)
        FROM player_recipes
    """)
    discovery_count = cursor.fetchone()[0]

    return discovery_count