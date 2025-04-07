from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


ENERGIZED_CRYSTAL_TYPE = ItemType(
    'energized_crystal',
    'Energized Crystal',
    ItemCategory.INSTANT, 
    Rarity.UNCOMMON,
    ItemTexture(
        constant.Texture.energized_crystal
    ),
    "+10 energy cap, +10 energy regen",
    activation_type=ActivationType.ON_PICKUP
)

class EnergizedCrystalEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, ENERGIZED_CRYSTAL_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        Stats.increaseValue(StatType.ENERGY_CAPACITY, self.quantity * 10)
        Stats.increaseValue(StatType.ENERGY_REGEN, self.quantity * 10)
