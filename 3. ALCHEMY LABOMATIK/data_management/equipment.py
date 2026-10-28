import sqlite3

from utils import id_exists

from display.display_equipment_and_equipment_craft import display_all_equipment
from display.display_utils import DIM, RESET


def add_equipment(cursor, connection):

    print()
    print("À chaque étape : Entrée pour quitter.")

    # =============================== NAME, DESCRIPTION

    name = input("Nom : ").strip().capitalize()

    if not name:
        return

    description = input("Description : ").strip()

    if not description:
        return

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
    
        choice = input(f"Catégorie {DIM}(Entrée pour revenir){RESET} : ")

        if not choice:
            return
    
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            new_category_id = int(choice)
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

        choice = input(f"Rareté {DIM}(Entrée pour revenir){RESET} : ")

        if not choice:
            return

        if choice.isdigit() and 1 <= int(choice) <= len(rarities):
            rarity_id = int(choice)
            break

        print("Choix invalide.")

    # ============================== SEUIL DE DEBLOCAGE NB DE DECOUVERTES

    while True:
    
        try:
            unlock_discoveries_threshold = int(input(f"Seuil de déblocage - nombre de découvertes {DIM}(Entrée pour revenir){RESET} : "))

            if not unlock_discoveries_threshold:
                return
    
            if unlock_discoveries_threshold >= 0 :
                break
            
            print("La valeur doit être 0 ou un entier positif.")
    
        except ValueError:
            print("Saisie invalide.")

    # =============================== COMMIT
    
    try:
        cursor.execute("""
            INSERT INTO equipment (name, description, rarity_id, category_id, unlock_discoveries)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, rarity_id, new_category_id, unlock_discoveries_threshold))

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
        print("[5] Déblocage via N découvertes")
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

        elif choix == "5":
            update_equipment_unlock_discoveries(cursor, connection)

        elif choix == "r":
            return

        else:
            print("Choix invalide")


def update_equipment_name(cursor, connection):
            
    display_all_equipment(cursor)
    
    while True:
    
        choice = input(f"Matériel choisi {DIM}(Entrée pour revenir){RESET} : ")

        if not choice:
            return
    
        if choice.isdigit() and id_exists(cursor, "equipment", int(choice)):
            equipment_id = int(choice)
            break
    
        print("Choix invalide.")

    new_name = input(f"Nouveau nom {DIM}(Entrée pour revenir){RESET} : ")

    if not new_name:
        return

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
    
        choice = input(f"Matériel choisi {DIM}(Entrée pour revenir){RESET} : ")
        
        if not choice:
            return
    
        if choice.isdigit() and id_exists(cursor, "equipment", int(choice)):
            equipment_id = int(choice)
            break
    
        print("Choix invalide.")

    new_description = input(f"Nouveau descriptif {DIM}(Entrée pour revenir){RESET} : ")

    if not new_description:
        return

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
    
        choice = input(f"Matériel choisi {DIM}(Entrée pour revenir){RESET} : ")
        
        if not choice:
            return
    
        if choice.isdigit() and id_exists(cursor, "equipment", int(choice)):
            equipment_id = int(choice)
            break
    
        print("Choix invalide.")

    cursor.execute("""
            SELECT id, name
            FROM rarities
        """)
    
    rarities = cursor.fetchall()
    
    while True:
        print("--- Rareté ---")
    
        for rarity in rarities:
            print(f"[{rarity[0]}] {rarity[1]}")
    
        choix = input(f"Rareté {DIM}(Entrée pour revenir){RESET} : ")
    
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
    
        choice = input("Matériel choisi : ")
    
        if choice.isdigit() and id_exists(cursor, "equipment", int(choice)):
            equipment_id = int(choice)
            break
    
        print("Choix invalide.")

    cursor.execute("""
            SELECT id, name
            FROM equipment_categories
        """)
    
    categories = cursor.fetchall()
    
    while True:
        print("--- Catégories ---")
    
        for category in categories:
            print(f"[{category[0]}] {category[1]}")
    
        choix = input(f"Catégorie {DIM}(Entrée pour revenir){RESET} : ")

        if not choice:
            return
    
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


def update_equipment_unlock_discoveries(cursor, connection):
            
    display_all_equipment(cursor)
    
    while True:
    
        choice = input(f"Matériel choisi {DIM}(Entrée pour revenir){RESET} : ")

        if not choice:
            return
    
        if choice.isdigit() and id_exists(cursor, "equipment", int(choice)):
            equipment_id = int(choice)
            break
    
        print("Choix invalide.")

    while True:

        try:
            unlock_discoveries_threshold = int(input(f"Seuil de déblocage - nombre de découvertes {DIM}(Entrée pour revenir){RESET} : "))

            if not unlock_discoveries_threshold:
                return

            if unlock_discoveries_threshold >= 0 :
                break

            print("La valeur doit être 0 ou un entier positif.")

        except ValueError:
            print("Saisie invalide.")

    try:
        cursor.execute("""
            UPDATE equipment
            SET unlock_discoveries = ?
            WHERE id = ?
            """, (unlock_discoveries_threshold, equipment_id,))

        connection.commit()
        print ("Seuil de déblocage - nombre de découvertes mis à jour.")

    except sqlite3.IntegrityError:
        print("Ce nom existe déjà.")