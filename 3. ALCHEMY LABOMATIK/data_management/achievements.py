# Type	                                   Objectifs	                                        Nombre

# Découvertes	                 Toutes les recettes à 2, 3, 4, 5 et 6 ingrédients	                   5
# Fabrication	              Toutes les potions, tous les élixirs, tous les pentagrammes	           3
# Récolte	                       Tous les ingrédients possibles	                                   1
# Hauts faits	                                  cf plus bas	                                       5
# Total		                                                                                          14


from display.display_achievements import display_all_achievements
from utils import id_exists


commercial_descriptions = {
    12: "Avoir vendu tous les articles provoquant des troubles digestifs sévères.",
    13: "Avoir vendu un exemplaire de chaque article conduisant directement en cellule de dégrisement.",
    14: "Avoir vendu tous les articles en rapport avec une prise de branlée monumentale.",
    15: "Avoir vendu tous les articles remboursés par la Société d'Équilibration de la Cupelle.",
    16: "Avoir vendu tous les articles prédictifs d'une reconversion post-burnout en élevage caprin dans le Cantal."
}


def menu_update_achievement(cursor, connection):

    while True:
        print()
        print("--- Modifier objectif ---")
        print("[1] Nom")
        print("[2] Description")
        
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            update_achievement_name(cursor, connection)

        elif choix == "2":
            update_achievement_description(cursor, connection)

        elif choix == "r":
            return

        else:
            print("Choix invalide")


def update_achievement_name(cursor, connection):
            
    display_all_achievements(cursor)
    
    while True:
    
        choix = input("Objectif choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "achievements", int(choix)):
            achievement_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_name = input("Nouveau nom (q pour quitter) : ")

    if not new_name.strip():
        print("Le nom ne peut pas être vide.")
        return

    if new_name == "q": 
        return

    cursor.execute("""
        UPDATE achievements
        SET name = ?
        WHERE id = ?
        """, (new_name, achievement_id,))

    connection.commit()
    print("Nom mis à jour.")


def update_achievement_description(cursor, connection):
            
    display_all_achievements(cursor)
    
    while True:
    
        choix = input("Objectif choisi : ")
    
        if choix.isdigit() and id_exists(cursor, "achievements", int(choix)):
            achievement_id = int(choix)
            break
    
        print("Choix invalide.")
        return

    new_description = input("Nouvelle description (Entrée pour vide, q pour quitter) : ")
    
    if new_description == "q": 
        return

    if new_description == "": 
        new_description = None

    cursor.execute("""
        UPDATE achievements
        SET description = ?
        WHERE id = ?
        """, (new_description, achievement_id,))
    
    connection.commit()
    print("Description mise à jour.")



def add_achievement(cursor, connection):

    name = input("Nom du haut fait (q pour quitter) : ").strip()

    if name == "q":
        return

    if not name:
        print("Le nom ne peut pas être vide.")
        return

    category = input("Catégorie (victory/fun) : ").strip().lower()

    if category not in ("victory", "fun"):
        print("Catégorie invalide.")
        return

    display_all_achievements(cursor)

    parent = input("ID du parent (Entrée si aucun) : ").strip()

    if parent:

        if not parent.isdigit() or not id_exists(cursor, "achievements", int(parent)):
            print("Parent invalide.")
            return

        parent_id = int(parent)

    else:
        parent_id = None

    description = input("Description (Entrée si aucune, q pour quitter) : ").strip() or None

    if description == "q":
        return

    cursor.execute("""
        INSERT INTO achievements (name, category, parent_id, description)
        VALUES (?, ?, ?, ?)
    """, (name, category, parent_id, description))

    connection.commit()

    print(f"Objectif ajouté ! ID : {cursor.lastrowid}")