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
    description="Gives 20% of player's total gold at the end of a level",
)

class CreditCardStack(ItemStack):
    def __init__(self):
        super().__init__(CREDIT_CARD, 1)
        self.is_payed = 0

    def apply_effect(self, snake):
        self.add_runtime_overriding(snake, 'update', 'before', self.payment)

    def payment(self,snake,*args, **kwargs):
        from levels.level import LevelStatus

        current_total_gold = snake.gold
        if snake.level.level_status == LevelStatus.PLAYING:
            self.is_payed = 0
        
        if snake.level.level_status == LevelStatus.ROOM_COMPLETED and self.is_payed == 0:
            self.is_payed = 1
            snake.gold+= (int)(current_total_gold*0.2)
        return args, kwargs
    
    def remove_effect(self, snake):
        self.remove_runtime_overriding(snake, 'update', 'before', self.payment)
        
    def get_item_entity_class(self):
        return CreditCardEntity
    
class CreditCardEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, CREDIT_CARD, area, r, quantity)
    
    def to_item_stack(self):
        return CreditCardStack()