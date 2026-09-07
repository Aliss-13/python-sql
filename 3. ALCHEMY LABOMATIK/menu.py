import sqlite3

YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
DIM = "\033[2m"
LIGHT_PINK = "\033[38;5;218m"
LIGHT_GREEN = "\033[38;5;120m"
PURPLE = "\033[95m"
RESET = "\033[0m"


COLORS = {
    "white": "\033[37m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "reset": "\033[0m",
}

def menu(cursor, connection):

    while True:

        print()
        print("========== ALCHEMY LABOMATIK ==========")
        print("[1] Ajouter affinité")
        print("[2] Voir affinités")
        print("[3] Ajouter ingrédient")
        print("[4] Voir ingrédients")
        print("[q] Quitter")

        choix = input("> ")

        if choix == "1":
            add_affinity(cursor, connection)

        elif choix == "2":
            display_all_affinities(cursor)

        elif choix == "3":
            add_ingredient(cursor, connection)

        elif choix == "4":
            display_all_ingredients(cursor)

        elif choix == "q":
            return

        else:
            print("Choix invalide")





def ask_positive_int(prompt):

    while True:

        try:
            value = int(input(prompt))

            if value > 0 :
                return value
            else:
                print("La valeur doit être positive.")

        except ValueError:
            print("Saisie invalide.")

# ----------------------------------- ingrédients --------------------------------------------

def add_ingredient(cursor, connection):

    name = input("Nom : ")

    description = input("Description : ")

    niveau = ask_positive_int("Niveau : ")

    cursor.execute("""
        SELECT id, name
        FROM rarities
    """)

    rarities = cursor.fetchall()

    while True:
        print("--- Rareté ---")

        for rarity in rarities:
            print(f"[{rarity[0]}] {rarity[1]}")

        choix = input("> ")

        if choix.isdigit() and 1 <= int(choix) <= len(rarities):
            rarity_id = int(choix)
            break

        print("Choix invalide.")


    try:
        cursor.execute("""
            INSERT INTO ingredients (name, description, level, rarity_id)
            VALUES (?, ?, ?, ?)
        """, (name, description, niveau, rarity_id))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Cet ingrédient existe déjà.")


def display_all_ingredients(cursor):

    cursor.execute("""
    SELECT
        ingredients.id,
        ingredients.name,
        ingredients.description,
        ingredients.level,
        rarities.color
    FROM ingredients
    JOIN rarities
        ON rarities.id = ingredients.rarity_id
    """)

    result = cursor.fetchall()
    display_ingredient(result)


def display_ingredient(ingredients):

    for ingredient in ingredients:
        ingredient_color = COLORS[ingredient[4]]
        print(f"{ingredient[0]} - {ingredient_color}{ingredient[1]}\033[0m - {DIM}{ingredient[2]}{RESET} - Niveau : {ingredient[3]}")

# ----------------------------------- affinités --------------------------------------------

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


def display_all_affinities(cursor):

    cursor.execute("""
    SELECT
        id,
        name
    FROM affinities
    """)

    result = cursor.fetchall()
    display_affinity(result)


def display_affinity(affinities):
    for aff_id, name in affinities:
        print(f'{aff_id} - {name}')