from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity

FIRE_GEM_AMULET = ItemType(
    id = 'fire_gem_amulet',
    name= 'Fire Gem Amulet',
    category=ItemCategory.EQUIPMENT,
    rarity=Rarity.COMMON,
    texture=ItemTexture(
        constant.Texture.fire_gem
    ),
    description="Boost the size, duration and power of fire (Fire Gem Amulet excluded)",
)

class FireGemAmuletStack(ItemStack):
    def __init__(self):
        super().__init__(FIRE_GEM_AMULET, 1)
        self.fire_list = []

    def apply_effect(self, snake):
        self.add_runtime_overriding(snake, 'update', 'before', self.boost_fire)

    def boost_fire(self, snake,*args, **kwargs):
        for fire in snake.level.fire_group.sprites():
            if fire not in self.fire_list:
                self.fire_list.append(fire)
                fire.width_tile +=1
                fire.height_tile +=1
                fire.damage += 0.5
                fire.burn_time += 2
        return args, kwargs
    
    def remove_effect(self, snake):
        for fire in snake.level.fire_group.sprites():
            fire.width_tile -=1
            fire.height_tile -=1
        self.remove_runtime_overriding(snake, 'update', 'before', self.boost_fire)
        
    def get_item_entity_class(self):
        return FireGemAmuletEntity
    
class FireGemAmuletEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, FIRE_GEM_AMULET, area, r, quantity)
    
    def to_item_stack(self):
        return FireGemAmuletStack()