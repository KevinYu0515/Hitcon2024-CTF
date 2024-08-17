from utils.role import User
from utils.commodity import Item
from db import db

col = db['user']

def add_user(new_user):
    col.insert_one(new_user)

def query(username):
    try:
        user = col.find_one({'username': username}, {'_id': 0})
        return User(
                    username=user['username'],
                    point=user['point'],
                    items={key: Item(**val) for key, val in user['items'].items()}
                )
    except Exception as e:
        print(f"An unexpected error occurred in user: {e}")

def update(username, user):
    col.update_one({"username": username}, {"$set": user})