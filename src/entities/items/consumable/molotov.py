
import pygame
from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from entities.throw_projectile import Throw_projectile
from levels.components.fire_tile import Fire_Tile


MOLOTOV_TYPE = ItemType(
    'molotov',
    "Molotov",
    ItemCategory.CONSUMABLE,
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.molotov
    ),
    'Makes a small fire hazard that last for 7s, 12s cooldown',
    max_stack=5,
    cooldown=12.0,
)

class MolotovStack(ItemStack):
    def __init__(self, quantity: int = 1) -> None:
        super().__init__(MOLOTOV_TYPE, quantity)
        
    def apply_effect(self, snake):
        mouse_pos = pygame.mouse.get_pos()
        projectile = Throw_projectile(
                                    snake.level,
                                    snake.blocks[0].rect.x, 
                                    snake.blocks[0].rect.y, 
                                    mouse_pos[0],
                                    mouse_pos[1], 
                                    'white', 
                                    8*constant.TILE_SIZE, 
                                    5,
                                    4,
                                    on_expire_class=Fire_Tile,
                                    on_expire_kwargs={'width_tile': 3, 'height_tile': 3, 'burn_time': 7}
                                    )
        snake.level.add(projectile)

    def get_item_entity_class(self):
        return MolotovEntity
    
class MolotovEntity(ItemEntity):
    def __init__(self, level, area = None, r = 2, quantity=1) -> None:
        super().__init__(level, MOLOTOV_TYPE, area, r, quantity)
        
    def to_item_stack(self):
        return MolotovStack(self.quantity)