from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from stats import StatType, Stats


DUNGEON_ESSENCE_TYPE = ItemType(
    'dungeon_essence',
    'Essence of The Dungeon', 
    ItemCategory.INSTANT, 
    Rarity.RARE,
    ItemTexture(
        constant.Texture.dungeon_essence,
    ),
    "+5 Every stats (Length excluded)",
    activation_type=ActivationType.ON_PICKUP
)

class DungeonEssenceEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, DUNGEON_ESSENCE_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        for stat in StatType:
            Stats.increaseValue(stat, self.quantity * 5) # type: ignore
