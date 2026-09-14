from pathlib import Path
from menu import menu
import sqlite3

player_level = 1

BASE_DIR = Path(__file__).resolve().parent #C:\Users\lisas\OneDrive\Documents\Python\python-sql\3. ALCHEMY LABOMATIK
DATABASE_PATH = BASE_DIR / "database.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

connection.execute("PRAGMA foreign_keys = ON")

#------------------------------------------ table rarities -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS rarities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    color TEXT NOT NULL,
    weight REAL
)""")

#------------------------------------------ table affinities -----------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS affinities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        icon TEXT
    )""")

#------------------------------------------ table ingredients -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    level INTEGER,
    rarity_id INTEGER,

    FOREIGN KEY (rarity_id) REFERENCES rarities(id)
)""")

#------------------------------------------ table ingredient_affinities -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredient_affinities (
    ingredient_id INTEGER,
    affinity_id INTEGER,
    value REAL,
    PRIMARY KEY (ingredient_id, affinity_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (affinity_id) REFERENCES affinities(id)
)""")

#------------------------------------------ table inventory -----------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        ingredient_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
)""")

connection.commit()

#------------------------------------------ menu -----------------------------

menu(cursor, connection, player_level)

connection.close()