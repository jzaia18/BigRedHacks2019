from flask import Flask, render_template
from functools import wraps
import os
from configparser import ConfigParser
from pathlib import Path
import database

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route("/")
def root():
    return render_template("base.html")

@app.route("/temperature")
def temperature():
    return render_template("temperature.html")

@app.route("/airquality")
def airquality():
    return render_template("airquality.html")

@app.route("/unlock/<id_num>")
def unlock(id_num):
    print(id_num)
    return render_template("base.html")

@app.route("/check/<id_num>")
def check(id_num):
    print(id_num)
    return render_template("base.html")

@app.route("/add/<id_num>")
def add(id_num):
    print(id_num)
    return render_template("base.html")

@app.route("/remove/<id_num>")
def remove(id_num):
    print(id_num)
    return render_template("base.html")


if __name__ == "__main__":
    # Parse in connection details for the database
    current_dir = Path(os.path.abspath(os.path.dirname(__file__)))
    mongo_config_file = current_dir / 'config' / 'database.ini'
    config = ConfigParser()
    config.read(mongo_config_file)

    # Initialize the database connection
    database.init(config)
    #database.query_users()

    app.debug = True
    app.run(host="0.0.0.0")
