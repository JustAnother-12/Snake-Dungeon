from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share


FOOD_TYPE = ItemType(
    'coin', 
    'Coin', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.apple,
    ),
    "helps you grow",
    activation_type=ActivationType.ON_COLLISION
)

class FoodEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, FOOD_TYPE, area, r, quantity)
        self.eaten_by = self.level.snake
    
    def apply_instant_effect(self):
        Share.audio.play_sound("eat")
        self.eaten_by.grow_up(self.quantity) # type: ignore

    def update(self):
        if self.level.snake.is_dead:
            return
        if self._is_collision_with_snake() or self._is_collision_with_monster():
            self.on_collision()

    def _is_collision_with_monster(self):
        for snake in self.level.snake_group._sub_group__:
            if snake != self.level.snake:
                if self.rect and len(snake.blocks) > 0 and self.rect.colliderect(snake.blocks[0].rect): # type: ignore
                    self.eaten_by = snake
                    return True
        return False
    