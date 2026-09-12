def add_to_inventory(cursor, connection, ingredient_id, quantity):

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
            
