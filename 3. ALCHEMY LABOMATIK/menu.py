from affinities import add_affinity_to_ingredient, reset_ingredient_affinities

from display import display_all_affinities, display_all_ingredients, display_inventory, display_all_equipment
from display import display_all_equipment_crafts, display_all_recipes

from ingredients import add_ingredient, menu_update_ingredient
from portals import menu_portal
from equipment import add_equipment, menu_update_equipment, add_equipment_craft, reset_equipment_craft
from blending import blending_list
from recipes import add_recipe, menu_update_recipe



def menu(cursor, connection, player_level):

    while True:

        print("──────── Menu ────────")
        print("[1] 🫟 Ingrédients") 
        print("[2] 🧬 Affinités")
        print("[3] ⚗️ Matériel")
        print("[4] 📜 Recettes")
        print()
        print("[5] 📓 Inventaire")
        print("[6] 🌀 Portails")
        print("[7] 🧫 Mélanger")
        print()
        print("[q] 🔚 Quitter")

        choix = input("> ")

        if choix == "1":
            menu_ingredients(cursor, connection)

        elif choix == "2":
            menu_affinities(cursor, connection)

        elif choix == "3":
            menu_equipment(cursor, connection)

        elif choix == "4":
            menu_recipes(cursor, connection)

        elif choix == "5":
            display_inventory(cursor)
            print()

        elif choix == "6":
            menu_portal(cursor, connection, player_level)

        elif choix == "7":
            blending_list(cursor)

        elif choix == "q":
            return

        else:
            print("Choix invalide")


def menu_recipes(cursor, connection):

    while True:
    
        print()
        print("📜 RECETTES")
        print("[1] Liste recettes")
        print("[2] Ajouter recette")
        print("[3] Modifier recette")
            
        print("[r] Retour")
    
        choix = input("> ")
    
        if choix == "1":
            display_all_recipes(cursor)
            
        elif choix == "2":
            add_recipe(cursor, connection)
            
        elif choix == "3":
            menu_update_recipe(cursor, connection)

        elif choix == "r":
            return
    
        else:
            print("Choix invalide")



def menu_ingredients(cursor, connection):

    while True:
    
            print()
            print("🫟 INGRÉDIENTS")
            print("[1] Liste ingrédients")
            print("[2] Ajouter ingrédient")
            print("[3] Modifier ingrédient") 
            
            print("[r] Retour")
    
            choix = input("> ")
    
            if choix == "1":
                display_all_ingredients(cursor)
    
            elif choix == "2":
                add_ingredient(cursor, connection)
    
            elif choix == "3":
                menu_update_ingredient(cursor, connection)
    
            elif choix == "r":
                return
    
            else:
                print("Choix invalide")


def menu_affinities(cursor, connection):

    while True:
    
        print()
        print("🧬 AFFINITÉS")
        print("[1] Liste affinités")
        print("[2] Ajouter affinité(s) à un ingrédient")
        print("[3] Supprimer les affinités d'un ingrédient")
            
        print("[r] Retour")
    
        choix = input("> ")
    
        if choix == "1":
            display_all_affinities(cursor)
            
        elif choix == "2":
            add_affinity_to_ingredient(cursor, connection)
            
        elif choix == "3":
            reset_ingredient_affinities(cursor, connection)
    
        elif choix == "r":
            return
    
        else:
            print("Choix invalide")


def menu_equipment(cursor, connection):

    while True:
    
        print()
        print("⚗️ MATÉRIEL")
        print("[1] Liste matériel")
        print("[2] Ajouter matériel")
        print("[3] Modifier matériel")
        print("[4] Ajouter ingrédients pour craft matériel")
        print("[5] Afficher ingrédients pour craft matériel")
        print("[6] Supprimer ingrédients pour craft matériel")
            
        print("[r] Retour")
    
        choix = input("> ")
    
        if choix == "1":
            display_all_equipment(cursor)
            
        elif choix == "2":
            add_equipment(cursor, connection)
            
        elif choix == "3":
            menu_update_equipment(cursor, connection)

        elif choix == "4":
            add_equipment_craft(cursor, connection)

        elif choix == "5":
            display_all_equipment_crafts(cursor)

        elif choix == "6":
            reset_equipment_craft(cursor, connection)
    
        elif choix == "r":
            return
    
        else:
            print("Choix invalide")