from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity

MIDAS_BLOOD = ItemType(
    id = 'midas_blood',
    name= 'Midas Blood',
    category=ItemCategory.EQUIPMENT,
    rarity=Rarity.UNCOMMON,
    texture=ItemTexture(
        constant.Texture.midas_blood
    ),
    description="Severed body parts turns in to 6-8 coins",
)

class MidasBloodStack(ItemStack):
    def __init__(self):
        super().__init__(MIDAS_BLOOD, 1)

    def apply_effect(self, snake):
        self.add_runtime_overriding(snake, 'split', 'before', self.effect)
        
    def effect(self, snake, *args, **kwargs):
        kwargs['transform_type'] = 'COIN'
        kwargs['delay'] = 0.5
        return args, kwargs

    def remove_effect(self, snake):
        self.remove_runtime_overriding(snake, 'split', 'before', self.effect)
        
    def get_item_entity_class(self):
        return MidasBloodEntity
    
class MidasBloodEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, MIDAS_BLOOD, area, r, quantity)
    
    def to_item_stack(self):
        return MidasBloodStack()