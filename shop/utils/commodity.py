from dataclasses import dataclass
from bson.objectid import ObjectId

@dataclass
class Item:
    _id: ObjectId
    name: str
    description: str
    count: int
    price: int
    type: str