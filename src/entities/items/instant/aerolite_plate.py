from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


AEROLITE_PLATE_TYPE = ItemType(
    'aerolite_plate',
    'Aerolite Armor Plate',
    ItemCategory.INSTANT, 
    Rarity.UNCOMMON,
    ItemTexture(
        constant.Texture.aerolite_plate
    ),
    "+10 resistance, + 10 speed",
    activation_type=ActivationType.ON_PICKUP
)

class AerolitePlateEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, AEROLITE_PLATE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.RESISTANCE, self.quantity * 10)
        Stats.increaseValue(StatType.SPEED, self.quantity * 10)
