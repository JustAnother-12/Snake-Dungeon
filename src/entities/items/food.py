from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity


FOOD_TYPE = ItemType(
    'coin', 
    'Coin', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.apple,
    ),
    "",
    1
)

class FoodEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, FOOD_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        self.level.snake.grow_up(self.quantity)
    