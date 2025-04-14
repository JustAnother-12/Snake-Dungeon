from pygame import Rect
from config import constant
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share
from stats import Stats


RESISTANCE_POTION_TYPE = ItemType(
    'resistance_potion',
    'Resistance Potion',
    ItemCategory.CONSUMABLE,
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.resistance_potion,
        0
    ),
    description=r"gives 50% resistance boost for 5s, 15s cooldown",
    max_stack=5,
    cooldown=15
)

class ResistancePotionStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(RESISTANCE_POTION_TYPE, quantity)
        self.active_duration = 5
        self.active_time = 0
        self.__last_resistance = 0
        
    def apply_effect(self, snake):
        self.active_time = self.active_duration

        self.__last_resistance = snake.base_stats.resistance

        self.add_runtime_overriding(snake, 'handle_go_out_of_bounds', 'before', self.boost_resistance)
    
    def boost_resistance(self, snake: Snake, *args, **kwargs):
        self.active_time -= Share.clock.get_time() / 1000
        if self.active_time <= 0:
            self.active_time = 0
            self.remove_runtime_overriding(snake, 'handle_go_out_of_bounds', 'before', self.boost_resistance)
        
        snake.base_stats.resistance = self.__last_resistance * 1.5
        return args, kwargs
    
    def get_item_entity_class(self):
        return ResistancePotionEntity

class ResistancePotionEntity(ItemEntity):
    def __init__(self, level, area: Rect | None = None, r=2, quantity=1):
        super().__init__(level, RESISTANCE_POTION_TYPE, area, r, quantity)

    def to_item_stack(self):
        return ResistancePotionStack(self.quantity)
