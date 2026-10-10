# Шаг 1. Знакомство с SQLite без Flask.
# Запуск внутри контейнера:  docker compose exec web python db_demo.py
import sqlite3

# connect открывает файл базы. Если файла нет, SQLite его создаст.
conn = sqlite3.connect("demo.db")

# Таблица: как лист в Excel. IF NOT EXISTS — чтобы второй запуск не падал.
conn.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        problem TEXT NOT NULL
    )
""")

# Добавляем строку. Значения подставляем через ?, а не склейкой строк.
conn.execute("INSERT INTO messages (name, problem) VALUES (?, ?)", ("Саша", "не работает форма"))

# Без commit запись останется только в памяти и пропадёт при закрытии.
conn.commit()

# Читаем всё, что накопилось. Каждый запуск добавляет ещё одну строку.
rows = conn.execute("SELECT id, name, problem FROM messages ORDER BY id DESC").fetchall()
for row in rows:
    print(row)

conn.close()