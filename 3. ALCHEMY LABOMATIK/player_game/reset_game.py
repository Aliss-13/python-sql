def reset_game(cursor, connection):

    tables_to_reset = [
        "inventory",
        "player_equipment",
        "player_recipes",
        "shop_inventory",
        "sales_history",
        "container_inventory",
        "product_inventory"
    ]

    for table in tables_to_reset:
        cursor.execute(f"DELETE FROM {table}")

    cursor.execute("""
        UPDATE player
        SET money = 100
    """)

    connection.commit()


def test_reset_game(cursor):
    
    cursor.execute("SELECT * FROM inventory")
    print("inventory :", cursor.fetchall())

    cursor.execute("SELECT * FROM container_inventory")
    print("container_inventory :", cursor.fetchall())

    cursor.execute("SELECT * FROM player_equipment")
    print("player_equipment :", cursor.fetchall())

    cursor.execute("SELECT * FROM player_recipes")
    print("player_recipes :", cursor.fetchall())

    cursor.execute("SELECT * FROM product_inventory")
    print("product_inventory :", cursor.fetchall())

    cursor.execute("SELECT * FROM shop_inventory")
    print("shop_inventory :", cursor.fetchall())

    cursor.execute("SELECT * FROM sales_history")
    print("sales_history :", cursor.fetchall())

    cursor.execute("SELECT * FROM player")
    print("player :", cursor.fetchall())