

from pygame import Rect
import pygame
from config import constant
from config.constant import Texture
from entities.Player import Snake
from entities.bullet_projectile import Bullet_projectile
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share


GUN_CONSTRACT = ItemType(
    id = "gun_devil_contract",
    name = "Gun Devil's Contract",
    category=ItemCategory.SKILL,
    rarity=Rarity.RARE,
    texture=ItemTexture(
        constant.Texture.hand_gun
    ),
    cooldown=10.0,
    description="Upon activation, the Player loses 1 body part to fires a bullet at the cursor position. The bullet kills anything on contact. Consumes 80 Energy, 10s cooldown",
    energy_usage=80
)

class GunStack(ItemStack):
    def __init__(self):
        super().__init__(GUN_CONSTRACT, 1)
        self.wait = Share.clock.get_time()/1000

    def apply_effect(self, snake: Snake):
        Share.audio.play_sound("body_part_cutoff")
        block = snake.blocks.pop()
        block.kill()
        # if Share.clock.get_time()/1000 - self.wait >= 0.5: 
        mouse_pos = pygame.mouse.get_pos()
        projectile = Bullet_projectile(
                                    snake.level,
                                    snake.blocks[0].rect.x, 
                                    snake.blocks[0].rect.y, 
                                    mouse_pos[0],
                                    mouse_pos[1], 
                                    'yellow', 
                                    20*constant.TILE_SIZE, 
                                    10,
                                    3,
                                    max_pierce=4
                                    )
        snake.level.add(projectile)
        Share.audio.play_sound("gun-shot")

    def use(self, snake: Snake):
        return super().use(snake)
    
    def get_item_entity_class(self):
        return GunEntity
    
class GunEntity(ItemEntity):
    def __init__(self, level, area: Rect | None = None, r=2, quantity=1):
        super().__init__(level, GUN_CONSTRACT, area, r, quantity)

    def to_item_stack(self):
        return GunStack()