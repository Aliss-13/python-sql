def delete_customer(cursor, connection):

    all_customers(cursor)
    customer_id = int(input("Client à supprimer : "))

    cursor.execute("""
        SELECT
            id,
            product_id,
            quantity
        FROM sales
        WHERE customer_id = ?
    """, (customer_id,))

    customer_sales = cursor.fetchall()

    for customer_sale in customer_sales:
        sale_id = customer_sale[0]
        product_id = customer_sale[1]
        quantity = customer_sale[2]

        cursor.execute("""
            UPDATE products
            SET stock = stock + ?
            WHERE id = ?
        """, (quantity, product_id,))

        cursor.execute("""
            DELETE FROM sales
            WHERE id = ?
        """, (sale_id,))

    cursor.execute("""
        DELETE FROM customers
        WHERE id = ?
    """, (customer_id,))
    
    connection.commit()



def delete_product(cursor, connection):

    all_products(cursor)
    product_id = int(input("Produit à supprimer : "))

    cursor.execute("""
        SELECT
            id
        FROM sales
        WHERE product_id = ?
    """, (product_id,))

    sales_to_delete = cursor.fetchall()

    for sale_to_delete in sales_to_delete:
        sale_id = sale_to_delete[0]

        cursor.execute("""
            DELETE FROM sales
            WHERE id = ?
        """, (sale_id,))

    cursor.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))
    
    connection.commit()
