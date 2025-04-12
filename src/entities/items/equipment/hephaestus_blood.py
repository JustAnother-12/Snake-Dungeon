from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity

HEPHAESTUS_BLOOD = ItemType(
    id = 'hephaestus_blood',
    name= 'Hephaestus Blood',
    category=ItemCategory.EQUIPMENT,
    rarity=Rarity.UNCOMMON,
    texture=ItemTexture(
        constant.Texture.hephaestus_blood
    ),
    description="Severed body parts burst in to flames that last for 5s",
)

class HephaestusBloodStack(ItemStack):
    def __init__(self):
        super().__init__(HEPHAESTUS_BLOOD, 1)

    def apply_effect(self, snake):
        self.add_runtime_overriding(snake, 'split', 'before', self.effect)
        
    def effect(self, snake, *args, **kwargs):
        kwargs['transform_type'] = 'FIRE'
        kwargs['delay'] = 0.5
        return args, kwargs

    def remove_effect(self, snake):
        self.remove_runtime_overriding(snake, 'split', 'before', self.effect)
        
    def get_item_entity_class(self):
        return HephaestusBloodEntity
    
class HephaestusBloodEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, HEPHAESTUS_BLOOD, area, r, quantity)
    
    def to_item_stack(self):
        return HephaestusBloodStack()