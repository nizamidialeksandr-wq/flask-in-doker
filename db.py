import sqlite3

# Файл базы лежит в папке проекта. Папка примонтирована в контейнер,
# поэтому база переживает перезапуск docker compose.
DB_PATH = "app.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    # строки будут вести себя как словарь: row["name"] вместо row[1]
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    with open("schema.sql", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.close()
