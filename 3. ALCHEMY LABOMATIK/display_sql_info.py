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

    for table in ["rarities", "affinities", "ingredients", "ingredient_affinities", "inventory", "product_inventory",
                  "container_inventory", "shop_inventory", "equipment", "equipment_categories", "equipment_craft", "mixing_tools", 
                  "player_equipment", "recipes", "recipe_types", "recipe_discovery", "player_recipes", "recipe_ingredients",
                  "recipe_products"]:
        print(f"\n--- {table} ---")

        cursor.execute(f"PRAGMA table_info({table})")

        for column in cursor.fetchall():
            print(column)


def display_new_table_contents(cursor):
    print()
    print("=> Contenu de container_inventory")
    cursor.execute("SELECT * FROM container_inventory")
    print(cursor.fetchall())
    print()


def display_FK(cursor):
    print()
    print("=> Liste clés étrangères recipe_products")
    cursor.execute("""
        PRAGMA foreign_key_list(recipe_products)
    """)

    for row in cursor.fetchall():
        print(row)