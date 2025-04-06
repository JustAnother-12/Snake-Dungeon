from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


EARTH_ESSENCE_TYPE = ItemType(
    'earth_essence',
    'Earth Essence', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.earth_essence,
    ),
    "",
    1,
    price=10,
    activation_type=ActivationType.ON_PICKUP
)

class EarthEssenceEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, EARTH_ESSENCE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.RESISTANCE, self.quantity * 5) # type: ignore
