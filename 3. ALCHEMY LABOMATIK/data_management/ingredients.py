import sqlite3
from display.display_ingredients import display_all_ingredients
from utils import ask_positive_int, id_exists


def add_ingredient(cursor, connection):
    print()
    print("À chaque étape : q pour quitter.")

    name = input("Nom : ") 

    if name == "q":
        return

    description = input("Description : ")

    if description == "q":
        return

    level = ask_positive_int("Niveau : ")

    if level == "q":
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

        choice = input("> ")

        if choice.isdigit() and 1 <= int(choice) <= len(rarities):
            rarity_id = int(choice)
            break

        print("Choix invalide.")
        return

    # ============================== SEUIL DE DEBLOCAGE NB DE DECOUVERTES
    
    while True:
    
        try:
            unlock_discoveries_threshold = int(input("Seuil de déblocage - nombre de découvertes : "))
    
            if unlock_discoveries_threshold >= 0 :
                break
    
            print("La valeur doit être 0 ou un entier positif.")
    
        except ValueError:
            print("Saisie invalide.")

    try:
        cursor.execute("""
            INSERT INTO ingredients (name, description, level, rarity_id, unlock_discoveries)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, level, rarity_id, unlock_discoveries_threshold))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Cet ingrédient est déjà répertorié.")



def menu_update_ingredient(cursor, connection):

    while True:
        print()
        print("--- Modifier ingrédient ---")
        print("[1] Nom")
        print("[2] Description")
        print("[3] Niveau")
        print("[4] Rareté")
        print("[5] Déblocage via N découvertes")
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

        elif choix == "5":
            update_ingredient_unlock_discoveries(cursor, connection)

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

    new_name = input("Nouveau nom (q pour quitter) : ")

    if new_name == "q": 
        return

    try:
        cursor.execute("""
            UPDATE ingredients
            SET name = ?
            WHERE id = ?
            """, (new_name, ingredient_id,))

        connection.commit()
        print("Nom mis à jour.")

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

    new_description = input("Nouveau descriptif (q pour quitter) : ")

    if new_description == "q": 
        return

    cursor.execute("""
        UPDATE ingredients
        SET description = ?
        WHERE id = ?
        """, (new_description, ingredient_id,))

    connection.commit()
    print("Description mise à jour.")


def update_ingredient_level(cursor, connection):
            
    display_all_ingredients(cursor)
    
    while True:
    
        choix = input("Ingrédient choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "ingredients", int(choix)):
            ingredient_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_level = ask_positive_int("Nouveau niveau (q pour quitter) : ")

    if new_level == "q": 
        return

    cursor.execute("""
        UPDATE ingredients
        SET level = ?
        WHERE id = ?
        """, (new_level, ingredient_id,))

    connection.commit()
    print("Niveau mis à jour.")


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
        return

    cursor.execute("""
        UPDATE ingredients
        SET rarity_id = ?
        WHERE id = ?
        """, (new_rarity_id, ingredient_id,))

    connection.commit()
    print("Rareté mise à jour.")


def update_ingredient_unlock_discoveries(cursor, connection):
            
    display_all_ingredients(cursor)
    
    while True:
    
        choice = input("Ingrédient choisi : ")
    
        if choice.isdigit() and id_exists(cursor, "ingredients", int(choice)):
            ingredient_id = int(choice)
            break
    
        print("Choix invalide.")
        return

    while True:

        try:
            unlock_discoveries_threshold = int(input("Seuil de déblocage - nombre de découvertes : "))

            if unlock_discoveries_threshold >= 0 :
                break

            print("La valeur doit être 0 ou un entier positif.")

        except ValueError:
            print("Saisie invalide.")

    try:
        cursor.execute("""
            UPDATE ingredients
            SET unlock_discoveries = ?
            WHERE id = ?
            """, (unlock_discoveries_threshold, ingredient_id,))

        connection.commit()
        print ("Seuil de déblocage - nombre de découvertes mis à jour.")

    except sqlite3.IntegrityError:
        print("Ce nom existe déjà.")



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