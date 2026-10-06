# Урок: SQLite во Flask

Цель занятия: обращения из формы на странице «связь» сохраняются в базу, а на новой странице
«обращения» видно их все.

Теория — в [02-sqlite-teoriya.md](02-sqlite-teoriya.md). Каждый шаг ниже — отдельный коммит
в ветке `sqlite`, его можно открыть на GitHub и посмотреть, что поменялось.

## Шаг 0. Подготовка

```bash
git fetch
git checkout sqlite
docker compose up
```

`--build` не нужен: `requirements.txt` и `Dockerfile` не менялись. Модуль `sqlite3` уже есть
внутри Python, ставить ничего не надо.

Вопросы из теории на разогрев:

- чем база отличается от папки с файлами;
- зачем `commit`, если `INSERT` уже выполнен;
- почему SQLite не нужен отдельный сервис в compose, а PostgreSQL нужен.

## Шаг 1. Потрогать базу руками

Файл `db_demo.py`. Без Flask: открыть базу, создать таблицу, добавить строку, прочитать.

Запуск во втором терминале, пока работает `docker compose up`:

```bash
docker compose exec web python db_demo.py
```

Запустить два-три раза: строк становится больше, данные живут в файле `demo.db`.

Что попробовать тут же:

- закомментировать `conn.commit()` и запустить: новая строка не сохранится;
- убрать `IF NOT EXISTS` и запустить: ошибка «table messages already exists».

Поиграть в живом Python внутри контейнера:

```bash
docker compose exec web python
```

```python
import sqlite3
conn = sqlite3.connect("demo.db")
conn.execute("SELECT COUNT(*) FROM messages").fetchone()
conn.execute("SELECT * FROM messages WHERE name = ?", ("Саша",)).fetchall()
conn.execute("DELETE FROM messages WHERE id = ?", (1,))
conn.commit()
```

Выход — `exit()`.

## Шаг 2. Схема и подключение для сайта

Новые файлы:

- `schema.sql` — описание таблицы `messages`: те же четыре поля, что в форме, плюс `id`
  и `created_at` (время заполнит сама база);
- `db.py` — две функции: `get_db()` открывает базу `app.db`, `init_db()` выполняет `schema.sql`.

В `app.py` при старте вызывается `init_db()`. Таблица создаётся один раз, дальше
`IF NOT EXISTS` её не трогает.

Обратить внимание:

- `row_factory = sqlite3.Row` — строки из базы можно читать как словарь: `row["name"]`;
- SQL лежит в отдельном файле, а не строкой в Python: так его проще читать и править.

## Шаг 3. Запись из формы

В обработчике `POST` на `/contact`, перед `render_template`:

```python
conn = get_db()
conn.execute(
    "INSERT INTO messages (name, problem, description, adress) VALUES (?, ?, ?, ?)",
    (name, problem, description, adress),
)
conn.commit()
conn.close()
```

Проверка: отправить форму, потом посмотреть в базу через шаг 1, только с `app.db`.

### Почему `?`, а не f-строка

Показать вживую, потом вернуть как было:

```python
conn.execute(f"INSERT INTO messages (name, problem, description, adress) VALUES ('{name}', '{problem}', '{description}', '{adress}')")
```

В поле «имя» ввести `Д'Артаньян` — запрос падает с синтаксической ошибкой: кавычка из имени
закрыла строку в SQL. Это и есть дыра: вместо кавычки можно подсунуть свой кусок SQL.
С `?` база получает значения отдельно от запроса и такое не пройдёт.

## Шаг 4. Страница со всеми обращениями

- в `app.py` новый адрес `/messages`: `SELECT * FROM messages ORDER BY id DESC` и передача
  строк в шаблон;
- `templates/messages.html` — таблица, строки выводятся циклом `{% for m in messages %}`;
- в меню `base.html` новый пункт «обращения»;
- в `style.css` рамки для таблицы.

Проверка: http://localhost:5000/messages, отправить ещё пару обращений, обновить страницу.
Перезапустить `docker compose` — записи на месте, потому что `app.db` лежит в папке проекта.

Бонус: отправить в описании `<b>жирно</b>`. В таблице видны теги, а не жирный текст: Jinja
экранирует всё, что пришло от пользователя.

## Грабли

- Файлы `app.db` и `demo.db` создаёт контейнер от root. Удалить их из Ubuntu можно
  обычным `rm`, а вот редактировать без `sudo` не выйдет.
- Базы в git не коммитим: `*.db` добавлены в `.gitignore`.
- Время в `created_at` записывается по UTC, на три часа меньше московского.
- Форма на самом деле уходит из `static/script.js` через `fetch("/contact")`, адрес там
  записан руками. Поэтому на прошлом занятии `url_for('contact')` в `action` формы
  ни на что не влиял: JS отменяет обычную отправку и шлёт запрос сам.

## Домашка

1. На странице `/messages` показывать только последние 10 обращений (`LIMIT`).
2. Кнопка «удалить» у каждой строки: `POST` на `/messages/<id>/delete`, внутри
   `DELETE FROM messages WHERE id = ?`, потом `redirect` обратно на `/messages`.
3. Поиск по имени: `/messages?name=Саша` показывает только его обращения (`WHERE name = ?`).
4. В `script.js` брать адрес из формы (`form.action`), а не писать `/contact` руками.
