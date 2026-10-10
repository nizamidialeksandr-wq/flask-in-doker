from flask import Flask, request
from flask import render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact", methods=["GET", "POST"], endpoint="contact")
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        name = request.form["name"]
        problem = request.form["problem"]
        description = request.form["description"]
        adress = request.form["adress"]



        conn = sqlite3.connect("database.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                problem TEXT NOT NULL,
                description TEXT NOT NULL,
                adress TEXT NOT NULL
            )
        """)
        conn.execute("INSERT INTO orders (name, problem, description, adress) VALUES (?, ?, ?, ?)", (name, problem, description, adress))
        conn.commit()
        conn.close()



        return render_template(
            "answer.html",
            name=name,
            problem=problem,
            description=description,
            adress=adress,
        )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/facts")
def facts():
    return render_template("facts.html")

@app.route("/eat")
def eat():
    return render_template("eat.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/orders")
def orders():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    orders = conn.execute("SELECT * FROM orders").fetchall()
    print(orders)
    conn.close()
    return render_template("orders.html", orders=orders)








