from flask import Flask, request
from flask import render_template

app = Flask(__name__)


# @app.route("/")
# def hello():
#     return render_template("index.html")



# @app.route("/hello")
# def hello_name():
#     nameparams = request.args.get("name", "незнакомец")
#     return render_template("greating.html", name=nameparams)

# @app.route("/1234")
# def one_two_three():
#     a = request.args.get("a", 0)
#     b = request.args.get("b", 0)
#     return str(int(a) + int(b))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/facts")
def facts():
    return render_template("facts.html")

@app.route("/eat")
def eat():
    return render_template("eat.html")
