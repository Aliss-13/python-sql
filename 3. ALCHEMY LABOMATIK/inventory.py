# --------------------------------------- concerne la table inventory

def add_ingredient_to_inventory(cursor, connection, ingredient_id, quantity):

    cursor.execute("""
        SELECT ingredient_id
        FROM inventory
        WHERE ingredient_id = ?
    """, (ingredient_id,))

    result = cursor.fetchone()

    if result is not None:
    
        cursor.execute("""
            UPDATE inventory
            SET quantity = quantity + ?
            WHERE ingredient_id = ?
        """, (quantity, ingredient_id,))
    
        connection.commit()

    else:
            
        cursor.execute("""
            INSERT INTO inventory (ingredient_id, quantity)
            VALUES (?, ?)
        """, (ingredient_id, quantity))
            
        connection.commit()

# --------------------------------------- concerne la table container_inventory

def add_container_to_inventory(cursor, connection, equipment_id, quantity):

    cursor.execute("""
        SELECT equipment_id
        FROM container_inventory
        WHERE equipment_id = ?
    """, (equipment_id,))

    result = cursor.fetchone()

    if result is not None:
    
        cursor.execute("""
            UPDATE container_inventory
            SET quantity = quantity + ?
            WHERE equipment_id = ?
        """, (quantity, equipment_id,))
    
        connection.commit()

    else:
            
        cursor.execute("""
            INSERT INTO container_inventory (equipment_id, quantity)
            VALUES (?, ?)
        """, (equipment_id, quantity))
            
        connection.commit()
            


# ------------------------------------------ inventaire et craft ---------------------------------------

def check_inventory_for_ingredients_and_quantity(
    cursor,
    source_table,
    source_id_column,
    source_id,
    item_type
):

    cursor.execute(f"""
    SELECT
        ingredient_id,
        quantity
    FROM {source_table}
    WHERE {source_id_column} = ?
    """, (source_id,))

    result_item_to_craft_ingredients = cursor.fetchall()

    cursor.execute("""
        SELECT
            ingredient_id,
            quantity
        FROM inventory
    """)
    
    result_inventory = cursor.fetchall()
    
    inventory_has_required_ingredients = True
    
    for ingredient_id, required_quantity in result_item_to_craft_ingredients :
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
    
        elif not ingredient_has_required_quantity:
            inventory_has_required_ingredients = False

    if not inventory_has_required_ingredients:
        print(f"Vous n'avez pas assez d'ingrédients pour fabriquer {item_type}.")
    
    return inventory_has_required_ingredients, result_item_to_craft_ingredients