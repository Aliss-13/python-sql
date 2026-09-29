from display import display_player_recipes_join_id_to_list_numbering, COLORS, RESET


def pick_recipe(cursor):

# affichage des recettes connues  

    player_recipes = display_player_recipes_join_id_to_list_numbering(cursor)

    # choix du joueur

    while True:
                 
        choix = input("Recette choisie (q pour revenir) : ") 

        if choix.lower() == "q":
            return None

        # récupération de l'identifiant de la recette

        if choix.isdigit() and 1 <= int(choix) <= len(player_recipes):
            recipe_id = player_recipes[int(choix)]
            break
            
        print("Choix invalide.")

    return recipe_id


def check_fire(cursor, recipe_id): # vérification feu dans l'équipement du joueur (player_equipment)

    cursor.execute("""
        SELECT 
            fire_equipment_id
            FROM recipes
            WHERE id = ?
    """, (recipe_id,))
                            
    result = cursor.fetchone()
    fire_equipment_id = result[0]
        
    cursor.execute("""
        SELECT
            equipment_id
        FROM player_equipment
    """)
                                
    result_equipment_ids = cursor.fetchall()

    player_equipment_has_required_fire = True 

    if fire_equipment_id is None:
        player_equipment_has_required_fire = True 
        
    else:
        fire_found = False

        for equipment_id, in result_equipment_ids:
            if fire_equipment_id == equipment_id:
                fire_found = True
                    
        if not fire_found:
            player_equipment_has_required_fire = False
            print("Vous n'avez pas le feu requis pour cette recette.")
            print()

    return player_equipment_has_required_fire


def check_melting_pot(cursor, recipe_id):  # vérification creuset dans l'équipement du joueur (player_equipment)

    cursor.execute("""
        SELECT 
            melting_pot_equipment_id
        FROM recipes
        WHERE id = ?
    """, (recipe_id,))
                                
    result = cursor.fetchone()
    melting_pot_equipment_id = result[0]
            
    cursor.execute("""
        SELECT
            equipment_id
        FROM player_equipment
    """)
                                    
    result_equipment_ids = cursor.fetchall()

    player_equipment_has_required_melting_pot = True

    if melting_pot_equipment_id is None:
        player_equipment_has_required_melting_pot = True

    else:
        melting_pot_found = False

        for equipment_id, in result_equipment_ids:
            if melting_pot_equipment_id == equipment_id: 
                melting_pot_found = True
                             
        if not melting_pot_found:
            player_equipment_has_required_melting_pot = False
            print("Vous n'avez pas le creuset requis pour cette recette.")
            print()

    return player_equipment_has_required_melting_pot


def check_inventory_for_ingredients_and_quantity(cursor, recipe_id):  # vérification ingrédients + quantité dans l'inventaire

    cursor.execute("""
        SELECT 
            ingredient_id, 
            quantity
        FROM recipe_ingredients
        WHERE recipe_id = ?
    """, (recipe_id,))
                    
    result_recipe_ingredients = cursor.fetchall()

    cursor.execute("""
        SELECT 
            ingredient_id, 
            quantity
        FROM inventory
    """)
                        
    result_inventory = cursor.fetchall()

    
    inventory_has_required_ingredients = True

    for ingredient_id, required_quantity in result_recipe_ingredients: 
    # | for a, b in liste_de_tuples: | signifie : « Pour chaque tuple de deux éléments, mets le premier dans a et le second dans b. »
        
        ingredient_found = False
        ingredient_has_required_quantity = False
        
        for inventory_ingredient_id, inventory_quantity in result_inventory: 
            
            if ingredient_id == inventory_ingredient_id:
                ingredient_found = True 

                if required_quantity <= inventory_quantity:
                    ingredient_has_required_quantity = True
                   
        
    if not ingredient_found:
        inventory_has_required_ingredients = False
        print("Vous n'avez pas les ingrédients requis pour cette recette.")
        print()

    else:
        if not ingredient_has_required_quantity:
            inventory_has_required_ingredients = False
            print("Vous n'avez pas assez d'ingrédients pour cette recette.")
            print()
            
    return inventory_has_required_ingredients, result_recipe_ingredients


def check_container_inventory_for_containers_and_quantity(cursor, recipe_id):  
# vérification contenants + quantité dans l'inventaire de contenants
    
    cursor.execute("""
        SELECT 
            container_equipment_id
        FROM recipes
        WHERE id = ?
    """, (recipe_id,))
                        
    result = cursor.fetchone()
    container_equipment_id = result[0]
    
    cursor.execute("""
        SELECT
            equipment_id, 
            quantity
        FROM container_inventory
    """)
                            
    result_container_inventory = cursor.fetchall()
    
        
    container_inventory_has_required_containers = True
    
    container_found = False
    
    for equipment_id, quantity in result_container_inventory: 
                
        if container_equipment_id == equipment_id: 
            if quantity >= 1:
                container_found = True
                     
    if not container_found:
        container_inventory_has_required_containers = False
        print("Vous n'avez pas le contenant requis pour cette recette.")
        print()

    return container_inventory_has_required_containers, container_equipment_id


def pick_product_destination(cursor, recipe_id):

    while True:
        print("--- Destination du produit ---")
        print("[1] 📓 Inventaire")
        print("[2] 💰 Boutique")

        destination = input("Destination : ")

        if destination == "1":

            cursor.execute("""
                SELECT recipe_id
                FROM product_inventory
            """)

            product_inventory_recipe_ids = cursor.fetchall()
            product_inventory_recipe_ids_unpacked = [product_inventory_recipe_id[0] for product_inventory_recipe_id in product_inventory_recipe_ids]


            if recipe_id not in product_inventory_recipe_ids_unpacked:

                cursor.execute("""
                    INSERT INTO product_inventory (recipe_id, quantity)
                    VALUES (?, ?)
                """, (recipe_id, 1))

            else:
                cursor.execute("""
                    UPDATE product_inventory
                    SET quantity = quantity + ?
                    WHERE recipe_id = ?
                """, (1, recipe_id))

            break

        if destination == "2":
            cursor.execute("""
                SELECT recipe_id
                FROM shop_inventory
            """)
            
            shop_inventory_recipe_ids = cursor.fetchall()
            shop_inventory_recipe_ids_unpacked = [shop_inventory_recipe_id[0] for shop_inventory_recipe_id in shop_inventory_recipe_ids]
            

            if recipe_id not in shop_inventory_recipe_ids_unpacked:
            
                cursor.execute("""
                    INSERT INTO shop_inventory (recipe_id, quantity)
                    VALUES (?, ?)
                """, (recipe_id, 1))
            
            else:

                cursor.execute("""
                    UPDATE shop_inventory
                    SET quantity = quantity + ?
                    WHERE recipe_id = ?
                """, (1, recipe_id))
            
            break

        print("Choix invalide.")


def crafted_is_true(cursor, recipe_id):

    cursor.execute("""
        UPDATE player_recipes
        SET crafted = 1
    WHERE recipe_id = ?
    """, (recipe_id,))


def craft_recipe(cursor, connection):

    recipe_id = pick_recipe(cursor)

    if recipe_id is None:
        return
    
    cursor.execute("""
        SELECT 
            recipes.name,
            rarities.color
        FROM recipes
        JOIN rarities
            ON rarities.id = recipes.rarity_id
        WHERE recipes.id = ?
        """, (recipe_id,))

    recipe_nc = cursor.fetchone()
    recipe_name = recipe_nc[0]
    recipe_color = recipe_nc[1]

    player_equipment_has_required_fire = check_fire(cursor, recipe_id)

    player_equipment_has_required_melting_pot = check_melting_pot(cursor, recipe_id)

    inventory_has_required_ingredients, result_recipe_ingredients = check_inventory_for_ingredients_and_quantity(cursor, recipe_id)

    container_inventory_has_required_containers, container_equipment_id = check_container_inventory_for_containers_and_quantity(cursor, recipe_id)
                              
    if player_equipment_has_required_fire:
        if player_equipment_has_required_melting_pot:
            if inventory_has_required_ingredients:
                if container_inventory_has_required_containers:
                    print(f"Vous fabriquez {COLORS[recipe_color]}{recipe_name}{RESET} !")
                    print()

                    pick_product_destination(cursor, recipe_id)

                    for ingredient_id, required_quantity in result_recipe_ingredients:

                        cursor.execute("""
                            UPDATE inventory
                            SET quantity = quantity - ?
                        WHERE ingredient_id = ?
                        """, (required_quantity, ingredient_id))
                
                    cursor.execute("""
                        UPDATE container_inventory
                        SET quantity = quantity - ?
                        WHERE equipment_id = ?
                    """, (1, container_equipment_id))

                    crafted_is_true(cursor, recipe_id)

                    connection.commit()