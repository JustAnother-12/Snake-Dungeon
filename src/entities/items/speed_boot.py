from pygame import Rect
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share
from stats import Stats


SPEED_BOOT_TYPE = ItemType(
    'speed_boot',
    'Speed boot',
    ItemCategory.CONSUMABLE,
    Rarity.COMMON,
    ItemTexture(
        'game-assets/graphics/pixil/STATS_ICON_SHEET.pixil',
        0
    ),
    max_stack=5,
    cooldown=5.0
)

class SpeedBootStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(SPEED_BOOT_TYPE, quantity)
        self.active_duration = 3
        self.active_time = 0
        self.last_speed = 0
        
    def apply_effect(self, snake):
        self.active_time = self.active_duration

        self.last_speed = snake.base_stats.speed

        self.add_runtime_overriding(snake, 'handle_speed_boost', 'before', self.speed_boot)
    
    def speed_boot(self, snake: Snake, *args, **kwargs):
        if time.time() - self.active_time > 3:
            self.remove_runtime_overriding(snake, 'handle_speed_boost', 'after', self.speed_boot)
            # self.remove_runtime_overriding()
        
        snake.base_stats.speed = self.last_speed * 2
        return args, kwargs
    
    def get_item_entity_class(self):
        return SpeedBootEntity

class SpeedBootEntity(ItemEntity):
    def __init__(self, level, area: Rect | None = None, r=2, quantity=1):
        super().__init__(level, SPEED_BOOT_TYPE, area, r, quantity)

    def to_item_stack(self):
        return SpeedBootStack(self.quantity)
