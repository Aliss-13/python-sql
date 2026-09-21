import sqlite3

from display import display_all_recipes
from utils import id_exists



def menu_update_recipe(cursor, connection):

    while True:
        print()
        print("--- Modifier recette ---")
        print("[1] Nom")
        print("[2] Catégorie")
        print("[3] Cible")
        print("[4] Description")
        print("[5] Effet")
        print("[6] Rareté")
        print("[7] Feu")
        print("[8] Creuset")
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            update_recipe_name(cursor, connection)

        elif choix == "2":
            update_recipe_category(cursor, connection)

        elif choix == "3":
            update_recipe_target(cursor, connection)   

        elif choix == "4":
            update_recipe_description(cursor, connection)    

        elif choix == "5":
            update_recipe_effect(cursor, connection)

        elif choix == "6":
            update_recipe_rarity(cursor, connection)

        elif choix == "7":
            update_recipe_fire(cursor, connection)

        elif choix == "8":
            update_recipe_melting_pot(cursor, connection)
            
        elif choix == "r":
            return

        else:
            print("Choix invalide")



def update_recipe_name(cursor, connection):
            
    display_all_recipes(cursor)
    
    while True:
    
        choix = input("Recette choisie : ")
    
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_name = input("Nouveau nom : ")

    try:
        cursor.execute("""
            UPDATE recipes
            SET name = ?
            WHERE id = ?
            """, (new_name, recipe_id,))

        connection.commit()
        print ("Nom mis à jour.")

    except sqlite3.IntegrityError:
        print("Ce nom existe déjà.")


def update_recipe_description(cursor, connection):
            
    display_all_recipes(cursor)
    
    while True:
        
        choix = input("Recette choisie : ")
        
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
        
        print("Choix invalide.")
        return

    new_description = input("Nouveau descriptif : ")

    cursor.execute("""
        UPDATE recipes
        SET description = ?
        WHERE id = ?
        """, (new_description, recipe_id,))

    connection.commit()
    print ("Description mise à jour.")


def update_recipe_effect(cursor, connection):
            
    display_all_recipes(cursor)
    
    while True:
        
        choix = input("Recette choisie : ")
        
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
        
        print("Choix invalide.")
        return

    new_effect = input("Nouvel effet : ")

    cursor.execute("""
        UPDATE recipes
        SET effect = ?
        WHERE id = ?
        """, (new_effect, recipe_id,))

    connection.commit()
    print ("Description mise à jour.")


def update_recipe_rarity(cursor, connection):
            
    display_all_recipes(cursor)
        
    while True:
            
        choix = input("Recette choisie : ")
            
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
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
        UPDATE recipes
        SET rarity_id = ?
        WHERE id = ?
        """, (new_rarity_id, recipe_id,))

    connection.commit()
    print ("Rareté mise à jour.")


def update_recipe_category(cursor, connection):
            
    display_all_recipes(cursor)
    
    while True:
                
        choix = input("Recette choisie : ")
                
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
                
        print("Choix invalide.")
        return

    cursor.execute("""
            SELECT id, name
            FROM recipe_types
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
        UPDATE recipes
        SET category_id = ?
        WHERE id = ?
        """, (new_category_id, recipe_id,))

    connection.commit()
    print ("Catégorie mise à jour.")


def update_recipe_target(cursor, connection):
            
    display_all_recipes(cursor)
    
    while True:
                
        choix = input("Recette choisie : ")
                
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
                
        print("Choix invalide.")
        return

    cursor.execute("""
        SELECT id, name
        FROM targets
        """)
    
    targets = cursor.fetchall()
    
    while True:
        print("--- Cible ---")
    
        for target in targets:
            print(f"[{target[0]}] {target[1]}")
    
        choix = input("> ")
    
        if choix.isdigit() and 1 <= int(choix) <= len(targets):
            new_target_id = int(choix)
            break
    
        print("Choix invalide.")

    cursor.execute("""
        UPDATE recipes
        SET target_id = ?
        WHERE id = ?
        """, (new_target_id, recipe_id,))

    connection.commit()
    print ("Catégorie mise à jour.")


def update_recipe_fire(cursor, connection):
            
    display_all_recipes(cursor)
    
    while True:
                
        choix = input("Recette choisie : ")
                
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
                
        print("Choix invalide.")
        return

    cursor.execute("""
            SELECT id, name
            FROM equipment
            WHERE category_id = 3
        """)
    
    fires = cursor.fetchall()
    fire_ids = [fire[0] for fire in fires]
    
    while True:
        print("--- Feux ---")
    
        for fire in fires:
            print(f"[{fire[0]}] {fire[1]}")
    
        choix = input("> ")
    
        if choix.isdigit() and int(choix) in fire_ids:
            new_fire_id = int(choix)
            break
    
        print("Choix invalide.")

    cursor.execute("""
        UPDATE recipes
        SET category_id = ?
        WHERE id = ?
        """, (new_fire_id, recipe_id,))

    connection.commit()
    print ("Feu mis à jour.")



def update_recipe_melting_pot(cursor, connection):
            
    display_all_recipes(cursor)
    
    while True:
                
        choix = input("Recette choisie : ")
                
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
                
        print("Choix invalide.")
        return

    cursor.execute("""
        SELECT id, name
        FROM equipment
        WHERE category_id = 2
    """)
            
    melting_pots = cursor.fetchall()
    melting_pot_ids = [melting_pot[0] for melting_pot in melting_pots]
            
    while True:
        print("--- Creusets ---")
            
        for melting_pot in melting_pots:
            print(f"[{melting_pot[0]}] {melting_pot[1]}")
            
            choix = input("> ")
            
            if choix.isdigit() and int(choix) in melting_pot_ids:
                new_melting_pot_id = int(choix)
                break
            
            print("Choix invalide.")

        cursor.execute("""
            UPDATE recipes
            SET category_id = ?
            WHERE id = ?
            """, (new_melting_pot_id, recipe_id,))

        connection.commit()
        print ("Creuset mise à jour.")


def add_recipe(cursor, connection):


    # ========================================= NAME, DESCRIPTION, EFFECT

    name = input("Nom : ")

    description = input("Description : ")

    effect = input("Effet : ")

    # ========================================= TYPE : POTION, ELIXIR, PENTAGRAMME

    cursor.execute("""
        SELECT id, name
        FROM recipe_types
    """)

    recipe_types = cursor.fetchall()

    while True:
        print()
        print("--- Type ---")

        for recipe_type in recipe_types:
            print(f"[{recipe_type[0]}] {recipe_type[1]}")

        choix = input("> ")

        if choix.isdigit() and 1 <= int(choix) <= len(recipe_types):
            recipe_type_id = int(choix)
            break

        print("Choix invalide.")

    # ========================================= TARGET

    cursor.execute("""
        SELECT id, name
        FROM targets
    """)
    
    targets = cursor.fetchall()
    
    while True:
        print()
        print("--- Cible ---")
    
        for target in targets:
            print(f"[{target[0]}] {target[1]}")
    
        choix = input("> ")

        if choix.isdigit() and 1 <= int(choix) <= len(targets):
            target_id = int(choix)
            break
    
        print("Choix invalide.")

    # ========================================= RARITY

    cursor.execute("""
        SELECT id, name
        FROM rarities
    """)

    rarities = cursor.fetchall()

    while True:
        print()
        print("--- Rareté ---")

        for rarity in rarities:
            print(f"[{rarity[0]}] {rarity[1]}")

        choix = input("> ")

        if choix.isdigit() and 1 <= int(choix) <= len(rarities):
            rarity_id = int(choix)
            break

        print("Choix invalide.")

    # ========================================= FIRE EQUIPMENT

    cursor.execute("""
        SELECT id, name
        FROM equipment
        WHERE category_id = 3 
    """)
    
    fires = cursor.fetchall()
    fire_ids = [fire[0] for fire in fires]
    
    while True:
        print()
        print("--- Feux ---")
    
        for fire in fires:
            print(f"[{fire[0]}] {fire[1]}")
        print("[0] Aucun")
    
        choix = input("> ")
    
        if choix == "0":
            fire_id = None
            break

        if choix.isdigit() and int(choix) in fire_ids:
            fire_id = int(choix)
            break
    
        print("Choix invalide.")

    # ========================================= MELTING POT EQUIPMENT

    cursor.execute("""
        SELECT id, name
        FROM equipment
        WHERE category_id = 2
    """)
                
    melting_pots = cursor.fetchall()
    melting_pot_ids = [melting_pot[0] for melting_pot in melting_pots]
                
    while True:
        print()
        print("--- Creusets ---")
                
        for melting_pot in melting_pots:
            print(f"[{melting_pot[0]}] {melting_pot[1]}")
        print("[0] Aucun")
                
        choix = input("> ")

        if choix == "0":
            melting_pot_id = None
            break

        if choix.isdigit() and int(choix) in melting_pot_ids:
            melting_pot_id = int(choix)
            break
                
        print("Choix invalide.")

    try:
        cursor.execute("""
            INSERT INTO recipes (name, type_id, target_id, description, effect, rarity_id, fire_equipment_id, melting_pot_equipment_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, recipe_type_id, target_id, description, effect, rarity_id, fire_id, melting_pot_id))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Cette recette est déjà répertoriée.")