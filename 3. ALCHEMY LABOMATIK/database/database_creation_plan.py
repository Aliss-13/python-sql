def create_tables(cursor):

    
    # -------------- ORDRE DE CREATION DES TABLES ------------

    # 1.  rarities
    # 2.  affinities
    # 3.  equipment_categories
    # 4.  targets
    # 5.  recipe_types
    # 6.  recipe_discovery_difficulty

    # 7.  ingredients
    # 8.  equipment

    # 9.  mixing_tools
    # 10. containers

    # 11. recipes
    # 12. recipe_discovery

    # 13. ingredient_affinities
    # 14. equipment_craft

    # 15. inventory
    # 16. container_inventory
    # 17. product_inventory
    # 18. shop_inventory

    # 19. player_recipes
    # 20. player_equipment

    # 21. recipe_ingredients
    # 22. recipe_products


    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    #------------------------------------------ rarities ------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rarities (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        color TEXT NOT NULL,
        weight REAL NOT NULL
        
    )""")

    #------------------------------------------ affinities ----------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS affinities (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        icon TEXT

    )""")

    #------------------------------------------ equipment_categories -------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment_categories (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE

    )""")

    #------------------------------------------ targets --------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS targets (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE

    )""")

    #------------------------------------------ recipe_types ---------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipe_types (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE

    )""")

    #------------------------------------------ recipe_discovery_difficulty ------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipe_discovery_difficulty (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        number_of_affinities INTEGER NOT NULL

    )""")


    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬:◦●◦:▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    #------------------------------------------ ingredients ----------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        level INTEGER NOT NULL,
        rarity_id INTEGER NOT NULL,

        FOREIGN KEY (rarity_id) REFERENCES rarities(id)

    )""")

    #------------------------------------------ equipment --------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        category_id INTEGER,
        description TEXT,
        rarity_id INTEGER,
        unlock_discoveries INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY (category_id) REFERENCES equipment_categories(id),
        FOREIGN KEY (rarity_id) REFERENCES rarities(id)

    )""")


    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬:◦●◦:▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    #------------------------------------------ mixing_tools --------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mixing_tools (

        equipment_id INTEGER PRIMARY KEY,
        capacity INTEGER NOT NULL,

        FOREIGN KEY (equipment_id) REFERENCES equipment(id)

    )""")


    #------------------------------------------ containers ----------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS containers (

        equipment_id INTEGER PRIMARY KEY,
        price INTEGER NOT NULL
            CHECK (price >= 0),

        FOREIGN KEY (equipment_id) REFERENCES equipment(id)
    )""")


    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬:◦●◦:▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    #------------------------------------------ recipes --------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (

        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        type_id INTEGER NOT NULL,
        target_id INTEGER NOT NULL,
        description TEXT,
        effect TEXT,
        rarity_id INTEGER,
        discovery_difficulty_id INTEGER,
        fire_equipment_id INTEGER,
        melting_pot_equipment_id INTEGER,
        container_equipment_id INTEGER,

        FOREIGN KEY (type_id) REFERENCES recipe_types(id),
        FOREIGN KEY (target_id) REFERENCES targets(id),
        FOREIGN KEY (rarity_id) REFERENCES rarities(id),
        FOREIGN KEY (discovery_difficulty_id) REFERENCES recipe_discovery_difficulty(id),
        FOREIGN KEY (fire_equipment_id) REFERENCES equipment(id),
        FOREIGN KEY (melting_pot_equipment_id) REFERENCES equipment(id),
        FOREIGN KEY (container_equipment_id) REFERENCES equipment(id)

    )""")

    #------------------------------------------ recipe_discovery -----------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipe_discovery (

        recipe_id INTEGER,
        number_of_ingredients INTEGER NOT NULL,
        affinity_id INTEGER,
        value REAL,

        PRIMARY KEY (recipe_id, affinity_id),

        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
        FOREIGN KEY (affinity_id) REFERENCES affinities(id)

    )""")


    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬:◦●◦:▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    #------------------------------------------ ingredient_affinities -----------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredient_affinities (

        ingredient_id INTEGER,
        affinity_id INTEGER,
        value REAL NOT NULL,

        PRIMARY KEY (ingredient_id, affinity_id),

        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
        FOREIGN KEY (affinity_id) REFERENCES affinities(id)

    )""")

    #------------------------------------------ equipment_craft -------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment_craft (

        equipment_id INTEGER,
        ingredient_id INTEGER,
        quantity INTEGER NOT NULL,

        PRIMARY KEY (equipment_id, ingredient_id),

        FOREIGN KEY (equipment_id) REFERENCES equipment(id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)

    )""")

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬:◦●◦:▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    
    #------------------------------------------ player --------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player (

        id INTEGER PRIMARY KEY CHECK (id = 1),
        money INTEGER NOT NULL DEFAULT 100
            CHECK (money >= 0)

    )""")

    #------------------------------------------ inventory -----------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (

        ingredient_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)

    )""")

    #------------------------------------------ container_inventory --------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS container_inventory (

        equipment_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY (equipment_id) REFERENCES equipment(id)

    )""")

    #------------------------------------------ product_inventory ----------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_inventory (

        recipe_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY (recipe_id) REFERENCES recipes(id)

    )""")

    #------------------------------------------ shop_inventory -------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shop_inventory (

        recipe_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY (recipe_id) REFERENCES recipes(id)

    )""")


    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬:◦●◦:▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    #------------------------------------------ player_recipes ------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_recipes (

        recipe_id INTEGER PRIMARY KEY,
        crafted INTEGER NOT NULL DEFAULT 0
            CHECK (crafted IN (0, 1)),

        FOREIGN KEY (recipe_id) REFERENCES recipes(id)

    )""")

    #------------------------------------------ player_equipment ----------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_equipment (

        equipment_id INTEGER PRIMARY KEY,
        crafted INTEGER NOT NULL DEFAULT 0 CHECK (crafted IN (0, 1)),

        FOREIGN KEY (equipment_id) REFERENCES equipment(id)

    )""")


    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬:◦●◦:▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    #------------------------------------------ recipe_ingredients --------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipe_ingredients (

        recipe_id INTEGER,
        ingredient_id INTEGER,
        quantity INTEGER,

        PRIMARY KEY (recipe_id, ingredient_id),

        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)

    )""")

    #------------------------------------------ recipe_products ------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipe_products (

        recipe_id INTEGER NOT NULL,
        product_recipe_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,

        PRIMARY KEY (recipe_id, product_recipe_id),

        FOREIGN KEY (recipe_id)
            REFERENCES recipes(id),

        FOREIGN KEY (product_recipe_id)
            REFERENCES recipes(id)

    )""")

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬