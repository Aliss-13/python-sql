from pathlib import Path
from menu import menu
import sqlite3


BASE_DIR = Path(__file__).resolve().parent #C:\Users\lisas\OneDrive\Documents\Python\python-sql\3. ALCHEMY LABOMATIK
DATABASE_PATH = BASE_DIR / "database.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

connection.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    level INTEGER,
    rarity TEXT
)""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS affinities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredient_affinities (
    ingredient_id INTEGER,
    affinity_id INTEGER,
    value REAL,
    PRIMARY KEY (ingredient_id, affinity_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (affinity_id) REFERENCES affinity(id)
)""")

connection.commit()
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

tables = cursor.fetchall()

for table in tables:
    print(table[0])

for table in ["ingredients", "affinities", "ingredient_affinities"]:
    print(f"\n--- {table} ---")

    cursor.execute(f"PRAGMA table_info({table})")

    for column in cursor.fetchall():
        print(column)


menu(cursor, connection)

connection.close()