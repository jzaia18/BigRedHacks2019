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
    user_id = mdb.SequenceField(required=True, primary_key=True)
    rfid = mdb.IntField()
    first_name = mdb.StringField(required=True)
    last_name = mdb.StringField(required=True)
