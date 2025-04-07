from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


GALE_ESSENCE_TYPE = ItemType(
    'gale_essence',
    'Gale Essence', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.gale_essence,
    ),
    "+5 speed",
    activation_type=ActivationType.ON_PICKUP
)

class GaleEssenceEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, GALE_ESSENCE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.SPEED, self.quantity * 5) # type: ignore
