from utils.commodity import Item
import pymongo, os

MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI) 
db = client.get_database()
col = db['commodity']

def initial():
    col.delete_many({})
    col.insert_one({"name": "flag{fake}", "price": 0, "description": "This is FLAG!!", "count": 1000, "type": "not for sale"})
    mylist = [
              { "name": "Cat Pillow", "price": 300, "description": "Very Soft and Cute.", "count": 1000, "type": "on sale"},
              { "name": "Dark Theme mouse pat", "price": 100, "description": "Super Cool.", "count": 1000, "type": "on sale"},
            ]
    col.insert_many(mylist)

def query(name):
    try:
        item = col.find_one({"name": name})
        return Item(**item)
    except Exception as e:
        print(f"An unexpected error occurred in buy: {e}")

def query_all():
    res = list()
    for item in col.find({'type': {'$ne': 'not for sale'}}):
        res.append(Item(**item))
    return res

def update(name, count):
    newvalues = { "$inc": { "count": count } }
    col.update_one({"name": name}, newvalues)