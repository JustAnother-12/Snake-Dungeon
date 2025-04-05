from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


LUCK_ESSENCE_TYPE = ItemType(
    'luck_essence',
    'Luck Essence', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.luck_essence,
    ),
    "",
    1,
    price=10,
    activation_type=ActivationType.ON_PICKUP
)

class LuckEssenceEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, LUCK_ESSENCE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.LUCK, self.quantity * 5) # type: ignore
