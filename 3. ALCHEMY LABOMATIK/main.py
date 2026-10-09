from pathlib import Path
import sqlite3
from database_creation_plan import create_tables
from menu import menu
from display_utils import display_main_menu


BASE_DIR = Path(__file__).resolve().parent #C:\Users\lisas\OneDrive\Documents\Python\python-sql\3. ALCHEMY LABOMATIK
DATABASE_PATH = BASE_DIR / "database.db"

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

player_level = 1

connection.execute("PRAGMA foreign_keys = ON")

create_tables(cursor)

# commit
connection.commit()

# code temporaire 

# menu

display_main_menu()

menu(cursor, connection, player_level)

connection.close()




#cursor.execute("""
#    UPDATE inventory
#    SET quantity = quantity + 20
#    WHERE ingredient_id = 15
#    """)