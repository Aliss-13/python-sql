from display.display_utils import YELLOW, RESET


def display_reset_game():

    print(f"      ⚠️  {YELLOW}RÉINITIALISATION DE LA PARTIE{RESET}")
    print()
    print("Cette action supprimera toute votre progression :")
    print("- ingrédients")
    print("- recettes découvertes")
    print("- équipements fabriqués")
    print("- produits")
    print("- ventes")
    print("- recherches du grimoire")
    print("- etc.")
    print()
    print("Votre argent sera réinitialisé à 100 pièces.")
    print()
    print(f"Pour confirmer, tapez {YELLOW}reset_game{RESET}")
    print()

def reset_game(cursor, connection):

    tables_to_reset = [
        "inventory",
        "player_equipment",
        "player_recipes",
        "shop_inventory",
        "sales_history",
        "container_inventory",
        "product_inventory", 
        "player_recipe_research",
        "player_achievements"
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

    cursor.execute("SELECT * FROM player_recipe_research")
    print("player_recipe_research :", cursor.fetchall())

    cursor.execute("SELECT * FROM player")
    print("player :", cursor.fetchall())

    cursor.execute("SELECT * FROM player_achievements")
    print("player_achievements :", cursor.fetchall())


def menu_reset_game(cursor, connection):

    while True:

        display_reset_game()

        choice = input("> ")
        print()

        if choice == "reset_game":
            reset_game(cursor, connection)
            test_reset_game(cursor)
            print()
            print ("Partie réinitialisée ✅")
            break

        else:
            print("Retour au menu ↩️")
            return 
    
    