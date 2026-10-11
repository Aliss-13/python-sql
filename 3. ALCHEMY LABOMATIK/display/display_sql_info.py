def display_tables(cursor):
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tables = cursor.fetchall()

    for table in tables:
        print(table[0])


def display_tables_info(cursor):

    for table in ["rarities", "affinities", "equipment_categories", "targets", "recipe_types", "recipe_discovery_difficulty",
                  "ingredients", "equipment", "mixing_tools", "containers", "recipes", "recipe_discovery",
                  "ingredient_affinities", "equipment_craft", 
                  "player", "inventory", "product_inventory",
                  "recipe_ingredients", "recipe_products",
                  "container_inventory", "shop_inventory",
                  "player_equipment", "player_recipes", "sales_history"
                  ]:
        print(f"\n--- {table} ---")

        cursor.execute(f"PRAGMA table_info({table})")

        for column in cursor.fetchall():
            print(column)


def display_new_table_contents(cursor):
    print()
    print("=> Contenu de sales_history")
    cursor.execute("SELECT * FROM sales_history")
    print(cursor.fetchall())
    print()


def display_FK(cursor):
    print()
    print("=> Liste clés étrangères sales_history")
    cursor.execute("""
        PRAGMA foreign_key_list(sales_history)
    """)

    for row in cursor.fetchall():
        print(row)