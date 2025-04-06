from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


WATER_ESSENCE_TYPE = ItemType(
    'water_essence',
    'Water Essence', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.water_essence,
    ),
    "",
    1,
    price=10,
    activation_type=ActivationType.ON_PICKUP
)

class WaterEssenceEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, WATER_ESSENCE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.ENERGY_CAPACITY, self.quantity * 5) # type: ignore
