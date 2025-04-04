from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from levels.components.bomb import Bomb, BombState


BOMB_TYPE = ItemType(
    'bomb',
    'Bomb',
    ItemCategory.CONSUMABLE,
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.bomb
    ),
    max_stack=10,
    cooldown=3.0
)

class BombStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(BOMB_TYPE, quantity)

    def apply_effect(self, snake):
        snake.level.bomb_group.add(Bomb(snake.level, snake.blocks[-1].pos, BombState.ACTIVE))
    
    def get_item_entity_class(self):
        return BombEntity


class BombEntity(ItemEntity):
    def __init__(self, level, area = None, r=2, quantity=1):
        super().__init__(level, BOMB_TYPE, area, r, quantity)

    def to_item_stack(self):
        return BombStack(self.quantity)