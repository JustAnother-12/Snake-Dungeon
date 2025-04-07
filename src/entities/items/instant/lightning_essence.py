from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


LIGHTNING_ESSENCE_TYPE = ItemType(
    'lightning_essence',
    'Light Essence', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.lightning_essence,
    ),
    "+5 energy regen",
    activation_type=ActivationType.ON_PICKUP
)

class LightningEssenceEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, LIGHTNING_ESSENCE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.ENERGY_REGEN, self.quantity * 5) # type: ignore
