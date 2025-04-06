

from entities.Player import Snake, SnakeBlock
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity


RITUAL_DAGGER_TYPE = ItemType(
    'ritual_dagger',
    'Ritual Dagger',
    ItemCategory.SKILL,
    Rarity.COMMON,
    ItemTexture(
        "game-assets/graphics/pixil/item-sprite/RITUAL_DAGGER.pixil",
    ),
    "",
    activation_type=ActivationType.ON_USE,
    cooldown=3,
    energy_usage=10
)

class RitualDaggerEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, RITUAL_DAGGER_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return RitualDaggerStack(self.quantity)

class RitualDaggerStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(RITUAL_DAGGER_TYPE, quantity)

    def apply_effect(self, snake):
        print("ok")
        block = snake.blocks.pop()
        pos = snake._block_positions.pop()
        # snake.remove(block)
        block.can_collide = True
        block.sever("", 5)
        # snake.level.item_group.add(FakeSnakeBlock(snake.level, pos, block.color))
    
    def use(self, snake: Snake):
        # if len(snake.blocks) <= 4:
        #     return False
        return super().use(snake)
    
    def get_item_entity_class(self):
        return RitualDaggerEntity
    