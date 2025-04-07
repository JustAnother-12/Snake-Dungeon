from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


ADRENALINE_SYRINGE_TYPE = ItemType(
    'adrenaline_syringe',
    'Adrenaline Syringe',
    ItemCategory.INSTANT, 
    Rarity.RARE,
    ItemTexture(
        constant.Texture.adrenaline_syringe
    ),
    "+10 energy regen, +10 resistance, + 10 speed",
    activation_type=ActivationType.ON_PICKUP
)

class AdrenalineSyringeEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, ADRENALINE_SYRINGE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.SPEED, self.quantity * 10)
        Stats.increaseValue(StatType.ENERGY_REGEN, self.quantity * 10)
        Stats.increaseValue(StatType.RESISTANCE, self.quantity * 10)
