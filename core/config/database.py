import pymongo
from pymongo.mongo_client import MongoClient

from core.config.env import Env

env = Env()


class AuthDatabase:
    uri = 'mongodb+srv://' + env.MONGODB_USERNAME + ':' + \
        env.MONGODB_PASSWORD.get_secret_value() + \
        '@' + env.MONGODB_CLUSTER + '/?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client['auth_db']  # Set the database name to 'auth_db'

    auth_collection = db['auth']  # Set the collection name to 'auth'
    # Create a unique constraint on the 'email' field in the 'auth' collection
    auth_collection.create_index([('email', pymongo.ASCENDING)], unique=True)
