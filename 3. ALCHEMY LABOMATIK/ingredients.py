import sqlite3
from display import display_all_ingredients
from utils import ask_positive_int, id_exists


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



def menu_update_ingredient(cursor, connection):

    while True:
        print()
        print("--- Modifier ingrédient ---")
        print("[1] Nom")
        print("[2] Description")
        print("[3] Niveau")
        print("[4] Rareté")
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            update_ingredient_name(cursor, connection)

        elif choix == "2":
            update_ingredient_description(cursor, connection)

        elif choix == "3":
            update_ingredient_level(cursor, connection)

        elif choix == "4":
            update_ingredient_rarity(cursor, connection)

        elif choix == "r":
            return

        else:
            print("Choix invalide")


def update_ingredient_name(cursor, connection):
            
    display_all_ingredients(cursor)
    
    while True:
    
        choix = input("Ingrédient choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "ingredients", int(choix)):
            ingredient_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_name = input("Nouveau nom : ")

    try:
        cursor.execute("""
            UPDATE ingredients
            SET name = ?
            WHERE id = ?
            """, (new_name, ingredient_id,))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Ce nom existe déjà.")


def update_ingredient_description(cursor, connection):
            
    display_all_ingredients(cursor)
    
    while True:
    
        choix = input("Ingrédient choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "ingredients", int(choix)):
            ingredient_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_description = input("Nouveau descriptif : ")

    cursor.execute("""
        UPDATE ingredients
        SET description = ?
        WHERE id = ?
        """, (new_description, ingredient_id,))

    connection.commit()


def update_ingredient_level(cursor, connection):
            
    display_all_ingredients(cursor)
    
    while True:
    
        choix = input("Ingrédient choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "ingredients", int(choix)):
            ingredient_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_level = ask_positive_int("Nouveau niveau : ")

    cursor.execute("""
        UPDATE ingredients
        SET level = ?
        WHERE id = ?
        """, (new_level, ingredient_id,))

    connection.commit()


def update_ingredient_rarity(cursor, connection):
            
    display_all_ingredients(cursor)
    
    while True:
    
        choix = input("Ingrédient choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "ingredients", int(choix)):
            ingredient_id = int(choix)
            break
    
        print("Choix invalide.")
        return

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
            new_rarity_id = int(choix)
            break
    
        print("Choix invalide.")

    cursor.execute("""
        UPDATE ingredients
        SET rarity_id = ?
        WHERE id = ?
        """, (new_rarity_id, ingredient_id,))

    connection.commit()