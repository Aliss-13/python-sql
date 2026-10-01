import sqlite3

from display_colors_and_rarities import COLORS, RESET
from display_ingredients import display_all_ingredients
from display_recipes import display_all_recipes
from display_recipe_ingredients_and_products import display_all_recipes_ingredients, display_all_recipes_products

from utils import id_exists, ask_positive_int


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
        print("[9] Contenant")
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

        elif choix == "9":
            update_recipe_container(cursor, connection)
            
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
            print(f"{rarity[0]} - {rarity[1]}")
    
        choix = input("> ")
    
        if choix.isdigit() and 1 <= int(choix) <= len(rarities):
            new_rarity_id = int(choix)
            break
    
        print("Choix invalide.")
        return

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
            print(f"{category[0]} - {category[1]}")
    
        choix = input("> ")
    
        if choix.isdigit() and 1 <= int(choix) <= len(categories):
            new_category_id = int(choix)
            break
    
        print("Choix invalide.")
        return

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
            print(f"{target[0]} - {target[1]}")
    
        choix = input("> ")
    
        if choix.isdigit() and 1 <= int(choix) <= len(targets):
            new_target_id = int(choix)
            break
    
        print("Choix invalide.")
        return

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
        SELECT 
            equipment.id,
            equipment.name, 
            rarities.color
        FROM equipment
        JOIN rarities
            ON rarities.id = equipment.rarity_id
        WHERE equipment.category_id = 3
        """)
    
    fires = cursor.fetchall()
    fire_ids = [fire[0] for fire in fires]
    
    while True:
        print("--- Feux ---")
    
        for fire in fires:
            print(f"{fire[0]} - {COLORS[fire[2]]}{fire[1]}{RESET}")
        print("[0] Aucun")
    
        choix = input("> ")

        if choix == "0":
            new_fire_id = None
            break
    
        if choix.isdigit() and int(choix) in fire_ids:
            new_fire_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    cursor.execute("""
        UPDATE recipes
        SET fire_equipment_id = ?
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
        SELECT 
            equipment.id,
            equipment.name, 
            rarities.color
        FROM equipment
        JOIN rarities
            ON rarities.id = equipment.rarity_id
        WHERE equipment.category_id = 2
    """)
            
    melting_pots = cursor.fetchall()
    melting_pot_ids = [melting_pot[0] for melting_pot in melting_pots]
            
    while True:
        print("--- Creusets ---")
            
        for melting_pot in melting_pots:
            print(f"{melting_pot[0]} - {COLORS[melting_pot[2]]}{melting_pot[1]}{RESET}")
        print("[0] Aucun")

        choix = input("> ")

        if choix == "0":
            new_melting_pot_id = None
            break

        if choix.isdigit() and int(choix) in melting_pot_ids:
            new_melting_pot_id = int(choix)
            break
            
        print("Choix invalide.")
        return

    cursor.execute("""
        UPDATE recipes
        SET melting_pot_equipment_id = ?
        WHERE id = ?
    """, (new_melting_pot_id, recipe_id,))

    connection.commit()
    print ("Creuset mise à jour.")


def update_recipe_container(cursor, connection):
            
    display_all_recipes(cursor)
    
    while True:
                
        choix = input("Recette choisie : ")
                
        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
                
        print("Choix invalide.")
        return

    cursor.execute("""
        SELECT 
            equipment.id,
            equipment.name, 
            rarities.color
        FROM equipment
        JOIN rarities
            ON rarities.id = equipment.rarity_id
        WHERE equipment.category_id = 4
        """)
               
    containers = cursor.fetchall()
    containers_ids = [container[0] for container in containers]
                        
    while True:
        print()
        print("--- Contenants ---")
                        
        for container in containers:
            print(f"{container[0]} - {COLORS[container[2]]}{container[1]}{RESET}")
        print("[0] Aucun")
                        
        choix = input("> ")
        
        if choix == "0":
            new_container_id = None
            break
        
        if choix.isdigit() and int(choix) in containers_ids:
            new_container_id = int(choix)
            break
                        
        print("Choix invalide.")
        return

    cursor.execute("""
        UPDATE recipes
        SET container_equipment_id = ?
        WHERE id = ?
        """, (new_container_id, recipe_id,))

    connection.commit()
    print ("Contenant mis à jour.")


def add_recipe(cursor, connection):

    print()
    print("À chaque étape : q pour quitter.")

    # ========================================= NAME, DESCRIPTION, EFFECT

    name = input("Nom : ")

    if name == "q":
        return

    description = input("Description : ")

    if description == "q":
        return

    effect = input("Effet : ")

    if effect == "q":
        return

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
            print(f"{target[0]} - {target[1]}")
    
        choice = input("> ")

        if choice.isdigit() and 1 <= int(choice) <= len(targets):
            target_id = int(choice)
            break
    
        print("Choix invalide.")
        return

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
            print(f"{recipe_type[0]} - {recipe_type[1]}")

        choice = input("> ")

        if choice.isdigit() and 1 <= int(choice) <= len(recipe_types):
            recipe_type_id = int(choice)
            break

        print("Choix invalide.")
        return

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
            print(f"{rarity[0]} - {rarity[1]}")

        choice = input("> ")

        if choice.isdigit() and 1 <= int(choice) <= len(rarities):
            rarity_id = int(choice)
            break

        print("Choix invalide.")
        return

    # ========================================= FIRE EQUIPMENT

    cursor.execute("""
        SELECT 
            equipment.id,
            equipment.name, 
            rarities.color
        FROM equipment
        JOIN rarities
            ON rarities.id = equipment.rarity_id
        WHERE equipment.category_id = 3
    """)
    
    fires = cursor.fetchall()
    fire_ids = [fire[0] for fire in fires]
    
    while True:
        print()
        print("--- Feux ---")
    
        for fire in fires:
            print(f"{fire[0]} - {COLORS[fire[2]]}{fire[1]}{RESET}")
        print("[0] Aucun")
    
        choice = input("> ")
    
        if choice == "0":
            fire_id = None
            break

        if choice.isdigit() and int(choice) in fire_ids:
            fire_id = int(choice)
            break
    
        print("Choix invalide.")
        return

    # ========================================= MELTING POT EQUIPMENT

    cursor.execute("""
        SELECT 
            equipment.id,
            equipment.name, 
            rarities.color
        FROM equipment
        JOIN rarities
            ON rarities.id = equipment.rarity_id
        WHERE equipment.category_id = 2
    """)
                
    melting_pots = cursor.fetchall()
    melting_pot_ids = [melting_pot[0] for melting_pot in melting_pots]
                
    while True:
        print()
        print("--- Creusets ---")
                
        for melting_pot in melting_pots:
            print(f"{melting_pot[0]} - {COLORS[melting_pot[2]]}{melting_pot[1]}{RESET}")
        print("[0] Aucun")
                
        choice = input("> ")

        if choice == "0":
            melting_pot_id = None
            break

        if choice.isdigit() and int(choice) in melting_pot_ids:
            melting_pot_id = int(choice)
            break
                
        print("Choix invalide.")
        return

    # ========================================= CONTAINER EQUIPMENT
    
    cursor.execute("""
        SELECT 
            equipment.id,
            equipment.name, 
            rarities.color
        FROM equipment
        JOIN rarities
            ON rarities.id = equipment.rarity_id
        WHERE equipment.category_id = 4
    """)
                    
    containers = cursor.fetchall()
    containers_ids = [container[0] for container in containers]
                    
    while True:
        print()
        print("--- Contenants ---")
                    
        for container in containers:
            print(f"{container[0]} - {COLORS[container[2]]}{container[1]}{RESET}")
        print("[0] Aucun")
                    
        choice = input("> ")
    
        if choice == "0":
            container_id = None
            break
    
        if choice.isdigit() and int(choice) in containers_ids:
            container_id = int(choice)
            break
                    
        print("Choix invalide.")
        return

    try:
        cursor.execute("""
            INSERT INTO recipes (name, type_id, target_id, description, effect, rarity_id, fire_equipment_id, melting_pot_equipment_id, container_equipment_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, recipe_type_id, target_id, description, effect, rarity_id, fire_id, melting_pot_id, container_id))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Cette recette est déjà répertoriée.")



def add_recipe_ingredients(cursor, connection):

    print()
    print("À chaque étape : q pour quitter.")

# ========================================= choix recette

    cursor.execute("""
        SELECT 
            recipes.id, 
            recipes.name, 
            rarities.color
        FROM recipes
        JOIN rarities
            ON rarities.id = recipes.rarity_id
        ORDER BY recipes.rarity_id ASC
    """)

    recipes = cursor.fetchall()

    while True:
        print()
        print("--- Recettes ---")

        for recipe in recipes:
            print(f"{recipe[0]} - {COLORS[recipe[2]]}{recipe[1]}{RESET}")

        choice = input("> ")

        if choice.isdigit() and id_exists(cursor, "recipes", int(choice)):
            recipe_id = int(choice)
            break

        print("Choix invalide.")
        return

    # ========================================= choix ingrédients + quantité
    recipe_has_ingredients = False
    
    while True:

        display_all_ingredients(cursor)
        print()
        print("[0] = Terminer")

        choice = input("> ")

        if choice == "q":
            return
    
        if choice == "0":
            if not recipe_has_ingredients:
                connection.rollback()
                print("Saisie annulée.")
                return
            break

        if choice.isdigit() and id_exists(cursor, "ingredients", int(choice)):
            ingredient_id = int(choice)

        else:
            print("Choix invalide.")
            continue

        quantity = ask_positive_int("Quantité (666 pour quitter) : ")

        if quantity == "666": 
            return

        try:
            cursor.execute("""
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity)
                VALUES (?, ?, ?)
            """, (recipe_id, ingredient_id, quantity))
            
            recipe_has_ingredients = True
            
        except sqlite3.IntegrityError:
            print("Cet ingrédient est déjà répertorié dans cette recette.")
        
    connection.commit()


def add_recipe_products(cursor, connection):

    print()
    print("À chaque étape : q pour quitter.")

# ========================================= choix recette

    cursor.execute("""
        SELECT 
            recipes.id, 
            recipes.name, 
            rarities.color
        FROM recipes
        JOIN rarities
            ON rarities.id = recipes.rarity_id
        ORDER BY recipes.rarity_id ASC
    """)

    recipes = cursor.fetchall()

    while True:
        print()
        print("--- Recettes ---")

        for recipe in recipes:
            print(f"{recipe[0]} - {COLORS[recipe[2]]}{recipe[1]}{RESET}")

        choice = input("> ")

        if choice.isdigit() and id_exists(cursor, "recipes", int(choice)):
            recipe_id = int(choice)
            break

        print("Choix invalide.")
        return

    # ========================================= choix produits + quantité
    recipe_has_products = False
    
    while True:

        display_all_recipes(cursor)
        print()
        print("[0] = Terminer")

        choice = input("> ")

        if choice == "q":
            return
    
        if choice == "0":
            if not recipe_has_products:
                connection.rollback()
                print("Saisie annulée.")
                return
            break

        if choice.isdigit() and id_exists(cursor, "recipes", int(choice)):
            product_id = int(choice)

        else:
            print("Choix invalide.")
            continue

        quantity = ask_positive_int("Quantité (666 pour quitter) : ")

        if quantity == "666": 
            return

        try:
            cursor.execute("""
                INSERT INTO recipe_products (recipe_id, product_recipe_id, quantity)
                VALUES (?, ?, ?)
            """, (recipe_id, product_id, quantity))
            
            recipe_has_products = True
            
        except sqlite3.IntegrityError:
            print("Ce produit est déjà répertorié dans cette recette.")
        
    connection.commit()


def reset_recipe_ingredients(cursor, connection):

    display_all_recipes_ingredients(cursor)

    while True:
            
        recipe_id = input("Recette choisie : ")

        cursor.execute("""
            SELECT recipe_id
            FROM recipe_ingredients
            WHERE recipe_id = ?
        """, (recipe_id,))
                
        result = cursor.fetchone()
        
        if recipe_id.isdigit() and recipe_id is not None:
            recipe_id = int(recipe_id)
            break
    
        print("Choix invalide.")
        return

    cursor.execute("""  
        DELETE FROM recipe_ingredients
        WHERE recipe_id = ?
        """, (recipe_id,))

    connection.commit()
    print("Ingrédients supprimés de la recette.")


def reset_recipe_products(cursor, connection):

    display_all_recipes_products(cursor)

    while True:
            
        recipe_id = input("Recette choisie : ")

        cursor.execute("""
            SELECT recipe_id
            FROM recipe_products
            WHERE recipe_id = ?
        """, (recipe_id,))
                
        result = cursor.fetchone()
        
        if recipe_id.isdigit() and recipe_id is not None:
            recipe_id = int(recipe_id)
            break
    
        print("Choix invalide.")
        return

    cursor.execute("""  
        DELETE FROM recipe_products
        WHERE recipe_id = ?
        """, (recipe_id,))

    connection.commit()
    print("Produits supprimés de la recette.")
        
        