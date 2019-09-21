from configparser import ConfigParser
import pymodm
import hashlib
import binascii
import os


def init(config: ConfigParser):
    """
    Initializes the connection to the mongodb database using the credentials and other
    details contained in the config parser

    config (ConfigParser): The configurations for the database details
    """
    username = config['credentials']['username']
    password = config['credentials']['password']
    host = config['connection']['url']

    mongodb_url = 'mongodb://{}:{}@{}'.format(username, password, host)
    pymodm.connect(mongodb_url)


class User(pymodm.MongoModel):
    """
    Represents a single user that is kept track of by the server. Each other datapoint
    is associated with a user

    user_id (SequenceField): The unique of the user set automatically
    rfid (StringField): The id of the rfid chip associated with the user
    first_name (StringField): The first name of the user
    last_name (StringField): The last name of the user
    """
    rfid = pymodm.CharField()
    first_name = pymodm.CharField()
    last_name = pymodm.CharField()


class Lock(pymodm.MongoModel):
    """
    Represents a single smart lock that user can potentially access via their RFID chip.
    Each room keeps track of a list of users that can access the lock as well as other
    information about the lock.

    lock_id (SequenceField): The unique id of the lock set automatically
    description (StringField): A human readable description of the lock
    accepted_users (ListField(ReferenceField('User'))): The users that can unlock the lock
    """
    description = pymodm.CharField()
    accepted_users = pymodm.ListField(pymodm.ReferenceField(User))


class Temperature(pymodm.MongoModel):
    """
    A single temperature database for a specific user at a specific time

    temperature (FloatField): The temperature read at the time period
    user (ReferenceField(User)): The user that the temperature was collected for
    timestamp (TimestampField): The time when the temperature reading was recorded
    """
    temp_value = pymodm.FloatField()
    user = pymodm.ReferenceField(User)
    timestamp = pymodm.TimestampField()


class AdminAccount(pymodm.MongoModel):
    """
    Represents the account of an admin that has the ability to make changes to the system
    including changing user data and lock data

    user_name (CharField): The user name used as the identifier for the admin in the system
    password (CharField): The password of the admin to login to the system
    """
    user_name = pymodm.CharField()
    password = pymodm.CharField()


def _hash_password(password: str) -> str:
    """
    Hash the provided password using sha512
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def _verify_password(provided_password: str, correct_password: str) -> bool:
    """
    Verify a stored password against one provided by user

    provided_password (str): The plain text password attempting to be used to login
    correct_password (str): The hashed password that is the correct password
    """
    salt = correct_password[:64]
    correct_password = correct_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == correct_password


def verify_password(admin: AdminAccount, provided_password: str) -> bool:
    """
    Checks to see if the password provided for the given user name is valid

    admin (AdminAccount): The admin that is attempting to login
    provided_password (str): The plain text password provided by the user
    """
    correct_password = admin.password
    return _verify_password(provided_password, correct_password)
