import sys
from pathlib import Path
import sqlite3

from database.database_creation_plan import create_tables
from menu import menu
from display.display_utils import display_main_menu
from player_game.game_functions.initialization import (
    initialize_containers,
    initialize_player_equipment,
    initialize_player_money
)


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "database.db"

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

connection.execute("PRAGMA foreign_keys = ON")


# ------------------------------------------------ création tables

create_tables(cursor)

# ------------------------------------------------ initialisation joueur

initialize_containers(cursor)
initialize_player_money(cursor)
initialize_player_equipment(cursor)

# ------------------------------------------------ commit

connection.commit()

# ------------------------------------------------ code temporaire 

# ------------------------------------------------ menu

try:
    display_main_menu()
    menu(cursor, connection)
finally:
    connection.close()