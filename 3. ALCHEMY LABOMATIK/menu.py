from affinities import add_affinity_to_ingredient, reset_ingredient_affinities
from display import display_all_affinities, display_all_ingredients, display_inventory
from ingredients import add_ingredient, update_ingredient_menu



def menu(cursor, connection):

    while True:

        print()
        print("========== ALCHEMY LABOMATIK ==========")
        print("[1] Liste des ingrédients")
        print("[2] Ajouter un ingrédient")
        print("[3] Modifier un ingrédient") 
        print("[4] Liste des affinités")
        print("[5] Ajouter une ou plusieurs affinités à un ingrédient")
        print("[6] Supprimer les affinités d'un ingrédient")
        print("[7] Inventaire")
        
        print("[q] Quitter")

        choix = input("> ")

        if choix == "1":
            display_all_ingredients(cursor)

        elif choix == "2":
            add_ingredient(cursor, connection)

        elif choix == "3":
            update_ingredient_menu(cursor, connection)

        elif choix == "4":
            display_all_affinities(cursor)

        elif choix == "5":
            add_affinity_to_ingredient(cursor, connection)

        elif choix == "6":
            reset_ingredient_affinities(cursor, connection)

        elif choix == "7":
            display_inventory(cursor)

        elif choix == "q":
            return

        else:
            print("Choix invalide")