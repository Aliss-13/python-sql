from display.display_sql_info import display_tables_info, display_tables, display_new_table_contents, display_FK
from display.display_recipe_ingredients_products_and_equipment import display_all_recipes_ingredients_products_and_equipments
from display.display_equipment_and_equipment_craft import display_all_equipment_crafts, display_all_equipment
from display.display_recipes import display_all_recipes
from display.display_affinities_and_portals import display_all_affinities
from display.display_discoveries import display_all_discoveries
from display.display_ingredients import display_all_ingredients


from data_management.equipment_craft import add_equipment_craft, reset_equipment_craft
from data_management.recipes import add_recipe, menu_update_recipe, add_recipe_ingredients, add_recipe_products, reset_recipe_ingredients, reset_recipe_products
from data_management.discoveries import add_recipe_discovery, menu_update_discovery
from data_management.affinities import add_affinity_to_ingredient
from data_management.ingredients import reset_ingredient_affinities, add_ingredient, menu_update_ingredient
from data_management.equipment import add_equipment, menu_update_equipment
from data_management.achievements import menu_update_achievement, display_all_achievements, add_achievement



def menu_database_management(cursor, connection):

    while True:
        print("")
        print("       = MENU GESTION BASE DE DONNÉES =        ")
        print("Mets le souk dedans, je te démonte. Bisous ❤️.")
        print("")
        print("[1] 🫧 Ingrédients") 
        print("[2] 🧬 Affinités")
        print("[3] ⚗️ Matériel")
        print("[4] 📜 Recettes")
        print("[5] 💡 Découvertes")
        print("[6] 🏆 Objectifs")
        print("[7] 🪑 Tables")
        print("")
        print("[r] 🔚 Retour")
        print("")

        choix = input("> ")
        print()

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
            menu_achievements(cursor, connection)

        elif choix == "7":
            print("======= SQL database info =======")
            print()
            display_tables(cursor)
            display_tables_info(cursor)
            display_new_table_contents(cursor)
            display_FK(cursor)
            print("=================================")

        elif choix == "r":
            return
        
        else:
            print("Choix invalide")


def menu_achievements(cursor, connection):

    while True:
    
        print()
        print("🏆 OBJECTIFS JOUEUR")
        print("[1] Liste objectifs")
        print("[2] Ajouter objectif")
        print("[3] Modifier objectif")
            
        print("[r] Retour")
    
        choix = input("> ")
        print()
    
        if choix == "1":
            display_all_achievements(cursor)
            
        elif choix == "2":
            add_achievement(cursor, connection)
            
        elif choix == "3":
            menu_update_achievement(cursor, connection)

        elif choix == "r":
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
        print()
    
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
        print()
        print("[1] Liste recettes")
        print("[2] Ajouter recette")
        print("[3] Modifier recette")
        print()
        print("[4] Afficher les ingrédients et produits d'une recette")
        print("[5] Ajouter ingrédients à une recette")
        print("[6] Ajouter produits à une recette")
        print("[7] Réinitialiser ingrédients d'une recette")
        print("[8] Réinitialiser produits d'une recette")
            
        print("[r] Retour")
    
        choix = input("> ")
        print()
    
        if choix == "1":
            display_all_recipes(cursor)
            
        elif choix == "2":
            add_recipe(cursor, connection)
            
        elif choix == "3":
            menu_update_recipe(cursor, connection)

        elif choix == "4":
            display_all_recipes_ingredients_products_and_equipments(cursor)

        elif choix == "5":
            add_recipe_ingredients(cursor, connection)

        elif choix == "6":
            add_recipe_products(cursor, connection)

        elif choix == "7":
            reset_recipe_ingredients(cursor, connection)

        elif choix == "8":
            reset_recipe_products(cursor, connection)

        elif choix == "r":
            return
    
        else:
            print("Choix invalide")



def menu_ingredients(cursor, connection):

    while True:
    
            print()
            print("🫧 INGRÉDIENTS")
            print("[1] Liste ingrédients")
            print("[2] Ajouter ingrédient")
            print("[3] Modifier ingrédient") 
            
            print("[r] Retour")
    
            choix = input("> ")
            print()
    
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
        print()
    
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
        print()
    
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