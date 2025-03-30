
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemType, Rarity


SHIELD_TYPE = ItemType(
    id="shield",
    name="Shield",
    category=ItemCategory.EQUIPMENT,
    rarity=Rarity.RARE,
    texture_path="game-assets/graphics/pixil/BOMB_SHEET.pixil",
    cooldown=15.0,
    description="Temporary invincibility for 3 seconds",
    price=150  # Shield is valuable!
)

class ShieldStack(ItemStack):
    def __init__(self):
        super().__init__(SHIELD_TYPE, 1)
    
    def apply_effect(self, snake):
        print("shield apply effect")
    

class ShieldEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, SHIELD_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return ShieldStack()

    