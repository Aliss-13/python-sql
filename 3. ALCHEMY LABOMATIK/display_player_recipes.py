from display_recipe_ingredients_products_and_equipment import display_recipe_ingredients_products_and_equipments

def get_all_player_recipes_infos(cursor):

    cursor.execute("""
        SELECT
            recipes.id,
            recipes.name,
            recipes.description,
            recipe_types.name,
            recipe_rarity.color

        FROM recipes

        JOIN player_recipes
            ON player_recipes.recipe_id = recipes.id

        JOIN recipe_types
            ON recipe_types.id = recipes.type_id
        
        JOIN rarities AS recipe_rarity
            ON recipe_rarity.id = recipes.rarity_id

        ORDER BY recipe_types.id ASC, recipe_rarity.id ASC, recipes.id ASC
    """)

    return cursor.fetchall()




def get_all_player_recipes_ingredients(cursor):

    cursor.execute("""
        SELECT
            recipe_ingredients.recipe_id,
            recipes.name,
            recipe_types.name,
            ingredients.name,
            recipe_rarity.color,
            ingredient_rarity.color,
            recipe_ingredients.quantity

        FROM recipe_ingredients

        JOIN player_recipes
            ON player_recipes.recipe_id = recipe_ingredients.recipe_id

        JOIN recipes
            ON recipes.id = recipe_ingredients.recipe_id

        JOIN recipe_types
            ON recipe_types.id = recipes.type_id

        JOIN ingredients
            ON ingredients.id = recipe_ingredients.ingredient_id

        JOIN rarities AS recipe_rarity
            ON recipe_rarity.id = recipes.rarity_id

        JOIN rarities AS ingredient_rarity
            ON ingredient_rarity.id = ingredients.rarity_id

        ORDER BY recipe_types.id ASC, recipe_rarity.id ASC, recipe_ingredients.recipe_id ASC
    """)

    return cursor.fetchall()


def get_all_player_recipes_products(cursor):

    cursor.execute("""
        SELECT
            recipes.id,
            recipes.name,
            recipe_types.id,
            product_recipe.name,
            recipe_rarity.color,
            product_rarity.color,
            recipe_products.quantity

        FROM recipe_products

        JOIN player_recipes
            ON player_recipes.recipe_id = recipe_products.recipe_id

        JOIN recipes
            ON recipes.id = recipe_products.recipe_id

        JOIN recipe_types
            ON recipe_types.id = recipes.type_id

        LEFT JOIN recipes AS product_recipe
            ON product_recipe.id = recipe_products.product_recipe_id

        JOIN rarities AS recipe_rarity
            ON recipe_rarity.id = recipes.rarity_id

        LEFT JOIN rarities AS product_rarity
            ON product_rarity.id = product_recipe.rarity_id

        ORDER BY recipe_types.id ASC, recipe_rarity.id ASC, recipes.id ASC
    """)

    return cursor.fetchall()


def get_all_player_recipes_equipments(cursor):

    cursor.execute("""
        SELECT
            recipes.id,
            recipe_types.id,
            recipe_rarity.color,
            fire.name,
            melting_pot.name,
            container.name

        FROM recipes

        JOIN player_recipes
            ON player_recipes.recipe_id = recipes.id

        JOIN recipe_types
            ON recipe_types.id = recipes.type_id

        JOIN rarities AS recipe_rarity
            ON recipe_rarity.id = recipes.rarity_id

        LEFT JOIN equipment AS fire
            ON fire.id = recipes.fire_equipment_id

        LEFT JOIN equipment AS melting_pot
            ON melting_pot.id = recipes.melting_pot_equipment_id

        LEFT JOIN equipment AS container
            ON container.id = recipes.container_equipment_id

        ORDER BY recipe_types.id ASC, recipe_rarity.id ASC, recipes.id ASC
    """)

    return cursor.fetchall()


def return_all_player_recipes_ingredients_products_and_equipments(cursor):

    ingredients = get_all_player_recipes_ingredients(cursor)
    products = get_all_player_recipes_products(cursor)
    equipments = get_all_player_recipes_equipments(cursor)
    recipes_datas = get_all_player_recipes_infos(cursor)

    return ingredients, products, equipments, recipes_datas


#------------------------------------------------------------------------------------------------------------------------

def display_all_player_recipes_ingredients_products_and_equipments(cursor):

    ingredients, products, equipments, recipes_datas = \
        return_all_player_recipes_ingredients_products_and_equipments(cursor)

    return display_recipe_ingredients_products_and_equipments(
        ingredients,
        products,
        equipments,
        recipes_datas
    )