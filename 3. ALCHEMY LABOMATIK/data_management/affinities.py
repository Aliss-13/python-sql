import sqlite3
from display.display_ingredients import display_all_ingredients
from display.display_affinities_and_portals import display_all_affinities
from utils import id_exists, ask_positive_float_0_1


def get_affinity_ingredient_total_points(cursor, ingredient_id):

    cursor.execute("""
        SELECT SUM(value)
        FROM ingredient_affinities
        WHERE ingredient_id = ?
    """, (ingredient_id,))

    total_value = cursor.fetchone()[0]

    if total_value is None:
        total_value = 0

    return round(total_value, 2)


def get_affinity_recipe_discovery_total_points(cursor, recipe_id):

    cursor.execute("""
        SELECT SUM(value)
        FROM recipe_discovery
        WHERE recipe_id = ?
    """, (recipe_id,))

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

# pas plus de 2 affinités différentes 

    affinities = display_all_affinities(cursor)

    while True:

        cursor.execute("""
            SELECT COUNT(*)
            FROM ingredient_affinities
            WHERE ingredient_id = ?
        """, (ingredient_id,))

        count = cursor.fetchone()[0]

        if count >= 2:
            print("Cet ingrédient a 2 affinités.")
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

        total_value = get_affinity_ingredient_total_points(cursor, ingredient_id)

        if count == 1:
            remaining = round(1 - total_value, 2)
            value = remaining
            print(f"Dernière affinité : {remaining}")

        else:
            value = ask_positive_float_0_1("Valeur de l'affinité : ")

        new_total_value = round(total_value + value, 2)

        cursor.execute("""
            INSERT INTO ingredient_affinities (
                ingredient_id,
                affinity_id,
                value
            )
            VALUES (?, ?, ?)
            """, (ingredient_id, affinity_id, value))

        connection.commit()

        if new_total_value == 1:
            break