

from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity


KEY_TYPE = ItemType(
    'key',
    'Key',
    ItemCategory.INSTANT,
    Rarity.COMMON,
    ItemTexture(
        "game-assets/graphics/pixil/KEY_SPRITE.pixil",
    ),
    "key for locked chests",
    activation_type=ActivationType.ON_COLLISION      
)

class KeyEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, KEY_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        self.level.snake.keys += 1
    