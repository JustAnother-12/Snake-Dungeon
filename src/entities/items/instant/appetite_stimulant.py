from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


APPETITE_STIMULANT_TYPE = ItemType(
    'appetite_stimulant',
    'Appetite Stimulant',
    ItemCategory.INSTANT, 
    Rarity.UNCOMMON,
    ItemTexture(
        constant.Texture.appetite_stimulant
    ),
    "+10 food potency, +10 energy cap",
    activation_type=ActivationType.ON_PICKUP
)

class AppetiteStimulantEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, APPETITE_STIMULANT_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.ENERGY_CAPACITY, self.quantity * 10)
        Stats.increaseValue(StatType.FOOD_POTENCY, self.quantity * 10)
