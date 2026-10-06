-- Таблица обращений из формы на странице «связь».
-- IF NOT EXISTS: при каждом старте приложения файл выполняется заново,
-- а уже созданная таблица с данными остаётся как есть.
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    problem TEXT NOT NULL,
    description TEXT NOT NULL,
    adress TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
