


from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity


BLOOD_BOMB_DEVIL = ItemType(
    id="blood_bomb_devil",
    name="Blood of the Bomb Devil",
    category=ItemCategory.EQUIPMENT,
    rarity=Rarity.RARE,
    texture=ItemTexture(
        constant.Texture.bomb_devil_blood,
    ),
    description="Severed body parts turns into a bomb"
)

class BloodBombDevilStack(ItemStack):
    def __init__(self):
        super().__init__(BLOOD_BOMB_DEVIL, 1)

    def apply_effect(self, snake):
        self.add_runtime_overriding(snake, 'split', 'before', self.effect)
        
    def effect(self, snake, *args, **kwargs):
        kwargs['transform_type'] = 'BOMB'
        return args, kwargs

    def remove_effect(self, snake):
        self.remove_runtime_overriding(snake, 'split', 'before', self.effect)
        
    def get_item_entity_class(self):
        return BloodBombDevilEntity
    
class BloodBombDevilEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, BLOOD_BOMB_DEVIL, area, r, quantity)
    
    def to_item_stack(self):
        return BloodBombDevilStack()