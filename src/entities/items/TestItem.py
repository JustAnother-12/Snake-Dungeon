
from time import time
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity


SHIELD_TYPE = ItemType(
    id="shield",
    name="Shield",
    category=ItemCategory.EQUIPMENT,
    rarity=Rarity.RARE,
    texture=ItemTexture(
        "game-assets/graphics/pixil/SHIELD.pixil",
    ),
    cooldown=15.0,
    description="Temporary invincibility for 3 seconds",
    price=150  # Shield is valuable!
)

class ShieldStack(ItemStack):
    def __init__(self):
        super().__init__(SHIELD_TYPE, 1)
        self.shield_active = False
        self.shield_end_time = 0
    
    def apply_effect(self, snake):
        self.shield_active = False
        self.shield_end_time = time() + 3
        
        # if '_is_collide_with_Obstacle' not in snake.run_time_overriding:
        #     snake.run_time_overriding['_is_collide_with_Obstacle'] = {
        #         "after": [],
        #         "return" : [],
        #         "before" : []
        #     }
        
        # snake.run_time_overriding['_is_collide_with_Obstacle']['after'].append(self.prevent_damage)
        self.add_runtime_overriding(snake, '_is_collide_with_Obstacle', 'after', self.prevent_damage)
    
    def prevent_damage(self, snake, *args, **kwargs):
        if time() < self.shield_end_time:
            snake._will_go_out_of_bounds = False
            return False 
        else:
            self.remove_runtime_overriding(snake, '_is_collide_with_Obstacle', 'after', self.prevent_damage)
            return False
    
    def get_item_entity_class(self):
        return ShieldEntity
    

class ShieldEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, SHIELD_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return ShieldStack()

    