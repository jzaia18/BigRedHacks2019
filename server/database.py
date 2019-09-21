from configparser import ConfigParser
import mongoengine as mdb


def init(config: ConfigParser):
    """
    Initializes the connection to the mongodb database using the credentials and other
    details contained in the config parser

    config (ConfigParser): The configurations for the database details
    """
    username = config['credentials']['username']
    password = config['credentials']['password']
    host = config['connection']['url']
    project_name = config['connection']['project_name']

    mdb.connect(
        project_name,
        host=host,
        username=username,
        password=password
    )


class User(mdb.Document):
    """
    Represents a single user that is kept track of by the server. Each other datapoint
    is associated with a user

    user_id (SequenceField): The unique of the user set automatically
    rfid (IntField): The id of the rfid chip associated with the user
    first_name (StringField): The first name of the user
    last_name (StringField): The last name of the user
    """
    user_id = mdb.SequenceField(required=True, primary_key=True)
    rfid = mdb.IntField()
    first_name = mdb.StringField(required=True)
    last_name = mdb.StringField(required=True)


class Lock(mdb.Document):
    """
    Represents a single smart lock that user can potentially access via their RFID chip.
    Each room keeps track of a list of users that can access the lock as well as other
    information about the lock.

    lock_id (SequenceField): The unique id of the lock set automatically
    description (StringField): A human readable description of the lock
    accepted_users (ListField(ReferenceField('User'))): The users that can unlock the lock
    """
    lock_id = mdb.SequenceField(required=True, primary_key=True)
    description = mdb.StringField()
    accepted_users = mdb.ListField(mdb.ReferenceField('User'))
