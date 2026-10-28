from display.display_utils import COLORS, RESET, DIM, YELLOW, CYAN, display_container_description
from utils import ask_positive_int

from player_game.game_functions.initialization import initialize_containers
from player_game.game_functions.advance_game_tick import advance_game_tick
from player_game.dialogues import FLAMELXPRESS_BANNERS

from data_management.discoveries import get_number_of_discoveries


import random


def flamel_xpress():
    print(f"🌐 {CYAN}FlamelXpress© = N°1 mondial de l'alchimie = {RESET}")
    print("   « Le prix et la qualité en instantané ! »*")
    print(f"{DIM}   *Voir conditions générales de transmutation.{RESET}")
    print()


def display_random_banner():
    banner = random.choice(FLAMELXPRESS_BANNERS)
    print(banner)


def get_available_containers(cursor):

    initialize_containers(cursor)

    discovery_count = get_number_of_discoveries(cursor)

    print(f"      {DIM}Nombre de découvertes : {discovery_count}{RESET}      ")

    cursor.execute("""
        SELECT
            equipment.id,
            equipment.name,
            equipment.description,
            rarities.color,
            containers.price,
            equipment.unlock_discoveries
        FROM containers

        JOIN equipment
            ON equipment.id = containers.equipment_id    

        JOIN rarities
            ON rarities.id = equipment.rarity_id
        
        JOIN equipment_categories
            ON equipment_categories.id = equipment.category_id
        
        WHERE equipment_categories.name = ?
            AND equipment.unlock_discoveries <= ?
            
        ORDER BY
            equipment.unlock_discoveries ASC,
            equipment.rarity_id ASC,
            containers.price ASC

    """, ("Contenant", discovery_count))

    available_containers = cursor.fetchall()

    print()
    for display_number, (equipment_id, name, description, container_color, price, unlock_discoveries) in enumerate(available_containers, start=1):
        
        color = COLORS[container_color]
        print(f'{display_number:<2} - {color}{name}{RESET} - Déblocage : {unlock_discoveries} découvertes - {YELLOW}{price} pièces.{RESET}')
        display_container_description(description)
        print()

    return available_containers


def buy_container(cursor, connection):

    available_containers = get_available_containers(cursor)

    while True:
    
        choice = input(f"Contenant à acheter {DIM}(Entrée pour revenir){RESET} : ")

        if not choice:
            return
    
        # Tu récupères le tuple correspondant à son choix
        if choice.isdigit() and 1 <= int(choice) <= len(available_containers):
            selected_container = available_containers[int(choice) - 1]
            break
        
        print("Choix invalide. Recommencer ou Entrée pour revenir.")
        

    # Tu extrais les deux informations nécessaires
    container_id = selected_container[0]
    price = selected_container[4]
        
    quantity = ask_positive_int("Quantité : ")

    cursor.execute("""SELECT money
    FROM player
    WHERE id = 1""")

    money = cursor.fetchone()[0]

    if price*quantity <= money:   


        try:
            cursor.execute("""
                UPDATE player
                SET money = money - ?
                WHERE id = ? AND money >= ?
            """, (price * quantity, 1, price * quantity))

            if cursor.rowcount != 1:
                raise ValueError("Fonds insuffisants.")

            cursor.execute("""
            SELECT equipment_id
            FROM container_inventory
            WHERE equipment_id = ?
            """, (container_id,))
            
            result = cursor.fetchone()

            
            if result is not None:
                cursor.execute("""
                UPDATE container_inventory
                SET quantity = quantity + ?
                WHERE equipment_id = ?
                """, (quantity, container_id))

            else:
                cursor.execute("""
                INSERT INTO container_inventory (equipment_id, quantity)
                VALUES (?, ?)
            """, (container_id, quantity))
                
            connection.commit()
           
        except Exception as error:
            connection.rollback()
            print(f"La transaction a échoué : {error}")
            return

        print(f"Vous achetez {COLORS[selected_container[3]]}{selected_container[1]}{RESET} x{quantity} !")

        advance_game_tick(cursor, connection)
        

    else:
        print("Pas assez d'argent.")
