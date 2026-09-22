from display import display_all_recipes, display_all_affinities, display_all_discoveries
from utils import id_exists, ask_positive_int, ask_positive_float_0_1
from affinities import get_affinity_recipe_discovery_total_points

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


    # entre 1 et 6 affinités différentes 

    affinities = display_all_affinities(cursor)

    while True:

        cursor.execute("""
            SELECT COUNT(*)
            FROM recipe_discovery
            WHERE recipe_id = ?
        """, (recipe_id,))

        count = cursor.fetchone()[0]

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
            
        recipe_id = input("Découverte choisie : ")

        cursor.execute("""
            SELECT affinity_id, value
            FROM recipe_discovery
            WHERE recipe_id = ?
        """, (recipe_id,))
                
        result = cursor.fetchone()
        
        if recipe_id.isdigit() and recipe_id is not None:
            recipe_id = int(recipe_id)
            break
    
        print("Choix invalide.")

    cursor.execute("""  
        DELETE FROM recipe_discovery
        WHERE recipe_id = ?
        """, (recipe_id,))

    connection.commit()
    print("Affinités de l'ingrédient supprimées.")
