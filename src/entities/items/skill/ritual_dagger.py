

from config import constant
from entities.Player import Snake, SnakeBlock
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share


RITUAL_DAGGER_TYPE = ItemType(
    'ritual_dagger',
    'Ritual Dagger',
    ItemCategory.SKILL,
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.ritual_dagger,
    ),
    "Upon activation, cuts 1 body part of the Player. That body part stays on the field for 5s and can be consume. Consumes 10 Energy, 3s cooldown",
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
        Share.audio.play_sound("blade-slice")
        block = snake.blocks[-1]
        block.is_edible = True
        snake.split(-1, delay=5)
        Share.audio.play_sound("body_part_cutoff")
    
    def use(self, snake: Snake):
        # if len(snake.blocks) <= 4:
        #     return False
        return super().use(snake)
    
    def get_item_entity_class(self):
        return RitualDaggerEntity
    