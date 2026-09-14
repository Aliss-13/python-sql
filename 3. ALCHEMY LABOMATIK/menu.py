from affinities import add_affinity_to_ingredient, reset_ingredient_affinities
from display import display_all_affinities, display_all_ingredients, display_inventory, display_all_equipment
from ingredients import add_ingredient, menu_update_ingredient
from portals import menu_portal
from equipment import add_equipment, menu_update_equipment



def menu(cursor, connection, player_level):

    while True:

        print("──────── Menu ────────")
        print("[1] 🫟 Ingrédients") 
        print("[2] 🧬 Affinités")
        print("[3] ⚗️ Matériel")
        print("[4] 📓 Inventaire")
        print("[5] 🌀 Portails")
        
        print("[q] 🔚 Quitter")

        choix = input("> ")

        if choix == "1":
            menu_ingredients(cursor, connection)

        elif choix == "2":
            menu_affinities(cursor, connection)

        elif choix == "3":
            menu_equipment(cursor, connection)

        elif choix == "4":
            display_inventory(cursor)
            print()

        elif choix == "5":
            menu_portal(cursor, connection, player_level)

        elif choix == "q":
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
            
        print("[r] Retour")
    
        choix = input("> ")
    
        if choix == "1":
            display_all_equipment(cursor)
            
        elif choix == "2":
            add_equipment(cursor, connection)
            
        elif choix == "3":
            menu_update_equipment(cursor, connection)
    
        elif choix == "r":
            return
    
        else:
            print("Choix invalide")