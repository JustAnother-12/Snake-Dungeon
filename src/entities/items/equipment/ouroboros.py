

from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share


OUROBOROS_TYPE = ItemType(
    'ouroboros',
    'The Ouroboros',
    ItemCategory.EQUIPMENT,
    Rarity.RARE,
    ItemTexture(
        constant.Texture.ouroboros
    ),
    description="Saves the Player from  death on collision and consumes 1 body part (-1 Length). -50 Resistance when holding on this Equipment",
    price=150,
)

class OuroborosStack(ItemStack):
    def __init__(self):
        super().__init__(OUROBOROS_TYPE, 1)

    def apply_effect(self, snake):
        self.add_runtime_overriding(snake, 'handle_go_out_of_bounds', 'return', self.effect)

    def effect(self, snake, *args, **kwargs):
        if snake._will_go_out_of_bounds:
            if snake._out_of_bounds_time != None:
                if snake._out_of_bounds_time / 1000 > snake.base_stats.resistance/2:
                    block = snake.blocks.pop()
                    block.kill()
                    snake._out_of_bounds_time = None
                    snake._will_go_out_of_bounds = False
                else:
                    snake._out_of_bounds_time += Share.clock.get_time()
        else:
            snake._out_of_bounds_time = None

    def remove_effect(self, snake):
        self.remove_runtime_overriding(snake, 'handle_go_out_of_bounds', 'return', self.effect)

    def get_item_entity_class(self):
        return OuroborosEntity
    
class OuroborosEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, OUROBOROS_TYPE, area, r, quantity)
        self.eaten_by = self.level.snake
    
    def to_item_stack(self):
        return OuroborosStack()
        