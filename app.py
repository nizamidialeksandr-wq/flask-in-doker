from flask import Flask, request
from flask import render_template

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








