# Type	                                   Objectifs	                                        Nombre

# Découvertes	                 Toutes les recettes à 2, 3, 4, 5 et 6 ingrédients	                   5
# Fabrication	              Toutes les potions, tous les élixirs, tous les pentagrammes	           3
# Récolte	                       Tous les ingrédients possibles	                                   1
# Hauts faits	                                  cf plus bas	                                       5
# Total		                                                                                          14


from display.display_achievements import display_all_achievements
from display.display_utils import DIM, RESET
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
    
        choice = input(f"Objectif choisi {DIM}(Entrée pour revenir){RESET} : ")

        if not choice:
            return
    
        if choice.isdigit() and id_exists(cursor, "achievements", int(choice)):
            achievement_id = int(choice)
            break
    
        print("Choix invalide. Recommencer ou Entrée pour revenir.")
        return

    new_name = input(f"Nouveau nom {DIM}(Entrée pour revenir){RESET} : ")

    if not new_name.strip():
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
    
        choice = input(f"Objectif choisi {DIM}(Entrée pour revenir){RESET} : ")

        if not choice:
            return
    
        if choice.isdigit() and id_exists(cursor, "achievements", int(choice)):
            achievement_id = int(choice)
            break
    
        print("Choix invalide. Recommencer ou Entrée pour revenir.")
        return

    new_description = input(f"Nouvelle description (Entrée pour vide) {DIM}(q pour revenir){RESET} : ")
    
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

    name = input(f"Nom du haut fait {DIM}(Entrée pour revenir){RESET} : ")

    if not name:
        return

    category = input("Catégorie (victory/fun) : ").strip().lower()

    if category not in ("victory", "fun"):
        print("Catégorie invalide.")
        return

    display_all_achievements(cursor)

    parent = input(f"ID du parent (Entrée si aucun) {DIM}(q pour revenir){RESET} : ").strip()

    if parent:

        if parent == "q":
            return

        if not parent.isdigit() or not id_exists(cursor, "achievements", int(parent)):
            print("Parent invalide.")
            return

        parent_id = int(parent)

    else:
        parent_id = None

    description = input(f"Description (Entrée pour vide) {DIM}(q pour revenir){RESET} : ").strip() or None

    if description == "q":
        return

    cursor.execute("""
        INSERT INTO achievements (name, category, parent_id, description)
        VALUES (?, ?, ?, ?)
    """, (name, category, parent_id, description))

    connection.commit()

    print(f"Objectif ajouté ! ID : {cursor.lastrowid}")