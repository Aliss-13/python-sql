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
    weight REAL
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
    level INTEGER,
    rarity_id INTEGER,

    FOREIGN KEY (rarity_id) REFERENCES rarities(id)
)""")

#------------------------------------------ ingredient_affinities -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredient_affinities (
    ingredient_id INTEGER,
    affinity_id INTEGER,
    value REAL,
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

#------------------------------------------ equipment -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
    rarity_id INTEGER,
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

connection.commit()

#------------------------------------------ affichage des tables et des colonnes -----------------------------

#for table in ["rarities", "affinities", "ingredients", "ingredient_affinities", "inventory", "equipment", "equipment_craft"]:
    #print(f"\n--- {table} ---")

#------------------------------------------ menu -----------------------------

print("            ┌──────────────────────┐            ")
print("            | Alchemy Lab-o-Matik  |            ")
print("            └──────────────────────┘            ")

menu(cursor, connection, player_level)

connection.close()