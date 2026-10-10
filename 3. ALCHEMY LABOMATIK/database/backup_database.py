import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database.db"
BACKUP_PATH = BASE_DIR / "database_backup.sql"

connection = sqlite3.connect(DATABASE_PATH)

with open(BACKUP_PATH, "w", encoding="utf-8") as file:
    for line in connection.iterdump():
        file.write(line + "\n")

connection.close()