import sqlite3
from utils import id_exists, ask_positive_int, ask_int
from display import display_all_equipment, display_all_ingredients, display_all_equipment_crafts


def add_equipment(cursor, connection):

    # =============================== NAME, DESCRIPTION

    name = input("Nom : ")

    description = input("Description : ")

    # =============================== CATEGORIES

    cursor.execute("""
        SELECT id, name
        FROM equipment_categories
        """)
    
    categories = cursor.fetchall()
    
    while True:
        print()
        print("--- Catégories ---")
    
        for category in categories:
            print(f"[{category[0]}] {category[1]}")
    
        choix = input("> ")
    
        if choix.isdigit() and 1 <= int(choix) <= len(categories):
            new_category_id = int(choix)
            break
    
        print("Choix invalide.")

    # =============================== RARITIES

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

    # =============================== COMMIT
    
    try:
        cursor.execute("""
            INSERT INTO equipment (name, description, rarity_id, category_id)
            VALUES (?, ?, ?, ?)
        """, (name, description, rarity_id, new_category_id))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Ce matériel est déjà répertorié.")


def menu_update_equipment(cursor, connection):

    while True:
        print()
        print("--- Modifier matériel ---")
        print("[1] Nom")
        print("[2] Description")
        print("[3] Rareté")
        print("[4] Catégorie")
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            update_equipment_name(cursor, connection)

        elif choix == "2":
            update_equipment_description(cursor, connection)

        elif choix == "3":
            update_equipment_rarity(cursor, connection)

        elif choix == "4":
            update_equipment_category(cursor, connection)

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
        print ("Nom mis à jour.")

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
    print ("Description mise à jour.")


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
        UPDATE equipment
        SET rarity_id = ?
        WHERE id = ?
        """, (new_rarity_id, equipment_id,))

    connection.commit()
    print ("Rareté mise à jour.")


def update_equipment_category(cursor, connection):
            
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
            FROM equipment_categories
        """)
    
    categories = cursor.fetchall()
    
    while True:
        print("--- Catégories ---")
    
        for category in categories:
            print(f"[{category[0]}] {category[1]}")
    
        choix = input("> ")
    
        if choix.isdigit() and 1 <= int(choix) <= len(categories):
            new_category_id = int(choix)
            break
    
        print("Choix invalide.")

    cursor.execute("""
        UPDATE equipment
        SET category_id = ?
        WHERE id = ?
        """, (new_category_id, equipment_id,))

    connection.commit()
    print ("Catégorie mise à jour.")


def add_equipment_craft(cursor, connection):

    display_all_equipment(cursor)
    equipment_id = ask_positive_int("Matériel : ")

    if not id_exists(cursor, "equipment", equipment_id):
        print("Matériel introuvable.")
        return

    equipment_has_craft = False

    while True:

        display_all_ingredients(cursor)
        ingredient_id = ask_int("Ingrédients pour le craft (0 = terminer) : ")

        if ingredient_id == 0:
            if not equipment_has_craft:
                connection.rollback()
                print("Saisie annulée.")
                return
            break

        if not id_exists(cursor, "ingredients", ingredient_id):
            print("Ingrédient introuvable.")
            connection.rollback()
            return

        quantity = ask_positive_int("Quantité : ")

        cursor.execute("""
            INSERT INTO equipment_craft (equipment_id, ingredient_id, quantity)
            VALUES (?, ?, ?)
        """, (equipment_id, ingredient_id, quantity))

        equipment_has_craft = True

    connection.commit()


def reset_equipment_craft(cursor, connection):

    display_all_equipment_crafts(cursor)

    while True:
            
        choix = input("Matériel choisi : ")

        cursor.execute("""
            SELECT equipment_id
            FROM equipment_craft
            WHERE equipment_id = ?
            """, (choix,))
        
        result = cursor.fetchone()

        if choix.isdigit() and result is not None:
            equipment_id = int(choix)
            break

        print("Choix invalide.")

    cursor.execute("""  
        DELETE FROM equipment_craft
        WHERE equipment_id = ?
        """, (equipment_id,))

    connection.commit()
    print("Matériaux nécessaires au craft de l'équipement supprimés.")


