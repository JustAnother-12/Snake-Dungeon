import pygame
from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from levels.components.bomb import Bomb, BombState
from entities.throw_projectile import Throw_projectile
from levels.components.fire_bomb import FireBomb
from utils.help import Share


FIRE_BOMB_TYPE = ItemType(
    'fire_bomb',
    'Fire Bomb',
    ItemCategory.CONSUMABLE,
    Rarity.UNCOMMON,
    ItemTexture(
        constant.Texture.fire_bomb,
        0
    ),
    'A clay orb packed with oil-soaked rags and sulfur .Upon detonate, makes a small explosion, then create a small fire hazard that last for 4s, 17s cooldown',
    max_stack=10,
    cooldown=17.0
)

class FireBombStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(FIRE_BOMB_TYPE, quantity)

    def apply_effect(self, snake):
        mouse_pos = pygame.mouse.get_pos()
        projectile = Throw_projectile(
                                    snake.level,
                                    snake.blocks[0].rect.x, 
                                    snake.blocks[0].rect.y, mouse_pos[0],
                                    mouse_pos[1], 
                                    'white', 
                                    8*constant.TILE_SIZE, 
                                    5,
                                    4,
                                    on_expire_class=FireBomb
                                    )
        snake.level.add(projectile)
        Share.audio.set_sound_volume("throw", 0.45)
        Share.audio.play_sound("throw")

        
    def get_item_entity_class(self):
        return FireBombEntity


class FireBombEntity(ItemEntity):
    def __init__(self, level, area = None, r=2, quantity=1):
        super().__init__(level, FIRE_BOMB_TYPE, area, r, quantity)

    def to_item_stack(self):
        return FireBombStack(self.quantity)