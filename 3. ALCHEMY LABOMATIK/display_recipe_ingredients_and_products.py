from display_colors_and_rarities import COLORS, LIGHT_PINK, RESET, YELLOW
from display_refactor import format_recipe_and_craft_items, group_data_under_same_id


def get_all_recipes_ingredients(cursor):

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


def get_all_recipes_products(cursor):

    cursor.execute("""
        SELECT
            recipes.id,
            recipes.name,
            recipe_types.id,
            product_recipe.name,
            recipe_rarity.color,
            product_rarity.color,
            recipe_products.quantity
        FROM recipes

        JOIN recipe_types
            ON recipe_types.id = recipes.type_id

        LEFT JOIN recipe_products
            ON recipe_products.recipe_id = recipes.id

        LEFT JOIN recipes AS product_recipe
            ON product_recipe.id = recipe_products.product_recipe_id

        JOIN rarities AS recipe_rarity
            ON recipe_rarity.id = recipes.rarity_id

        LEFT JOIN rarities AS product_rarity
            ON product_rarity.id = product_recipe.rarity_id

        ORDER BY recipe_types.id ASC, recipe_rarity.id ASC, recipes.id ASC
    """)

    return cursor.fetchall()


def display_all_recipes_ingredients(cursor):

    result = get_all_recipes_ingredients(cursor)
    display_recipe_ingredients(result)
    return result


def display_all_recipes_products(cursor):

    result = get_all_recipes_products(cursor)
    display_recipe_product(result)
    return result


def return_recipe_ingredients_and_products(cursor):

    ingredients = get_all_recipes_ingredients(cursor)
    products = get_all_recipes_products(cursor)

    return ingredients, products


def display_recipe_ingredients_and_products(cursor):

    ingredients, products = return_recipe_ingredients_and_products(cursor)

    ingredient_groups = group_data_under_same_id(ingredients)
    product_groups = group_data_under_same_id(products)
    
    ingredients_by_recipe = {}
    products_by_recipe = {}

    for ingredient_group in ingredient_groups: # 1. construction du dictionnaire des ingrédients par recette

        ingredient_list = []
       
        for ingredient in ingredient_group:

            recipe_id = ingredient[0]

            ingredient_name = ingredient[3]
            ingredient_quantity = ingredient[6]
            ingredient_color = ingredient[5]
        
            if ingredient_name is not None:
                ingredient_list.append((ingredient_name, ingredient_quantity, ingredient_color))

        ingredients_by_recipe[recipe_id] = ingredient_list


    for product_group in product_groups: # 2. construction du dictionnaire des produits par recette

        product_list = []

        for product in product_group:

            recipe_id = product[0]
            
            product_name = product[3]
            product_quantity = product[6]
            product_color = product[5]

            if product_name is not None:
                product_list.append((product_name, product_quantity, product_color))

        products_by_recipe[recipe_id] = product_list

    for ingredient_group in ingredient_groups: # 3. affichage des recettes avec leurs ingrédients et produits

        ingredient = ingredient_group[0]  # On prend le premier élément du groupe pour obtenir les informations de la recette

        recipe_id = ingredient[0]
        recipe_name = ingredient[1]
        recipe_type = ingredient[2]
        recipe_color = ingredient[4]

        # récupération des ingrédients
        ingredient_list = ingredients_by_recipe.get(recipe_id, [])

        # récupération des produits
        product_list = products_by_recipe.get(recipe_id, [])

        # formatage pour l'affichage
        product_text = format_recipe_and_craft_items(product_list)
        ingredient_text = format_recipe_and_craft_items(ingredient_list)

          
        print(f'{recipe_id:>2} - {COLORS[recipe_color]}{recipe_name}{RESET} {YELLOW}[{recipe_type}]{RESET}')
        print(f'{LIGHT_PINK}     Ingrédients : {RESET}{ingredient_text}')
        print(f'{LIGHT_PINK}     Produits : {RESET}{product_text}')
        print()

#----------------------------------------------- RECIPE_PRODUCTS ----------------------------------------------------

def display_all_recipes_products(cursor):

    cursor.execute("""
    SELECT
        recipes.id,
        recipes.name,
        product_recipe.name,
        recipe_rarity.color,
        product_rarity.color,
        recipe_products.quantity
    FROM recipes
    LEFT JOIN recipe_products
        ON recipe_products.recipe_id = recipes.id
    LEFT JOIN recipes AS product_recipe
        ON product_recipe.id = recipe_products.product_recipe_id
    JOIN rarities AS recipe_rarity
        ON recipe_rarity.id = recipes.rarity_id
    LEFT JOIN rarities AS product_rarity
        ON product_rarity.id = product_recipe.rarity_id
    ORDER BY recipe_rarity.id ASC
    """)
   
    result = cursor.fetchall()
    display_recipe_product(result)
    return(result)


def display_recipe_product(recipe_products):
  
    groups = group_data_under_same_id(recipe_products)

    for group in groups:

        product_list = []

        for recipe_product in group:

            recipe_id = recipe_product[0]
            recipe_name = recipe_product[1]
            recipe_color = recipe_product[3]

            name = recipe_product[2]
            quantity = recipe_product[5]
            color = recipe_product[4]

            if name is not None:
                product_list.append((name, quantity, color))

        product_text = format_recipe_and_craft_items(product_list)
            
        print(
                f'{recipe_id} - '
                f'{COLORS[recipe_color]}{recipe_name}{RESET} - '
                f'{product_text}'
            )

#----------------------------------------------- RECIPE_INGREDIENTS ----------------------------------------------------

def display_all_recipes_ingredients(cursor):

    cursor.execute("""
    SELECT
        recipe_ingredients.recipe_id,
        recipes.name,
        ingredients.name,
        recipe_rarity.color,
        ingredient_rarity.color,
        recipe_ingredients.quantity
    FROM recipe_ingredients
    JOIN recipes
        ON recipes.id = recipe_ingredients.recipe_id
    JOIN ingredients
        ON ingredients.id = recipe_ingredients.ingredient_id
    JOIN rarities AS recipe_rarity
        ON recipe_rarity.id = recipes.rarity_id
    JOIN rarities AS ingredient_rarity
        ON ingredient_rarity.id = ingredients.rarity_id
    ORDER BY recipe_rarity.id ASC
    """)
   
    result = cursor.fetchall()
    display_recipe_ingredients(result)
    return(result)


def display_recipe_ingredients(recipe_ingredients):

    groups = group_data_under_same_id(recipe_ingredients)
   
    for group in groups:

        ingredient_list = []

        for recipe_ingredient in group:

            recipe_id = recipe_ingredient[0]
            recipe_name = recipe_ingredient[1]
            recipe_color = recipe_ingredient[3]
            ingredient_name = recipe_ingredient[2]
            ingredient_quantity = recipe_ingredient[5]
            ingredient_color = recipe_ingredient[4]
        
            if ingredient_name is not None:
                ingredient_list.append((ingredient_name, ingredient_quantity, ingredient_color))
        
        ingredient_text = format_recipe_and_craft_items(ingredient_list)

        print(
                f'{recipe_id} - {COLORS[recipe_color]}{recipe_name}{RESET} - '
                f'{ingredient_text}'
            )