from display import display_all_affinities, display_inventory, display_harvest_portal
from utils import id_exists
from inventory import add_to_inventory
import random


def menu_portal(cursor, connection, player_level):

    while True:

        print()
        print("🌀 Portails")

        display_all_affinities(cursor)

        print("[r] Retour")

        choix = input("> ")

        if choix.isdigit() and id_exists(cursor, "affinities", int(choix)):
            portal = int(choix)
            harvest_portal(cursor, connection, portal, player_level)
            
            display_inventory(cursor)

        elif choix == "r":
            return

        else:
            print("Choix invalide")


def harvest_portal(cursor, connection, portal, player_level):

    cursor.execute("""
        SELECT 
            ingredient_affinities.ingredient_id,
            ingredient_affinities.affinity_id,
            ingredient_affinities.value,
            ingredients.level,
            ingredients.rarity_id,
            rarities.weight
        FROM ingredient_affinities
        JOIN ingredients
            ON ingredients.id = ingredient_affinities.ingredient_id
        JOIN rarities
            ON rarities.id = ingredients.rarity_id
        WHERE ingredient_affinities.affinity_id = ?
        """, (portal,))
    
    portaff_ingredients = cursor.fetchall()

    portal_ingredients = []

    for ingredient_id, affinity_id, value, level, rarity_id, weight in portaff_ingredients:
        if value >= 0.4 and level <= player_level:
            portal_ingredients.append((ingredient_id, affinity_id, value, level, rarity_id, weight))


    loots = []

    for _ in range(min(3, len(portal_ingredients))):
        result = random.choices(
            portal_ingredients,
            weights=[ingredient[5] for ingredient in portal_ingredients],
            k=1
        )[0]

        quantity = random.randint(1, 3)

        loots.append((result, quantity))

        portal_ingredients.remove(result)

    for result, quantity in loots:
        ingredient_id = result[0]
        
    display_harvest_portal(cursor, quantity, ingredient_id)

    add_to_inventory(cursor, connection, ingredient_id, quantity)

