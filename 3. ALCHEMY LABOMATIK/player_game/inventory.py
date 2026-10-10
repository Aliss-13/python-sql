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
            


