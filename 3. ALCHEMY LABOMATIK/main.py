import os
from pathlib import Path
import sqlite3

from database.database_creation_plan import create_tables
from menu import menu
from display.display_utils import display_main_menu
from player_game.initialization import initialize_containers, initialize_player_equipment, initialize_player_money
from player_game.reset_game import reset_game, test_reset_game

BASE_DIR = Path(__file__).resolve().parent #C:\Users\lisas\OneDrive\Documents\Python\python-sql\3. ALCHEMY LABOMATIK
DATABASE_PATH = BASE_DIR / "database.db"
print(os.path.abspath("database.db"))

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

connection.execute("PRAGMA foreign_keys = ON")


# ------------------------------------------------ création tables

create_tables(cursor)

# ------------------------------------------------ REINITIALISATION JOUEUR

#reset_game(cursor, connection)
#test_reset_game(cursor)

# ------------------------------------------------ initialisation joueur

initialize_containers(cursor, connection)
initialize_player_money(cursor, connection)
initialize_player_equipment(cursor, connection)

# ------------------------------------------------ commit

connection.commit()

# ------------------------------------------------ code temporaire 

# ------------------------------------------------ menu

display_main_menu()

menu(cursor, connection)

connection.close()


