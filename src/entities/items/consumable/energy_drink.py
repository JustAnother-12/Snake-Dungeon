from pygame import Rect
from config import constant
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share
from stats import Stats


ENERGY_DRINK_TYPE = ItemType(
    'energy_drink',
    'Speed Potion',
    ItemCategory.CONSUMABLE,
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.energy_drink,
        0
    ),
    description="gives energy regeneration boost for 10s, 20s cooldown",
    max_stack=5,
    cooldown=20
)

class EnergyDrinkStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(ENERGY_DRINK_TYPE, quantity)
        self.active_duration = 10
        self.active_time = 0
        self.energy_regen = 0
        
    def apply_effect(self, snake):
        self.active_time = self.active_duration

        self.energy_regen = snake.base_stats.energy_regen

        self.add_runtime_overriding(snake, 'handle_speed_boost', 'before', self.boost_energy_regen)
    
    def boost_energy_regen(self, snake: Snake, *args, **kwargs):
        self.active_time -= Share.clock.get_time() / 1000
        if self.active_time <= 0:
            self.active_time = 0
            self.remove_runtime_overriding(snake, 'handle_speed_boost', 'before', self.boost_energy_regen)
            # self.remove_runtime_overriding()
        
        snake.base_stats.energy_regen = self.energy_regen * 1.5
        return args, kwargs
    
    def get_item_entity_class(self):
        return EnergyDrinkEntity

class EnergyDrinkEntity(ItemEntity):
    def __init__(self, level, area: Rect | None = None, r=2, quantity=1):
        super().__init__(level, ENERGY_DRINK_TYPE, area, r, quantity)

    def to_item_stack(self):
        return EnergyDrinkStack(self.quantity)
