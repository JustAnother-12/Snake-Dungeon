import config.constant as constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity

COIN_TYPE = ItemType(
    'coin', 
    'Coin', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        "game-assets/graphics/pixil/GOLD_LEVEL.pixil",
    ),
    "gives 10 gold",
    activation_type=ActivationType.ON_COLLISION,
)

class CoinEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, COIN_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        self.level.snake.gold += self.item_type.value * self.quantity
    