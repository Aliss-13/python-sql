import sqlite3

from display.display_utils import COLORS, RESET, dans_ton_q
from display.display_ingredients import display_all_ingredients
from display.display_recipes import display_all_recipes
from display.display_recipe_ingredients_products_and_equipment import display_all_recipes_ingredients, display_all_recipes_products

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
        print("[7] Difficulté à découvrir")
        print("[8] Feu")
        print("[9] Creuset")
        print("[10] Contenant")
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            update_recipe_name(cursor, connection)

        elif choix == "2":
            update_recipe_type(cursor, connection)

        elif choix == "3":
            update_recipe_target(cursor, connection)   

        elif choix == "4":
            update_recipe_description(cursor, connection)    

        elif choix == "5":
            update_recipe_effect(cursor, connection)

        elif choix == "6":
            update_recipe_rarity(cursor, connection)

        elif choix == "7":
            update_recipe_discovery_difficulty(cursor, connection)

        elif choix == "8":
            update_recipe_fire(cursor, connection)

        elif choix == "9":
            update_recipe_melting_pot(cursor, connection)

        elif choix == "10":
            update_recipe_container(cursor, connection)
            
        elif choix == "r":
            return

        else:
            print("Choix invalide")


def choose_recipe_to_update(cursor):

    display_all_recipes(cursor)
    
    while True:
    
        choix = input("Recette choisie : ")

        if choix.isdigit() and id_exists(cursor, "recipes", int(choix)):
            recipe_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    return recipe_id


def update_recipe_name(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

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
    
    recipe_id = choose_recipe_to_update(cursor)

    new_description = input("Nouveau descriptif : ")

    cursor.execute("""
        UPDATE recipes
        SET description = ?
        WHERE id = ?
        """, (new_description, recipe_id,))

    connection.commit()
    print ("Description mise à jour.")


def update_recipe_effect(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

    new_effect = input("Nouvel effet : ")

    cursor.execute("""
        UPDATE recipes
        SET effect = ?
        WHERE id = ?
        """, (new_effect, recipe_id,))

    connection.commit()
    print ("Effet mis à jour.")


def update_recipe_rarity(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

    new_rarity_id = add_recipe_rarity(cursor)

    cursor.execute("""
        UPDATE recipes
        SET rarity_id = ?
        WHERE id = ?
        """, (new_rarity_id, recipe_id,))

    connection.commit()
    print ("Rareté mise à jour.")


def update_recipe_type(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

    new_category_id = add_recipe_type

    cursor.execute("""
        UPDATE recipes
        SET type_id = ?
        WHERE id = ?
        """, (new_category_id, recipe_id,))

    connection.commit()
    print ("Catégorie mise à jour.")


def update_recipe_target(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

    new_target_id = add_recipe_target(cursor)

    cursor.execute("""
        UPDATE recipes
        SET target_id = ?
        WHERE id = ?
        """, (new_target_id, recipe_id,))

    connection.commit()
    print ("Catégorie mise à jour.")


def update_recipe_fire(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

    new_fire_id = add_recipe_fire(cursor)

    cursor.execute("""
        UPDATE recipes
        SET fire_equipment_id = ?
        WHERE id = ?
        """, (new_fire_id, recipe_id,))

    connection.commit()
    print ("Feu mis à jour.")



def update_recipe_melting_pot(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

    new_melting_pot_id = add_recipe_melting_pot(cursor)
       
    cursor.execute("""
        UPDATE recipes
        SET melting_pot_equipment_id = ?
        WHERE id = ?
    """, (new_melting_pot_id, recipe_id,))

    connection.commit()
    print ("Creuset mise à jour.")


def update_recipe_container(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

    new_container_id = add_recipe_container(cursor)

    cursor.execute("""
        UPDATE recipes
        SET container_equipment_id = ?
        WHERE id = ?
        """, (new_container_id, recipe_id,))

    connection.commit()
    print ("Contenant mis à jour.")



def update_recipe_discovery_difficulty(cursor, connection):
            
    recipe_id = choose_recipe_to_update(cursor)

    new_difficulty_id = add_recipe_discovery_difficulty(cursor)

    cursor.execute("""
        UPDATE recipes
        SET discovery_difficulty_id = ?
        WHERE id = ?
        """, (new_difficulty_id, recipe_id,))

    connection.commit()
    print ("Difficulté de la découverte mise à jour.")


# ---------------------------------------------- AJOUTER RECETTE ----------------------------------------------------------------

def add_recipe_name_description_and_effect():

    while True:

        name = input("Nom : ").strip()

        if name == "q":
            return

        if name:
            break

        print("Le nom ne peut pas être vide.")
    
    description = input("Description : ").strip()
    
    if description == "q":
        return
    
    effect = input("Effet : ").strip()
    
    if effect == "q":
        return

    return name, description, effect


def add_recipe_target(cursor):

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

    return target_id


def add_recipe_type(cursor):

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

    return recipe_type_id


def add_recipe_rarity(cursor):

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

    return rarity_id


def add_recipe_fire(cursor):

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

    return fire_id


def add_recipe_melting_pot(cursor):

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

    return melting_pot_id


def add_recipe_container(cursor):

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
    
    return container_id


def add_recipe_discovery_difficulty(cursor):

    cursor.execute("""
        SELECT id, name, number_of_affinities
        FROM recipe_discovery_difficulty
        """)
    
    difficulties = cursor.fetchall()
    
    while True:
        print()
        print("--- Difficulté de la découverte ---")
    
        for difficulty in difficulties:
            print(f"{difficulty[0]} - {difficulty[1]} - Nombre d'affinités à classer : {difficulty[2]}")
    
        choice = input("> ")
    
        if choice.isdigit() and 1 <= int(choice) <= len(difficulties):
            discovery_difficulty_id = int(choice)
            break
    
        print("Choix invalide.")
        return

    return discovery_difficulty_id

    
    
def add_recipe(cursor, connection):

    dans_ton_q() # Q FOR QUITTING

    name_description_effect = add_recipe_name_description_and_effect() # NAME, DESCRIPTION, EFFECT

    if name_description_effect is None: # c'est pour le q qui fait None, banane
        return

    name, description, effect = name_description_effect


    target_id = add_recipe_target(cursor) # TARGET

    recipe_type_id = add_recipe_type(cursor) # TYPE : POTION, ELIXIR, PENTAGRAMME

    rarity_id = add_recipe_rarity(cursor) # RARITY

    discovery_difficulty_id = add_recipe_discovery_difficulty(cursor)

    fire_id = add_recipe_fire(cursor) # FIRE

    melting_pot_id = add_recipe_melting_pot(cursor) # MELTING POT

    container_id = add_recipe_container(cursor) # CONTAINER  
    

    try:
        cursor.execute("""
            INSERT INTO recipes (name, type_id, target_id, description, effect, rarity_id, discovery_difficulty_id, fire_equipment_id, melting_pot_equipment_id, container_equipment_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, recipe_type_id, target_id, description, effect, rarity_id, discovery_difficulty_id, fire_id, melting_pot_id, container_id))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Cette recette est déjà répertoriée.")


# ---------------------------------------------- AJOUTER INGRéDIENTS à RECETTE ----------------------------------------------------------------

def choose_recipe_to_add_to(cursor):

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

    return recipe_id


def add_recipe_ingredients(cursor, connection):

    dans_ton_q()

# ========================================= choix recette

    recipe_id = choose_recipe_to_add_to(cursor)

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

# ---------------------------------------------- AJOUTER RECETTES PRODUITES (=PRODUCTS) à RECETTE ----------------------------------------------------------------

def add_recipe_products(cursor, connection):

    dans_ton_q()

    recipe_id = choose_recipe_to_add_to(cursor) # choix recette

# ============================================ choix produits + quantité
    
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


# ---------------------------------------------- Réinitialiser INGREDIENTS et PRODUCTS d'une RECETTE ----------------------------------------------------------------

def reset_recipe_ingredients(cursor, connection):

    display_all_recipes_ingredients(cursor)

    recipe_id = input("Recette choisie : ")
    
    if not recipe_id.isdigit():
        print("Choix invalide.")
        return
    
    recipe_id = int(recipe_id)
    
    cursor.execute("""  
        DELETE FROM recipe_ingredients
        WHERE recipe_id = ?
        """, (recipe_id,))

    connection.commit()
    print("Ingrédients supprimés de la recette.")


def reset_recipe_products(cursor, connection):

    display_all_recipes_products(cursor)

    recipe_id = input("Recette choisie : ")

    if not recipe_id.isdigit():
        print("Choix invalide.")
        return

    recipe_id = int(recipe_id)
        
    cursor.execute("""  
        DELETE FROM recipe_products
        WHERE recipe_id = ?
        """, (recipe_id,))

    connection.commit()
    print("Produits supprimés de la recette.")   