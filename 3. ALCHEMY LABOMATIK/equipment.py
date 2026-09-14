import sqlite3
from utils import id_exists
from display import display_all_equipment


def add_equipment(cursor, connection):

    name = input("Nom : ")

    description = input("Description : ")

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
            INSERT INTO equipment (name, description, rarity_id)
            VALUES (?, ?, ?)
        """, (name, description, rarity_id))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Ce matériel est déjà répertorié.")


def menu_update_equipment(cursor, connection):

    while True:
        print()
        print("--- Modifier matériel ---")
        print("[1] Nom")
        print("[2] Description")
        print("[4] Rareté")
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            update_equipment_name(cursor, connection)

        elif choix == "2":
            update_equipment_description(cursor, connection)

        elif choix == "3":
            update_equipment_rarity(cursor, connection)

        elif choix == "r":
            return

        else:
            print("Choix invalide")


def update_equipment_name(cursor, connection):
            
    display_all_equipment(cursor)
    
    while True:
    
        choix = input("Matériel choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "equipment", int(choix)):
            equipment_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_name = input("Nouveau nom : ")

    try:
        cursor.execute("""
            UPDATE equipment
            SET name = ?
            WHERE id = ?
            """, (new_name, equipment_id,))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Ce nom existe déjà.")


def update_equipment_description(cursor, connection):
            
    display_all_equipment(cursor)
    
    while True:
    
        choix = input("Matériel choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "equipment", int(choix)):
            equipment_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_description = input("Nouveau descriptif : ")

    cursor.execute("""
        UPDATE equipment
        SET description = ?
        WHERE id = ?
        """, (new_description, equipment_id,))

    connection.commit()


def update_equipment_rarity(cursor, connection):
            
    display_all_equipment(cursor)
    
    while True:
    
        choix = input("Matériel choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "equipment", int(choix)):
            equipment_id = int(choix)
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
        """, (new_rarity_id, equipment_id,))

    connection.commit()