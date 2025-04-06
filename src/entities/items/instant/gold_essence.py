from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


GOLD_ESSENCE_TYPE = ItemType(
    'gold_essence',
    'Gold Essence', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.gold_essence,
    ),
    "",
    1,
    price=10,
    activation_type=ActivationType.ON_PICKUP
)

class GoldEssenceEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, GOLD_ESSENCE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.TREASURY, self.quantity * 5) # type: ignore
