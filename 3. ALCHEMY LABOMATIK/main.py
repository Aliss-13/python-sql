from pathlib import Path
import sqlite3

from database.database_creation_plan import create_tables
from menu import menu
from display.display_utils import display_main_menu
from player_game.initialization import initialize_containers, initialize_player_equipment, initialize_player_money

BASE_DIR = Path(__file__).resolve().parent #C:\Users\lisas\OneDrive\Documents\Python\python-sql\3. ALCHEMY LABOMATIK
DATABASE_PATH = BASE_DIR / "database.db"

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

player_level = 1

connection.execute("PRAGMA foreign_keys = ON")

# création tables

create_tables(cursor)

# initialisation joueur

initialize_containers(cursor, connection)
initialize_player_money(cursor, connection)
initialize_player_equipment(cursor, connection)

# commit
cursor.execute("""
UPDATE shop_inventory
SET quantity = 3
WHERE recipe_id = 5
""")

cursor.execute("""
UPDATE shop_inventory
SET quantity = 3
WHERE recipe_id = 12
""")

cursor.execute("""
UPDATE shop_inventory
SET quantity = 3
WHERE recipe_id = 13
""")

connection.commit()

# code temporaire 

# menu

display_main_menu()

menu(cursor, connection, player_level)

connection.close()


