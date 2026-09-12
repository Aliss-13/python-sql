import sqlite3
from display import display_all_ingredients, display_all_affinities
from utils import id_exists, ask_positive_float_0_1


def get_affinity_total_points(cursor, ingredient_id):

    cursor.execute("""
        SELECT SUM(value)
        FROM ingredient_affinities
        WHERE ingredient_id = ?
    """, (ingredient_id,))

    total_value = cursor.fetchone()[0]

    if total_value is None:
        total_value = 0

    return round(total_value, 2)


def add_affinity(cursor, connection):

    name = input("Nom : ")

    try:
        cursor.execute("""
            INSERT INTO affinities (name)
            VALUES (?)
        """, (name,))
        connection.commit()
        print("Affinité ajoutée !")

    except sqlite3.IntegrityError:
        print("Cette affinité existe déjà.")

    connection.commit()


def add_affinity_to_ingredient(cursor, connection):

# choix ingrédient à modifier 

    display_all_ingredients(cursor)

    while True:
            
        choix = input("Ingrédient choisi : ")

        if choix.isdigit() and id_exists(cursor, "ingredients", int(choix)):
            ingredient_id = int(choix)
            break

        print("Choix invalide.")
        return

# pas plus de 3 affinités différentes 

    affinities = display_all_affinities(cursor)

    while True:

        cursor.execute("""
            SELECT COUNT(*)
            FROM ingredient_affinities
            WHERE ingredient_id = ?
        """, (ingredient_id,))

        count = cursor.fetchone()[0]

        if count >= 3:
            print("Cet ingrédient possède déjà 3 affinités.")
            break

# pas deux fois la même affinité

        while True:

            choix = input("Affinité à associer : ")

            if choix.isdigit() and 1 <= int(choix) <= len(affinities):
                affinity_id = int(choix)

                cursor.execute("""
                    SELECT 1
                    FROM ingredient_affinities
                    WHERE ingredient_id = ?
                    AND affinity_id = ?
                """, (ingredient_id, affinity_id))

                affinity = cursor.fetchone()

                if affinity is not None:
                    print("Cette affinité est déjà associée à cet ingrédient.")
                    continue

                break

            print("Choix invalide.")

# points à attribuer entre 0 et 1

        total_value = get_affinity_total_points(cursor, ingredient_id)

        if total_value == 1:
            print("La somme des affinités est à son maximum.")
            return

        elif total_value > 1: 
            print("La somme des affinités ne doit pas dépasser 1.") 
            return

        remaining = round(1 - total_value, 2)
        print(f"Il reste {remaining} à répartir.")
        
        if count == 2:
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
            INSERT INTO ingredient_affinities (
                ingredient_id,
                affinity_id,
                value
            )
            VALUES (?, ?, ?)
            """, (ingredient_id, affinity_id, value))

        connection.commit()

        total_value = get_affinity_total_points(cursor, ingredient_id)

        if total_value == 1:
            print("Tous les points ont été répartis.")
            break

        remaining = round(1 - total_value, 2)
        print(f"Il reste {remaining} à répartir.")
        continue


def reset_ingredient_affinities(cursor, connection):

    display_all_ingredients(cursor)

    while True:
            
        choix = input("Ingrédient choisi : ")

        if choix.isdigit() and id_exists(cursor, "ingredients", int(choix)):
            ingredient_id = int(choix)
            break

        print("Choix invalide.")

    cursor.execute("""  
        DELETE FROM ingredient_affinities
        WHERE ingredient_id = ?
        """, (ingredient_id,))

    connection.commit()
    print("Affinités de l'ingrédient supprimées.")
