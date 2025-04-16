from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity

CREDIT_CARD = ItemType(
    id = 'credit_card',
    name= 'Credit Card',
    category=ItemCategory.EQUIPMENT,
    rarity=Rarity.COMMON,
    texture=ItemTexture(
        constant.Texture.credit_card
    ),
    description="Provides 30% discount in the shop",
)

class CreditCardStack(ItemStack):
    def __init__(self):
        super().__init__(CREDIT_CARD, 1)
        self.fire_list = []

    def apply_effect(self, snake):
        self.add_runtime_overriding(snake, 'update', 'before', self.discount)

    def discount(self, snake,*args, **kwargs):
        for itemEntity in snake.level.item_group.sprites():
            itemEntity.item_type.sale = 70
        return args, kwargs
    
    def remove_effect(self, snake):
        for itemEntity in snake.level.item_group.sprites():
            itemEntity.item_type.sale = 100
        self.remove_runtime_overriding(snake, 'update', 'before', self.discount)
        
    def get_item_entity_class(self):
        return CreditCardEntity
    
class CreditCardEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, CREDIT_CARD, area, r, quantity)
    
    def to_item_stack(self):
        return CreditCardStack()