from pathlib import Path
from menu import menu
import sqlite3


BASE_DIR = Path(__file__).resolve().parent #C:\Users\lisas\OneDrive\Documents\Python\python-sql\2. MAGIQUE BOUTIQUE
DATABASE_PATH = BASE_DIR / "database.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

connection.execute("PRAGMA foreign_keys = ON")

cursor.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER,
    purchase_price REAL
)""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        city TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        date TEXT,
        
        FOREIGN KEY (customer_id) REFERENCES customers(id)   
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_purchases (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        unit_purchase_price REAL,
        date TEXT,
    
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (
        id INTEGER PRIMARY KEY,
        sale_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        unit_purchase_price REAL,

        FOREIGN KEY (sale_id) REFERENCES sales(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")

connection.commit()


menu(cursor, connection)


connection.close()