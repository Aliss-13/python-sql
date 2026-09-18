from pathlib import Path
from menu import menu
import sqlite3

player_level = 1

BASE_DIR = Path(__file__).resolve().parent #C:\Users\lisas\OneDrive\Documents\Python\python-sql\3. ALCHEMY LABOMATIK
DATABASE_PATH = BASE_DIR / "database.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

connection.execute("PRAGMA foreign_keys = ON")

#------------------------------------------ rarities -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS rarities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    color TEXT NOT NULL,
    weight REAL NOT NULL
)""")

#------------------------------------------ affinities -----------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS affinities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        icon TEXT
    )""")

#------------------------------------------ ingredients -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    level INTEGER NOT NULL,
    rarity_id INTEGER NOT NULL,

    FOREIGN KEY (rarity_id) REFERENCES rarities(id)
)""")

#------------------------------------------ ingredient_affinities -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredient_affinities (
    ingredient_id INTEGER,
    affinity_id INTEGER,
    value REAL NOT NULL,
    PRIMARY KEY (ingredient_id, affinity_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (affinity_id) REFERENCES affinities(id)
)""")

#------------------------------------------ inventory -----------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        ingredient_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
)""")

#------------------------------------------ equipment_categories -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment_categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)""")

#------------------------------------------ equipment -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category_id INTEGER,
    description TEXT,
    rarity_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES equipment_categories(id),
    FOREIGN KEY (rarity_id) REFERENCES rarities(id)
)""")

#------------------------------------------ equipment_craft -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment_craft (
    equipment_id INTEGER,
    ingredient_id INTEGER,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (equipment_id, ingredient_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
)""")

#------------------------------------------ mixing_tools -----------------------------

cursor.execute("""CREATE TABLE IF NOT EXISTS mixing_tools (
    equipment_id INTEGER PRIMARY KEY,
    capacity INTEGER NOT NULL,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
)""")


connection.commit()

#------------------------------------------ affichage des tables et des colonnes -----------------------------

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

tables = cursor.fetchall()

for table in tables:
    print(table[0])

for table in ["rarities", "affinities", "ingredients", "ingredient_affinities", "inventory", "equipment", "equipment_categories", "equipment_craft", "mixing_tools"]:
    print(f"\n--- {table} ---")

    cursor.execute(f"PRAGMA table_info({table})")

    for column in cursor.fetchall():
        print(column)

#------------------------------------------ menu -----------------------------

print("            ┌──────────────────────┐            ")
print("            | Alchemy Lab-o-Matik  |            ")
print("            └──────────────────────┘            ")

menu(cursor, connection, player_level)

connection.close()