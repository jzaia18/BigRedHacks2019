from flask import Flask, render_template, request, Response
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

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/temperature")
def temperature():
    return render_template("temperature.html")

@app.route("/airquality")
def airquality():
    return render_template("airquality.html")

@app.route("/lock/query/<id_num>")
def query_lock(id_num):
    # Get the lock from the database
    lock = database.Lock.objects(lock_id=id_num)[0]

    # Test output
    output = 'Lock: ' + str(lock.lock_id) + '\n'
    for user in lock.accepted_users:
        output += 'User: ' + user.first_name + '\n'
    return output

@app.route("/unlock/<id_num>")
def unlock(id_num):
    print(id_num)
    return render_template("base.html")

@app.route("/add/<id_num>")
def add_user_lock(id_num):
    # Get the rfid and the user specified
    rfid = request.args.get('rfid')
    print(rfid)
    user = database.User.objects(rfid=rfid)[0]
    lock = database.Lock.objects(lock_id=id_num)[0]
    print(type(lock))

    # Add the user to the accepted user list of the lock and update the database
    lock.accepted_users.append(user)
    lock.save()
    return Response(status=200)

@app.route("/remove/<id_num>")
def remove_user_lock(id_num):
    # Get the rfid and the user specified
    rfid = request.args.get('rfid')
    user = database.User.objects(rfid=rfid)[0]
    lock = database.Lock.objects(lock_id=id_num)[0]

    # Remove the user from the accepted user list for the lock
    lock.accepted_users.remove(user)
    lock.save()

    return Response(status=200)

@app.route("/user/create")
def create_user():
    # Get the data for the user
    rfid = request.args.get('rfid')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    # Create a new user and save the user to the database
    user = database.User(rfid=rfid, first_name=first_name, last_name=last_name)
    user.save()
    return Response(status=200)

@app.route("/usermod")
def usermod():
    return render_template("base.html")

if __name__ == "__main__":
    # Parse in connection details for the database
    current_dir = Path(os.path.abspath(os.path.dirname(__file__)))
    mongo_config_file = current_dir / 'config' / 'database.ini'
    config = ConfigParser()
    config.read(mongo_config_file)
    database.init(config)

    app.debug = True
    app.run(host="0.0.0.0")
