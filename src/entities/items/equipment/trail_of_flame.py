from pygame import KEYDOWN, Rect, Vector2
import pygame
from config import constant
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from levels.components.fire_tile import Fire_Tile
from utils.help import Share


TRAIL_OF_FLAME = ItemType(
    'trail_of_flame',
    'Trail of Flame',
    ItemCategory.EQUIPMENT,
    Rarity.UNCOMMON,
    ItemTexture(
        constant.Texture.trail_of_flame,
        0
    ),
    description="If Length is lesser than 7 then upon boosting, the player creates a trail of fire",
)

class FlameTrailStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(TRAIL_OF_FLAME, quantity)
        self.last_fire_pos = Vector2(0, 0)
        
    def apply_effect(self, snake):
        self.add_runtime_overriding(snake, 'handle_speed_boost', 'after', self.flame_trail)
    
    def flame_trail(self, snake: Snake, *args, **kwargs):
        Share.audio.set_sound_volume("short-fire-burst", 0.6)
        keys = pygame.key.get_pressed()
        
        # Initialize flag if not present
        if not hasattr(self, "_space_held"):
            self._space_held = False

        if keys[pygame.K_SPACE] and len(snake.blocks) < 7:
            if not self._space_held:
                Share.audio.play_sound("short-fire-burst")
                self._space_held = True
        elif not keys[pygame.K_SPACE]:
            self._space_held = False

        if snake.is_speed_boost and len(snake.blocks) < 7:
            if snake.stamina > 0:
                new_pos = snake.blocks[-1].pos // constant.TILE_SIZE * constant.TILE_SIZE + (8, 8)
                if self.last_fire_pos != new_pos:
                    self.last_fire_pos = new_pos
                    fire = Fire_Tile(snake.level, new_pos, 1, 1, 3)
                    snake.level.fire_group.add(fire)
        
    def remove_effect(self, snake):
        self.remove_runtime_overriding(snake, 'update', 'after', self.flame_trail)
    
    def get_item_entity_class(self):
        return FlameTrailEntity

class FlameTrailEntity(ItemEntity):
    def __init__(self, level, area: Rect | None = None, r=2, quantity=1):
        super().__init__(level, TRAIL_OF_FLAME, area, r, quantity)

    def to_item_stack(self):
        return FlameTrailStack(self.quantity)