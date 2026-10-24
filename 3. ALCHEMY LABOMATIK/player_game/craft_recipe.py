from display.display_player_recipes import display_all_player_recipes_ingredients_products_and_equipments
from display.display_utils import COLORS, RESET

from player_game.game_functions.advance_game_tick import advance_game_tick

from player_game.get_achievements import check_crafted_recipes_achievements

#----------------------------------------------- craft recettes ----------------------------------------

def pick_recipe(cursor):

# affichage des recettes connues  

    recipe_infos = display_all_player_recipes_ingredients_products_and_equipments(cursor)

    if not recipe_infos:
        print("Vous ne connaissez pas encore de recette. Tentez de faire un mélange dans le  🧪 Laboratoire  pour en découvrir !")
        return

    # choix du joueur

    while True:
                 
        choice = input("Recette choisie (q pour revenir) : ") 

        if choice.lower() == "q":
            return None

        # récupération de l'identifiant de la recette

        if choice.isdigit() and 1 <= int(choice) <= len(recipe_infos):
            recipe_id = recipe_infos[int(choice) - 1][0]
            return recipe_id
    
        print("Choix invalide.")


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
        print("[2] 🐍 Youtique©")

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


#------------------------------------------------------ CRAFT RECIPE -------------------------------------------------------------

def consume_ingredients(cursor, required_ingredients):

    for ingredient_id, required_quantity in required_ingredients:
        cursor.execute("""
            UPDATE inventory
            SET quantity = quantity - ?
            WHERE ingredient_id = ?
              AND quantity >= ?
        """, (required_quantity, ingredient_id, required_quantity))

        if cursor.rowcount != 1:
            raise ValueError("Stock d'ingrédients insuffisant.")


def consume_products(cursor, required_products):

    for product_recipe_id, required_quantity in required_products:
        cursor.execute("""
            UPDATE product_inventory
            SET quantity = quantity - ?
            WHERE recipe_id = ?
              AND quantity >= ?
        """, (required_quantity, product_recipe_id, required_quantity))

        if cursor.rowcount != 1:
            raise ValueError("Stock de produits insuffisant.")


def consume_container(cursor, container_equipment_id):

    cursor.execute("""
        UPDATE container_inventory
        SET quantity = quantity - 1
        WHERE equipment_id = ?
          AND quantity >= 1
    """, (container_equipment_id,))

    if cursor.rowcount != 1:
        raise ValueError("Contenant indisponible.")
    
#-------------------------------------------------------------------------------------------------------------------------

def check_recipe_craftability(cursor, recipe_id):

    player_equipment_has_required_fire = check_fire(cursor, recipe_id)

    player_equipment_has_required_melting_pot = check_melting_pot(cursor, recipe_id)

    inventory_has_required_ingredients, required_ingredients = (check_inventory_for_items_and_quantity(
        cursor,
        "recipe_ingredients",
        "recipe_id",
        recipe_id,
        "ingredient_id",
        "inventory",
        "ingredient_id",
        "cette recette"
    ))


    product_inventory_has_required_products, required_products = (
    check_inventory_for_items_and_quantity(
        cursor,
        "recipe_products",
        "recipe_id",
        recipe_id,
        "product_recipe_id",
        "product_inventory",
        "recipe_id",
        "cette recette"
    )
)

    container_inventory_has_required_containers, container_equipment_id = check_container_inventory_for_containers_and_quantity(cursor, recipe_id)

    recipe_is_craftable = all((
        player_equipment_has_required_fire,
        player_equipment_has_required_melting_pot,
        inventory_has_required_ingredients,
        product_inventory_has_required_products,
        container_inventory_has_required_containers
    ))

    return (
        recipe_is_craftable,
        required_ingredients,
        required_products,
        container_equipment_id
    )

    
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
                              
    recipe_is_craftable, required_ingredients, required_products, container_equipment_id = (
    check_recipe_craftability(cursor, recipe_id))

    if not recipe_is_craftable:
        return

    try:

        consume_ingredients(cursor, required_ingredients)
        consume_products(cursor, required_products)
        consume_container(cursor, container_equipment_id)
        
        print(f"Vous fabriquez {COLORS[recipe_color]}{recipe_name}{RESET} !")
        print()

        pick_product_destination(cursor, recipe_id)
        
        crafted_recipe_is_true(cursor, recipe_id)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    else:
        check_crafted_recipes_achievements(cursor, connection)
        advance_game_tick(cursor, connection)


def crafted_recipe_is_true(cursor, recipe_id):

    cursor.execute("""
        UPDATE player_recipes
        SET crafted = 1
    WHERE recipe_id = ?
    """, (recipe_id,))

# ------------------------------------------ inventaire et craft ---------------------------------------

def check_inventory_for_items_and_quantity(
    cursor,
    source_table,
    source_id_column,
    source_id,
    source_item_column,
    inventory_table,
    inventory_item_column,
    item_type
):

    cursor.execute(f"""
        SELECT
            {source_item_column},
            quantity
        FROM {source_table}
        WHERE {source_id_column} = ?
    """, (source_id,))

    required_items = cursor.fetchall()

    cursor.execute(f"""
        SELECT
            {inventory_item_column},
            quantity
        FROM {inventory_table}
    """)

    inventory_items = dict(cursor.fetchall())

    inventory_has_required_items = True

    for item_id, required_quantity in required_items:

        available_quantity = inventory_items.get(item_id, 0)

        if available_quantity < required_quantity:
            inventory_has_required_items = False

    if not inventory_has_required_items:
        print(f"Vous n'avez pas assez de ressources pour fabriquer {item_type}.")

    return inventory_has_required_items, required_items