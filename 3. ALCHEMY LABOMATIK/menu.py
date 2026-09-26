from affinities import add_affinity_to_ingredient

from display import display_all_affinities, display_all_ingredients, display_inventory, display_all_equipment
from display import display_all_equipment_crafts, display_all_recipes, display_all_discoveries

from ingredients import add_ingredient, menu_update_ingredient, reset_ingredient_affinities
from portals import menu_portal
from equipment import add_equipment, menu_update_equipment, add_equipment_craft, reset_equipment_craft
from blending import join_corresponding_recipe_to_blend
from recipes import add_recipe, menu_update_recipe
from discoveries import add_recipe_discovery, menu_update_discovery, discover_recipe



def menu(cursor, connection, player_level):

    while True:

        print("──────── Menu ────────")
        print("[1] 🫟 Ingrédients") 
        print("[2] 🧬 Affinités")
        print("[3] ⚗️ Matériel")
        print("[4] 📜 Recettes")
        print("[5] 💡 Découvertes")
        print()
        print("[6] 📓 Inventaire")
        print("[7] 🌀 Portails")
        print("[8] 🧫 Mélanger")
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
            menu_discoveries(cursor, connection)

        elif choix == "6":
            display_inventory(cursor)
            print()

        elif choix == "7":
            menu_portal(cursor, connection, player_level)

        elif choix == "8":
            recipe_id = join_corresponding_recipe_to_blend(cursor)

            if recipe_id is not None:
                discover_recipe(cursor, connection, recipe_id)

        elif choix == "q":
            return

        else:
            print("Choix invalide")


def menu_discoveries(cursor, connection):

    while True:
    
        print()
        print("💡 DÉCOUVERTES")
        print("[1] Liste découvertes")
        print("[2] Ajouter découverte")
        print("[3] Modifier découverte")
            
        print("[r] Retour")
    
        choix = input("> ")
    
        if choix == "1":
            display_all_discoveries(cursor)
            
        elif choix == "2":
            add_recipe_discovery(cursor, connection)
            
        elif choix == "3":
            menu_update_discovery(cursor, connection)

        elif choix == "r":
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
        print("[4] Afficher ingrédients pour craft matériel")
        print("[5] Ajouter ingrédients pour craft matériel")
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
            display_all_equipment_crafts(cursor)

        elif choix == "5":
            add_equipment_craft(cursor, connection)

        elif choix == "6":
            reset_equipment_craft(cursor, connection)
    
        elif choix == "r":
            return
    
        else:
            print("Choix invalide")