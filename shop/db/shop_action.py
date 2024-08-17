from utils.commodity import Item
from db import db
import json

col = db['commodity']

def initial():
    col.delete_many({})
    with open('db/commodity.json', 'r') as f:
        col.insert_many(json.load(f))

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