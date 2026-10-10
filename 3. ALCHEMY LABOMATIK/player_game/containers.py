from display.display_utils import COLORS, RESET, DIM, YELLOW
from player_game.initialization import initialize_containers
from utils import ask_positive_int

def get_available_containers(cursor, connection):

    initialize_containers(cursor, connection)

    cursor.execute("""
        SELECT COUNT(*)
        FROM player_recipes
    """)
    discovery_count = cursor.fetchone()[0]
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
        print(f'{display_number} - {color}{name}{RESET} - {YELLOW}{price} pièces.{RESET}')
        print(f'    Déblocage : {unlock_discoveries} découvertes - {DIM}{description}{RESET}')
        print()

    return available_containers


def buy_container(cursor, connection):

    available_containers = get_available_containers(cursor, connection)

    while True:
    
        choice = input("Contenant à acheter : ") 
    
        # Tu récupères le tuple correspondant à son choix
        if choice.isdigit() and 1 <= int(choice) <= len(available_containers):
            selected_container = available_containers[int(choice) - 1]
            break
        
        print("Choix invalide.")
        

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
            WHERE id = ?
            """, (price*quantity, 1))


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

        print(f"Vous achetez {COLORS[selected_container[3]]}{selected_container[1]}{RESET} x{quantity} !")
        

    else:
        print("Pas assez d'argent.")
