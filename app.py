from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")



@app.route("/hello")
def hello_name():
    nameparams = request.args.get("name", "незнакомец")
    return render_template("greating.html", name=nameparams)

@app.route("/1234")
def one_two_three():
    a = request.args.get("a", 0)
    b = request.args.get("b", 0)
    return str(int(a) + int(b))

