import pymongo
from bson import ObjectId


class Mongo:
    client = None
    database=None

    @staticmethod
    def connect():
        Mongo.client=pymongo.MongoClient('mongodb://localhost:27017/')
        Mongo.database = Mongo.client['journalist']

    @staticmethod
    def insert (collection, data):
        Mongo.database[collection].insert(data)

    @staticmethod
    def get_all(collection):
        return Mongo.database[collection].find()

    @staticmethod
    def update(collection, _id, data):
        Mongo.database[collection].update_one({'_id': ObjectId(_id)}, data, upsert=False)

    @staticmethod
    def get_user(login):
        return Mongo.database['user'].find_one({"login": login})

    @staticmethod
    def get(collection, data):
        return Mongo.database[collection].find_one(data)