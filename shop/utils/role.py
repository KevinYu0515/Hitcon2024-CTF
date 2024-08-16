from dataclasses import dataclass, field
import db.action as db 
from utils.commodity import Item
from typing import Dict

@dataclass
class User:
    point: int
    items: Dict[str, Item] = field(default_factory=dict)

    def buy_item(self, buy_item: Item):
        if(buy_item.type == 'not for sale'):
            return
        if self.point >= buy_item.price:
            self.point -= buy_item.price
            if buy_item.name in self.items:
                self.items[buy_item.name].count += 1
            else:
                self.items[buy_item.name] = buy_item
                self.items[buy_item.name].count = 1
            db.update(buy_item.name, -1)
        else:
            raise ValueError(f"Not enough points to complete the purchase.")

    def sell_item(self, sell_name):
        if sell_name in self.items:
            self.point += self.items[sell_name].price
            self.items[sell_name].count -= 1
            if self.items[sell_name].count == 0:
                del self.items[sell_name]
            db.update(sell_name, 1)
        else:
            raise ValueError(f"Item '{sell_name}' not found in the user's items.")