
import pygame
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share
from utils.pixil import Pixil
from config import constant


GHOST_TYPE = ItemType(
    id="ghost_like_body",
    name="Ghost Like Body",
    category=ItemCategory.SKILL,
    rarity=Rarity.COMMON,
    texture=ItemTexture(
        "game-assets/graphics/pixil/item-sprite/GHOST_LIKE_BODY.pixil",
        0,
    ),
    cooldown=7.0,
    description="Temporary invincibility for 3 seconds",
    price=50,
    energy_usage= 30
)

class GhostStack(ItemStack):
    def __init__(self):
        super().__init__(GHOST_TYPE, 1)
        self.active_time = 0
        self.active_duration = 3  # seconds
    
    def apply_effect(self, snake):
        self.active_time = self.active_duration
        snake.stamina -= self.item_type.energy_usage
        snake.headImg = pygame.Surface((constant.TILE_SIZE, constant.TILE_SIZE), pygame.SRCALPHA)
        snake.headImg.fill((255, 255, 255, 80))
        pygame.draw.rect(snake.headImg, (255, 255, 255), (3, 3, 2, 4))
        pygame.draw.rect(snake.headImg, (255, 255, 255), (11, 3, 2, 4))
        for block in snake.blocks:
            self.default_color = block.color
            block.color = pygame.Color(255, 255, 255, 80)
        self.add_runtime_overriding(snake, '_is_collide_with_orther_snake', 'after', self.prevent_damage)
        self.add_runtime_overriding(snake, '_collide_with_active_trap', 'after', self.prevent_damage)
        self.add_runtime_overriding(snake, '_is_collide_with_self', 'after', self.prevent_damage)
        self.add_runtime_overriding(snake, '_is_collide_with_obstacle', 'after', self.prevent_damage)
    
    def use(self, snake: Snake):
        if snake.stamina < self.item_type.energy_usage:
            return False
        return super().use(snake)
    
    def update(self):
        if self.active_time >= 0: 
            self.active_time -= Share.clock.get_time() / 1000
        return super().update() 
    
    def prevent_damage(self, snake, *args, **kwargs):
        if self.active_time <= 0:
            snake.headImg = Pixil.load(constant.Texture.snake_head, 1).frames[0]
            for block in snake.blocks:
                block.color = pygame.Color(self.default_color)
            self.remove_runtime_overriding(snake, '_is_collide_with_orther_snake', 'after', self.prevent_damage)
            self.remove_runtime_overriding(snake, '_collide_with_active_trap', 'after', self.prevent_damage)
            self.remove_runtime_overriding(snake, '_is_collide_with_self', 'after', self.prevent_damage)
            self.remove_runtime_overriding(snake, '_is_collide_with_obstacle', 'after', self.prevent_damage)
            return False 
        else:
            return False
    
    def get_item_entity_class(self):
        return GhostEntity
    

class GhostEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, GHOST_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return GhostStack()

    