from bson import ObjectId

from database import Mongo


def add_file(title, description, file, datetime):
    Mongo.insert('img',{'title': title, 'file': file, 'description': description, 'datetime':datetime})

def edit_file(_id, description):
    Mongo.update('img', _id, {'$set': {'description': description}})

def get_file():
    return Mongo.get_all('img')

def get_work(_id):
    return Mongo.get('img', {'_id': ObjectId(_id)})

def get_post():
    return Mongo.get_all('img')