from flask import Flask, render_template, request, Response, redirect
from functools import wraps
import os, json
from configparser import ConfigParser
from pathlib import Path
import database
from bson import ObjectId

app = Flask(__name__)
app.secret_key = os.urandom(16)


#authentication wrapper
def require_login(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'uname' not in session:
            flash("Please log in to use this feature")
            return redirect(url_for("login"))
        else:
            return f(*args, **kwargs)
    return inner

@app.route("/")
def root():
    return render_template("base.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_attempt", methods=['POST'])
def login_attempt():
    user_name = request.form['email'].lower()
    print(user_name)
    password = request.form['password']
    admins = database.AdminAccount.objects.all()
    admins = list(filter(lambda admin: admin.user_name.lower() == user_name, admins))
    # Invalid username
    if len(admins) == 0:
        return redirect('/login')
    admin = admins[0]
    if database.verify_password(admin, password) is not True:
        print('there')
        return redirect('/login')
    return redirect('/usermod')


@app.route("/temperature")
def temperature():
    """
    Handles displaying the temperature data for a specific user. Takes in id of the user
    and returns the temperature data displayed in HTML
    """
    return render_template("temperature.html")

@app.route("/get_temperature")
def get_temp():
    """
    Handles displaying the temperature data for a specific user. Takes in id of the user
    and returns the temperature data displayed in HTML
    """
    f = open("info_pipe", 'r')
    temperature = f.read()
    print(temperature+"F")
    temperature = temperature.split(',')[1]
    f.close()
    s = {'temp': temperature}
    res = json.dumps(s)
    return res

@app.route("/add_temperature")
def add_temperature():
    """
    Add temperature data to the database associated with a given user
    """
    temperature_value = request.form['value']
    timestamp = request.form['timestamp']
    user = database.User.objects.get({'rfid', request.form['rfid']})
    temperature = database.Temperature(temp_value=temperature, timestamp=timestamp, user=user)


@app.route("/airquality")
def airquality():
    """
    Handles displaying the air quality for a specific user. Takes in id of the user and
    returns the airquality data displayed in HTML
    """
    return render_template("airquality.html")


@app.route("/lock/create")
def lock_create():
    """
    Creates a new smart lock that has a description associated with it. The description
    is a human-readable short detail of what the lock is for. By default the lock is
    saved with no access granted to any user.
    """
    description = request.args.get('description')
    new_lock = database.Lock(description=description)
    new_lock.save()
    return Response(status=200)


@app.route("/lock/query/<id_num>")
def query_lock(id_num):
    """
    Handles getting information for a given lock. The lock data is returned as a string
    for testing including the ID of the lock and the users that are able to unlock the
    given lock

    id_num (int): The ID of the lock to get information for
    """
    # Get the lock from the database
    lock = database.Lock.objects.get({'_id': ObjectId(id_num)})

    # Test output
    output = 'Lock: ' + str(lock._id) + '\n'
    for user in lock.accepted_users:
        output += 'User: ' + user.first_name + '\n'
    return output


@app.route("/unlock/<id_num>")
def unlock(id_num):
    """
    Handles unlocking a specific lock. A user that is a member of the accepted list of
    users for the lock can successfully unlock the door
    """
    user_rfid = request.args.get('rfid')

    lock = database.Lock.objects.get({'_id': ObjectId(id_num)})
    user = database.User.objects.get({'rfid': user_rfid})
    if user in lock.accepted_users:
        print('PLACE HOLDER FOR UNLOCKING LOCK')
    else:
        print('PLACE HOLDER FOR FAILURE TO UNLOCK LOCK')
    return Response(status=200)


@app.route("/add/<id_num>")
def add_user_lock(id_num):
    """
    Add a given user to the list of accepted users for a lock. Passed in as a get
    parameter is the ID of the user to ad
    """
    # Get the rfid and the user specified
    rfid = request.args.get('rfid')
    user = database.User.objects.get({'rfid': rfid})
    lock = database.Lock.objects.get({'_id': ObjectId(id_num)})

    # Add the user to the accepted user list of the lock and update the database
    lock.accepted_users.append(user)
    lock.save()
    return Response(status=200)


@app.route("/remove/<id_num>")
def remove_user_lock(id_num):
    """
    Removes a users for the accepted list of users that can unlock a specific lock.
    """
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
    """
    Handles creating a user with an rfid and a name associated with it. The rfid is the
    id of the chip of the user and the name of the user is included.

    rfid (str): A string representation of the rfid
    name (str): The name of the user
    """
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
    locks = database.Lock.objects.all()
    return render_template("usermod.html", locks=locks)

if __name__ == "__main__":
    # Parse in connection details for the database
    current_dir = Path(os.path.abspath(os.path.dirname(__file__)))
    mongo_config_file = current_dir / 'config' / 'database.ini'
    config = ConfigParser()
    config.read(mongo_config_file)
    database.init(config)

    app.debug = True
    app.run(host="0.0.0.0")
