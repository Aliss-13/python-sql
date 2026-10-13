import random

from display.display_affinities_and_portals import display_all_affinities, display_harvest_portal

from utils import id_exists

from player_game.inventory import add_ingredient_to_inventory
from player_game.youtique import auto_sell
import player_game.game_state



def menu_portal(cursor, connection):

    while True:

        print("     🌀 Portails")
        print()

        display_all_affinities(cursor)

        print("[r] Retour")

        choix = input("> ")

        if choix.isdigit() and id_exists(cursor, "affinities", int(choix)):
            portal = int(choix)
            harvest_portal(cursor, connection, portal)

        elif choix == "r":
            return

        else:
            print("Choix invalide")


def harvest_portal(cursor, connection, portal):

    global game_tick

    discoveries = get_player_discoveries(cursor)

    cursor.execute("""
        SELECT 
            ingredient_affinities.ingredient_id,
            ingredient_affinities.affinity_id,
            ingredient_affinities.value,
            ingredients.rarity_id,
            rarities.weight,
            ingredients.unlock_discoveries
        FROM ingredient_affinities
        JOIN ingredients
            ON ingredients.id = ingredient_affinities.ingredient_id
        JOIN rarities
            ON rarities.id = ingredients.rarity_id
        WHERE ingredient_affinities.affinity_id = ?
        """, (portal,))
    
    portaff_ingredients = cursor.fetchall()

    portal_ingredients = []

    for ingredient_id, affinity_id, value, rarity_id, weight, unlock_discoveries in portaff_ingredients:
        if value >= 0.4 and unlock_discoveries <= discoveries:
            portal_ingredients.append((ingredient_id, affinity_id, value, rarity_id, weight))


    loots = []

    for _ in range(min(3, len(portal_ingredients))):
        result = random.choices(
            portal_ingredients,
            weights=[ingredient[4] for ingredient in portal_ingredients],
            k=1
        )[0]

        quantity = random.randint(1, 3)

        loots.append((result, quantity))

        portal_ingredients.remove(result)

    for result, quantity in loots:
        ingredient_id = result[0]
        
        display_harvest_portal(cursor, quantity, ingredient_id)

        add_ingredient_to_inventory(cursor, connection, ingredient_id, quantity)

        player_game.game_state.game_tick +=1
        auto_sell(cursor, connection, player_game.game_state.game_tick)


def get_player_discoveries(cursor):

    cursor.execute("""
        SELECT COUNT(*)
        FROM player_recipes
    """)

    return cursor.fetchone()[0]


def get_available_ingredients(cursor, discoveries):

    cursor.execute("""
        SELECT id, name
        FROM ingredients
        WHERE unlock_discoveries <= ?
    """, (discoveries,))

    return cursor.fetchall()