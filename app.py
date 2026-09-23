from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Привет, мир! Flask работает в контейнере."


@app.route("/hello")
def hello_name():
    name = request.args.get("name", "незнакомец")
    return f"Привет, {name}!"
