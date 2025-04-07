from pygame import Rect
from config import constant
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share
from stats import Stats


SPEED_BOOT_TYPE = ItemType(
    'speed_potion',
    'Speed Potion',
    ItemCategory.CONSUMABLE,
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.speed_potion,
        0
    ),
    description="gives x1.5 speed boost for 5s, 7s cooldown",
    max_stack=5,
    cooldown=7.0
)

class SpeedPotionStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(SPEED_BOOT_TYPE, quantity)
        self.active_duration = 5
        self.active_time = 0
        self.last_speed = 0
        
    def apply_effect(self, snake):
        self.active_time = self.active_duration

        self.last_speed = snake.base_stats.speed

        self.add_runtime_overriding(snake, 'handle_speed_boost', 'before', self.speed_potion)
    
    def speed_potion(self, snake: Snake, *args, **kwargs):
        self.active_time -= Share.clock.get_time() / 1000
        if self.active_time <= 0:
            self.active_time = 0
            self.remove_runtime_overriding(snake, 'handle_speed_boost', 'before', self.speed_potion)
            # self.remove_runtime_overriding()
        
        snake.base_stats.speed = int(self.last_speed * 1.5)
        return args, kwargs
    
    def get_item_entity_class(self):
        return SpeedPotionEntity

class SpeedPotionEntity(ItemEntity):
    def __init__(self, level, area: Rect | None = None, r=2, quantity=1):
        super().__init__(level, SPEED_BOOT_TYPE, area, r, quantity)

    def to_item_stack(self):
        return SpeedPotionStack(self.quantity)
