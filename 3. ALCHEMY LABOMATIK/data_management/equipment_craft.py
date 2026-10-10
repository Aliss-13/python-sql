from utils import ask_positive_int, id_exists, ask_int
from display.display_equipment_and_equipment_craft import display_all_equipment, display_all_equipment_crafts
from display.display_ingredients import display_all_ingredients


def add_equipment_craft(cursor, connection):

    display_all_equipment(cursor)

    equipment_id = ask_positive_int("Matériel (666 pour quitter) : ")

    if not id_exists(cursor, "equipment", equipment_id):
        print("Matériel introuvable.")
        return

    equipment_has_craft = False

    while True:

        display_all_ingredients(cursor)
        
        ingredient_id = ask_int("Ingrédients pour le craft (0 = terminer) : ")

        if ingredient_id == 0:
            if not equipment_has_craft:
                connection.rollback()
                print("Saisie annulée.")
                return
            break

        if not id_exists(cursor, "ingredients", ingredient_id):
            print("Ingrédient introuvable.")
            connection.rollback()
            return

        quantity = ask_positive_int("Quantité (666 pour quitter) : ")

        if quantity == "666":
            return

        cursor.execute("""
            INSERT INTO equipment_craft (equipment_id, ingredient_id, quantity)
            VALUES (?, ?, ?)
        """, (equipment_id, ingredient_id, quantity))

        equipment_has_craft = True

    connection.commit()


def reset_equipment_craft(cursor, connection):

    equipment_crafts = display_all_equipment_crafts(cursor)

    available_equipment = []
    
    for equipment in equipment_crafts:
        equipment_id = equipment[0]
    
        if equipment_id not in available_equipment:
            available_equipment.append(equipment_id)
    
    # choix du joueur  
    while True:
    
        choice = input("Craft équipement à réinitialiser (q pour revenir) : ") 
    
        if choice.lower() == "q":
            return
    
        # récupération de l'identifiant de l'équipement
    
        if choice.isdigit() and 1 <= int(choice) <= len(available_equipment):
            equipment_id = available_equipment[int(choice) - 1]
            break
    
        print("Choix invalide.")
    
    cursor.execute("""  
        DELETE FROM equipment_craft
        WHERE equipment_id = ?
    """, (equipment_id,))

    connection.commit()
    print("Matériaux nécessaires au craft de l'équipement supprimés.")