import pygame
from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from levels.components.bomb import Bomb, BombState
from entities.projectile import Projectile


BOMB_TYPE = ItemType(
    'bomb',
    'Bomb',
    ItemCategory.CONSUMABLE,
    Rarity.COMMON,
    ItemTexture(
        'game-assets/graphics/pixil/item-sprite/BOMB_ITEM.pixil',
        0
    ),
    max_stack=10,
    cooldown=3.0
)

class BombStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(BOMB_TYPE, quantity)

    def apply_effect(self, snake):
        mouse_pos = pygame.mouse.get_pos()
        projectile = Projectile(snake.level,
                                snake.blocks[0].rect.x, 
                                snake.blocks[0].rect.y, mouse_pos[0],
                                  mouse_pos[1], 
                                  'white', 
                                  8*constant.TILE_SIZE, 
                                  5)
        snake.level.add(projectile)
        # projectile.draw_trail()

    
    def get_item_entity_class(self):
        return BombEntity


class BombEntity(ItemEntity):
    def __init__(self, level, area = None, r=2, quantity=1):
        super().__init__(level, BOMB_TYPE, area, r, quantity)

    def to_item_stack(self):
        return BombStack(self.quantity)