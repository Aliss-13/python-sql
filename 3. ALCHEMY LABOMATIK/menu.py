from display.display_inventories import display_inventory, display_container_inventory, display_product_inventory, get_player_money
from display.display_player_equipment import display_all_player_equipments
from display.display_utils import DIM, RESET
from display.display_shop_inventory import display_shop_inventory

from player_game.portals import menu_portal
from player_game.blending import discover_recipe
from player_game.recipe_research import menu_unknown_recipes
from player_game.craft_recipe import craft_recipe
from player_game.craft_equipment import craft_equipment
from player_game.flamelxpress import buy_container, flamel_xpress, display_random_banner
from player_game.objectives import menu_objectives
from player_game.youtique import youtique, menu_transfer_products, display_shop_sales_report

from player_game.game_functions.advance_game_tick import advance_game_tick
from player_game.game_functions.reset_game import menu_reset_game

from menu_data import menu_database_management

def menu_laboratory(cursor, connection):

    while True:
    
        print()
        print("🧪 LABORATOIRE")
        print(f"[1] 🥣 Tenter un mélange {DIM}- Le mélange, c'est comme le mariage. Imprévisible et potentiellement explosif.{RESET}")
        print(f"[2] 📓 Carnet de laboratoire {DIM}- Liste les indices découverts sur chaque recette inconnue. Une enquête palpitante.{RESET}")
            
        print("[r] Retour")
    
        choix = input("> ")
        print()
    
        if choix == "1":
            print("      === Tenter un mélange ===")
            print()
            discover_recipe(cursor, connection)
            
        elif choix == "2":
            menu_unknown_recipes(cursor)
            
        elif choix == "r":
            return
    
        else:
            print("Choix invalide")

def menu(cursor, connection):

    while True:
        print()
        print("       = MENU =        ")
        print("")
        print(f'[1] 🌀 Portails {DIM}- Récolte des ingrédients.{RESET}')
        print(f"[2] 🧪 Laboratoire {DIM}- Découverte des recettes : expérimentation par le mélange des ingrédients, la souffrance et l'introspection.{RESET}")
        print(f'[3] 🧫 La Popotte {DIM}- Préparation des potions, élixirs et pentagrammes dont la recette est connue. Ne fonctionne pas pour le gasoil.{RESET}')
        print(f'[4] 🥽 La Fonderie {DIM}- Manufacture des instruments de mélange, feux et creusets. Magimix, Dolby Digital THX et Assurancetourix.{RESET}')
        print(f"[5] 🌐 FlamelXpress© {DIM}- Fournisseur incontournable des contenants alchimiques : contenants certifiés, prix transmutés !{RESET}")
        print(f"[6] 📓 Inventaire {DIM}- Ingrédients, contenants et produits fabriqués. Deuxième porte à droite.{RESET}")
        print(f"[7] ⚗️ Matériel d'alchimie {DIM}- Instruments de mélange, creusets et feux manufacturés. Dernière porte à gauche.{RESET}")
        print(f"[8] 🐍 La Youtique© {DIM}- Vente des potions, élixirs et pentagrammes concoctés : enrichissement personnel, statistiques et contrôle fiscal.{RESET}")
        print(f"[9] 📈 Objectifs {DIM}- On se voit au prochain copil ? Ah non c’est au coproj, autant pour moi ! Tu as bien prévenu les membres du codir ?{RESET}")
        print("")
        print(f"[q] 🔚 Quitter {DIM}- Je m'en vais comme un prince !{RESET}")
        print()
        print(f"[r] ♾️ Réinitialiser la partie {DIM}- Un choix radical.{RESET}")
        print("")

        choix = input("> ")
        print()

        if choix == "b":
            menu_database_management(cursor, connection)

        elif choix == "1":
            print("      === Récolte des ingrédients ===")
            print()
            menu_portal(cursor, connection)
        
        elif choix == "2":
            menu_laboratory(cursor, connection)
            advance_game_tick(cursor, connection)


        elif choix == "3":
            print("      === Fabriquer Potion, Élixir ou Pentagramme ===")
            print()
            craft_recipe(cursor, connection)

        elif choix == "4":
            print("      === Fabriquer matériel d'alchimie : Instruments de mélange, feux et creusets ===")
            print()
            craft_equipment(cursor, connection)

        elif choix == "5":
            flamel_xpress()
            display_random_banner()
            print()
            get_player_money(cursor)
            buy_container(cursor, connection) 

        elif choix == "6":
            print("      === Inventaire ===")
            print()
            get_player_money(cursor)
            display_inventory(cursor)
            display_container_inventory(cursor)
            display_product_inventory(cursor)
            print()

        elif choix == "7":
            print("      === Matériel ===")
            print()
            display_all_player_equipments(cursor)
            print()

        elif choix == "8":
            youtique()
            get_player_money(cursor)
            display_shop_inventory(cursor)
            display_shop_sales_report(cursor)
            menu_transfer_products(cursor, connection)

        elif choix == "9":
            menu_objectives(cursor)

        elif choix == "q":
            return

        elif choix == "r":
            menu_reset_game(cursor, connection)

        else:
            print("Choix invalide")

