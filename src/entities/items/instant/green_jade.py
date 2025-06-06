from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


GREEN_JADE_TYPE = ItemType(
    'green_jade',
    'Green Jade Pellet',
    ItemCategory.INSTANT, 
    Rarity.UNCOMMON,
    ItemTexture(
        constant.Texture.green_jade,
    ),
    "+10 luck, +5 treasury",
    activation_type=ActivationType.ON_PICKUP
)

class GreenJadeEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, GREEN_JADE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.LUCK, self.quantity * 10)
        Stats.increaseValue(StatType.TREASURY, self.quantity * 5)
