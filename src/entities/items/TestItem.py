
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share


SHIELD_TYPE = ItemType(
    id="shield",
    name="Shield",
    category=ItemCategory.SKILL,
    rarity=Rarity.RARE,
    texture=ItemTexture(
        "game-assets/graphics/pixil/SHIELD.pixil",
    ),
    cooldown=15.0,
    description="Temporary invincibility for 3 seconds",
    price=150,  # Shield is valuable!
    energy_usage= 30
)

class ShieldStack(ItemStack):
    def __init__(self):
        super().__init__(SHIELD_TYPE, 1)
        self.shield_active_time = 0
        self.shield_active_duration = 3  # seconds
    
    def apply_effect(self, snake):
        self.shield_active_time = self.shield_active_duration
        snake.stamina -= self.item_type.energy_usage
        
        # snake.run_time_overriding['_is_collide_with_Obstacle']['after'].append(self.prevent_damage)
        self.add_runtime_overriding(snake, '_is_collide_with_obstacle', 'after', self.prevent_damage)
    
    def use(self, snake: Snake):
        if snake.stamina < self.item_type.energy_usage:
            return False
        return super().use(snake)
    
    def update(self):
        if self.shield_active_time >= 0: 
            self.shield_active_time -= Share.clock.get_time() / 1000
        return super().update()
    
    def prevent_damage(self, snake, *args, **kwargs):
        if self.shield_active_time <= 0:
            print("Shield expired")
            self.remove_runtime_overriding(snake, '_is_collide_with_obstacle', 'after', self.prevent_damage)
            return False 
        else:
            snake._will_go_out_of_bounds = False
            return False
    
    def get_item_entity_class(self):
        return ShieldEntity
    

class ShieldEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, SHIELD_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return ShieldStack()

    