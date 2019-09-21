from configparser import ConfigParser
import pymodm


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
    temperature = pymodm.FloatField()
    user = pymodm.ReferenceField(User)
    timestamp = pymodm.TimestampField()
