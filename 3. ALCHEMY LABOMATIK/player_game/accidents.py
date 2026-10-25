import random

import player_game.game_functions.game_state as game_state

from display.display_utils import YELLOW, RESET, CYAN, COLORS
from player_game.inventory import add_ingredient_to_inventory
from player_game.recipe_research import group_by_number_of_ingredients, get_unknown_recipes, get_max_capacity

from player_game.dialogues import ADVERTISING_INTERFERENCE, ASTRAL_GOSSIP, DIMENSIONAL_COMIC, CATASTROPHIC_ADVISOR
from player_game.dialogues import SANITARY_INSPECTION, TAX_AUDIT, random_dialogue


def trigger_blending_accident(cursor, blending_ingredients):

    accidents = [
        advertising_interference,
        lambda: crackling_explosion(cursor),
        lambda: transformation_of_matter(cursor, blending_ingredients),
        lambda: gemino_gemini(cursor, blending_ingredients),
        lambda: surprise_preparation(cursor),
        hes_alive,
        taxes_and_fuckeries
    ]

    if game_state.active_event is not None:
        return
    
    print()
    print("⚠️ ACCIDENT ALCHIMIQUE ⚠️")
    print()

    random.choice(accidents)()

#------------------------------------------- Gestion temporalité des évènements textuels --------------------------------------------------
#                                                    advertising_interference
#                                                       taxes_and_fuckeries
#                                                             hes_alive

def start_temporary_event(dialogue_function, end_message):

    if game_state.active_event is not None:
        return False

    game_state.active_event = dialogue_function
    game_state.event_start_tick = game_state.game_tick
    game_state.last_event_tick = game_state.game_tick
    game_state.event_end_message = end_message

    print(dialogue_function())
    return True


def tick_temporary_event():

    EVENT_DURATION = 12
    EVENT_INTERVAL = 3

    if game_state.active_event is None:
        return

    elapsed = game_state.game_tick - game_state.event_start_tick

    if elapsed >= EVENT_DURATION:
        print(game_state.event_end_message)

        game_state.active_event = None
        game_state.event_start_tick = None
        game_state.last_event_tick = None
        game_state.event_end_message = None
        return

    if game_state.game_tick - game_state.last_event_tick >= EVENT_INTERVAL:
        print(game_state.active_event())
        game_state.last_event_tick = game_state.game_tick

#------------------------------------------------- Interférence publicitaire --------------------------------------------------------------

def advertising_interference():

    advertising = lambda: random_dialogue(ADVERTISING_INTERFERENCE, "advertising")

    print("📡 INTERFÉRENCE PUBLICITAIRE ARCANIQUE DÉTECTÉE !")
    print("Une fréquence commerciale parasite votre laboratoire...")
    print()
    start_temporary_event(advertising, "✨ Le signal publicitaire arcanique s'est dissipé.")

#------------------------------------------------- Il est vivant ! --------------------------------------------------------------

def hes_alive():

    print("🐙 IL EST VIVANT !")
    print("Oh, mais il parle...")
    print()

    companions = {
    "La Commère astrale": (ASTRAL_GOSSIP, "astral_gossip"),
    "Le Conseiller catastrophique": (CATASTROPHIC_ADVISOR, "catastrophic_advisor"),
    "Le Bouffon dimensionnel": (DIMENSIONAL_COMIC, "dimensional_comic")
    }

    name, (dialogues, category) = random.choice(list(companions.items()))

    dialogue = lambda: random_dialogue(dialogues, category)

    print(f"✨ Vous avez invoqué {YELLOW}{name}{RESET} !")
    print()
    start_temporary_event(dialogue, f"✨ {name} disparaît... Ouf.")

#------------------------------------------------------ Taxes et emmerdes ----------------------------------------------è---------------------

def taxes_and_fuckeries():

    print("📋 Taxes et emmerdes !")
    print("Sens mon doigt.")
    print()

    fuckeries = {
    "Hermine Pingelig, Inspectrice sanitaire de l'ASEPM": (SANITARY_INSPECTION, "hermine_pingelig"),
    "Lucien Cheval, Contrôleur fiscal de la DDDP": (TAX_AUDIT, "lucien_cheval")
    }

    name, (dialogues, category) = random.choice(list(fuckeries.items()))

    dialogue = lambda: random_dialogue(dialogues, category)
    
    print(f"✨ Vous avez rameuté {CYAN}{name}{RESET} !")
    print()
    start_temporary_event(dialogue, f"✨ {name} part, l'air très satisfait. Pfiou... Vous vous demandez s'il vous reste du Transmut-o-Plomb...")

#------------------------------------------------- Explosion pétaradante --------------------------------------------------------------

def crackling_explosion(cursor):

    print("💥 Explosion pétaradante !")

    cursor.execute("""
        SELECT
            ingredients.id,
            ingredients.name,
            rarities.color,
            inventory.quantity
        FROM inventory
        JOIN ingredients
            ON ingredients.id = inventory.ingredient_id
        JOIN rarities
            ON rarities.id = ingredients.rarity_id
        WHERE inventory.quantity > 2
    """)

    ingredients = cursor.fetchall()
    
    if not ingredients:
        return
    
    number_to_lose = min(random.randint(1, 3), len(ingredients))
    picked_ingredients = random.sample(ingredients, k=number_to_lose)

    messages = []

    for ingredient_id, ingredient_name, ingredient_color, available_quantity in picked_ingredients:
    
        lost_quantity = random.randint(1, 3)
    
        cursor.execute("""
        UPDATE inventory
        SET quantity = quantity - ?
        WHERE ingredient_id = ?
            AND quantity >= ?
        """, (lost_quantity, ingredient_id, lost_quantity))
      
        if cursor.rowcount != 1:   # Aucune ligne modifiée ou modification inattendue.
            raise RuntimeError("Impossible de retirer les ingrédients pendant l'explosion.")
        
        messages.append(f"Vous perdez {COLORS[ingredient_color]}{ingredient_name}{RESET} x{lost_quantity} !")

    for message in messages:
        print(message)

#------------------------------------------------- Transformation de matière --------------------------------------------------------------

def transformation_of_matter(cursor, blending_ingredients):

    print("🦠 Transformation de matière...")

    cursor.execute("""
    SELECT
        ingredients.id,
        ingredients.name,
        rarities.color
    FROM inventory
    JOIN ingredients
        ON ingredients.id = inventory.ingredient_id
    JOIN rarities
        ON rarities.id = ingredients.rarity_id
    """)

    ingredients = cursor.fetchall()
    
    if not ingredients:
        return
    
    number_to_gain = min(len(blending_ingredients), len(ingredients))
    picked_ingredients = random.sample(ingredients, k=number_to_gain)

    for ingredient_id, ingredient_name, ingredient_color in picked_ingredients:

        quantity = random.randint(1, 3)

        add_ingredient_to_inventory(cursor, ingredient_id, quantity)

        print(f"Vous récoltez {COLORS[ingredient_color]}{ingredient_name}{RESET} x{quantity} !")

#------------------------------------------------------ Réaction instable ------------------------------------------------------------------

def surprise_preparation(cursor):

    print("🧪 Vous obtenez une préparation impeccable ! Comment ça se fait ? Ca ne vous ressemble pas... ")

    unknown_recipes = get_unknown_recipes(cursor)
    _, number_groups = group_by_number_of_ingredients(unknown_recipes)
    capacity = get_max_capacity(cursor)

    possible_recipes = []

    for number, recipes in number_groups.items():
        if number <= capacity:
            possible_recipes.extend(recipes)

    # Pourquoi extend() plutôt que append() ?
    #   - append(recipes) ajouterait une liste entière comme un seul élément.
    #   - extend(recipes) ajoute individuellement toutes les recettes de ce groupe.

    if not possible_recipes:
        print("Aucune préparation compatible avec votre équipement.")
        return

    picked_recipe = random.choice(possible_recipes)

    # (recipe_name, recipe_type, recipe_color, number_of_ingredients, difficulty_id, number_of_affinities, signature) = recipe_data
    # vient de get_discovery_affinity_signature (module blending)

    picked_recipe_id, recipe_data = picked_recipe
    picked_recipe_name = recipe_data[0]
    picked_recipe_color = recipe_data[2]

    cursor.execute("""
        SELECT 
            product_inventory.recipe_id, 
            recipes.name, 
            rarities.color
        FROM product_inventory

        JOIN recipes
            ON recipes.id = product_inventory.recipe_id
        
        JOIN rarities
            ON rarities.id = recipes.rarity_id

    """)
    
    product_inventory_recipes = cursor.fetchall()
    
    product_inventory_recipe_ids = []

    for product_inventory_recipe in product_inventory_recipes:
        product_inventory_recipe_ids.append(product_inventory_recipe[0])
        

    if picked_recipe_id not in product_inventory_recipe_ids:
    
        cursor.execute("""
            INSERT INTO product_inventory (recipe_id, quantity)
            VALUES (?, ?)
        """, (picked_recipe_id, 1))
    
    else:
        cursor.execute("""
            UPDATE product_inventory
            SET quantity = quantity + ?
            WHERE recipe_id = ?
        """, (1, picked_recipe_id))

    print(f"Vous fabriquez {COLORS[picked_recipe_color]}{picked_recipe_name}{RESET} !")

#------------------------------------------------------- Gemino Gemini ---------------------------------------------------------------------

def gemino_gemini(cursor, blending_ingredients):

    print("🧑‍🤝‍🧑 Gemino-Gemini 🎶 Un nous étions, plusieurs nous devenons 🎶 ")

    for ingredient_id in set(blending_ingredients):

        cursor.execute(""" 
            SELECT 
                ingredients.id, 
                ingredients.name, 
                rarities.color 
            FROM ingredients
            JOIN rarities
                ON rarities.id = ingredients.rarity_id
            WHERE ingredients.id = ?
            """, (ingredient_id,))
        

        ingredient = cursor.fetchone()

        if ingredient is None:
            continue

        ingredient_name = ingredient[1]
        ingredient_color = ingredient[2]

        quantity = random.randint(1, 3)
        add_ingredient_to_inventory(cursor, ingredient_id, quantity)
        print(f"Vous récoltez {COLORS[ingredient_color]}{ingredient_name}{RESET} x{quantity} !")