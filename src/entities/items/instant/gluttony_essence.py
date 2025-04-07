from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


GLUTTONY_ESSENCE_TYPE = ItemType(
    'gluttony_essence',
    'Gluttony Essence', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.gluttony_essence,
    ),
    "+5 food potency",
    activation_type=ActivationType.ON_PICKUP
)

class GluttonyEssenceEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, GLUTTONY_ESSENCE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.FOOD_POTENCY, self.quantity * 5) # type: ignore
