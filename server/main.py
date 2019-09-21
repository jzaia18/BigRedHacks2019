from flask import Flask, render_template
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route("/")
def root():
    return render_template("base.html")

@app.route("/temperature")
def temperature():
    return render_template("base.html")

@app.route("/airquality")
def airquality():
    return render_template("base.html")

@app.route("/unlock/<id_num>")
def unlock(id_num):
    print(id_num)
    return render_template("base.html")

@app.route("/lock/<id_num>")
def lock(id_num):
    print(id_num)
    return render_template("base.html")

@app.route("/check/<id_num>")
def check(id_num):
    print(id_num)
    return render_template("base.html")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
