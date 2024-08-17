import pymongo, os

MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI) 
db = client.get_database()