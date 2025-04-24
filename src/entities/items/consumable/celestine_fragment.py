from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share

CELESTINE_FRAGMENT_TYPE = ItemType(
    'celestine_fragment',
    'The Celestine Fragment',
    ItemCategory.CONSUMABLE,
    Rarity.RARE,
    ItemTexture(
        constant.Texture.celestine_fragment
    ),
    description="A small fragment of Celestine. Breaks upon use, then gives the player Powered state. Makes the player invincible and kill everything on contact. Last for 5s and consumes 60 Energy",
    cooldown=5.0,
    energy_usage=60
)

class CelestineFragmentStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(CELESTINE_FRAGMENT_TYPE, quantity)
        self.active_duration = 5
        self.active_time = 0
        self.energy_regen = 0
        self.last_speed = 0
        
    def apply_effect(self, snake):
        self.active_time = self.active_duration
        self.last_speed = snake.base_stats.speed
        self.add_runtime_overriding(snake, '_is_collide_with_orther_snake', 'return', self.kill_moster_when_collide)
        self.add_runtime_overriding(snake, 'handle_collision', 'return', self.disable_collision)
        self.add_runtime_overriding(snake, 'handle_speed_boost', 'before', self.speed_boost)
        
    def disable_collision(self, snake, *args, **kwargs):
        return False
    
    def kill_moster_when_collide(self, snake, *args, **kwargs):
        if self.active_time <= 0:
            self.active_time = 0
            self.remove_effect(snake)
            
        position = snake._block_positions[0]
        for _snake in snake.level.snake_group._sub_group__: # type: ignore
            if _snake == snake: continue
            if _snake.is_dead: continue
            for block in _snake.sprites():
                if block.rect.colliderect(
                    (
                        position[0],
                        position[1],
                        constant.TILE_SIZE,
                        constant.TILE_SIZE,
                    )
                ):
                    _snake.is_dead = True
                    return False
        return False
    
    def speed_boost(self, snake, *args, **kwargs):
        snake.base_stats.speed = int(self.last_speed * 1.5)
        return args, kwargs
    
    def update(self, inventory_manager):
        self.active_time -= (Share.clock.get_time() / 1000)
        return super().update(inventory_manager)
    
    def remove_effect(self, snake):
        self.remove_runtime_overriding(snake, '_is_collide_with_orther_snake', 'return', self.kill_moster_when_collide)
        self.remove_runtime_overriding(snake, 'handle_collision', 'return', self.disable_collision)
        self.remove_runtime_overriding(snake, 'handle_speed_boost', 'before', self.speed_boost)
    
    def get_item_entity_class(self):
        return CelestineFragmentEntity
    
class CelestineFragmentEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, CELESTINE_FRAGMENT_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return CelestineFragmentStack(self.quantity)
        