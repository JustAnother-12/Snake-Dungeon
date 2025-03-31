

import math
import random
import pygame

from config import constant
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory
import levels.level
from ui.screens.item_info_popup import ItemInfoPopup
from utils import pixil


class ItemEntity(pygame.sprite.Sprite):
    from entities.items.item_type import ItemType
    def __init__(self, level: "levels.level.Level", item_type: ItemType, area: pygame.Rect | None = None, r=2, quantity=1):
        super().__init__()
        self.level = level
        self.item_type = item_type
        self.quantity = quantity
        self._image = pixil.Pixil.load(item_type.texture.pixil_path, item_type.texture.scale).frames[item_type.texture.frame]
        self.image = self._image.copy()
        self.random_pos(area, r)
        self.rect = self.image.get_rect(topleft=self.pos)
        
        
        # Interaction properties
        self.interaction_radius = constant.TILE_SIZE * 2  # 2 tiles radius
        self.in_range = False  # Is snake in range?
        self.highlight_effect = None  # Visual effect when in range
        self.pulse_animation = 0  # For pulsing effect
        self.create_highlight_effect()
    
    def create_highlight_effect(self):
        """Create a highlight effect for the item"""
        self.highlight_effect = pygame.Surface((
            self.rect.width + 10,  # type: ignore
            self.rect.height + 10 # type: ignore
        ), pygame.SRCALPHA)
        
        # Different colors based on rarity
        if self.item_type.rarity.name == "COMMON":
            color = (255, 255, 255, 100)  # White
        elif self.item_type.rarity.name == "UNCOMMON":
            color = (0, 255, 0, 100)  # Green
        elif self.item_type.rarity.name == "RARE":
            color = (0, 0, 255, 100)  # Blue
        elif self.item_type.rarity.name == "EPIC":
            color = (128, 0, 128, 100)  # Purple
        else:
            color = (255, 215, 0, 100)  # Gold
            
        pygame.draw.rect(
            self.highlight_effect, 
            color, 
            (0, 0, self.highlight_effect.get_width(), self.highlight_effect.get_height()),
            border_radius=5
        )    

    def random_pos(self, area: pygame.Rect | None, r = 2):
        if not area:
            self.pos = pygame.Vector2(
                random.randint(
                    constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                    (
                        constant.SCREEN_WIDTH_TILES
                        - constant.LEFT_RIGHT_BORDER_TILES
                        - constant.WALL_TILES
                    ),
                )
                * constant.TILE_SIZE,
                random.randint(
                    constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                    (
                        constant.SCREEN_HEIGHT_TILES
                        - constant.TOP_BOTTOM_BORDER_TILES
                        - constant.WALL_TILES
                    ),
                )
                * constant.TILE_SIZE,
            )
        else:
            R = int(r * constant.TILE_SIZE)
            x = random.randint(
                area.centerx - R - area.width // 2,
                area.centerx + R + area.width // 2,
            )
            if (
                x < area.centerx - area.width // 2
                or x > area.centerx + area.width // 2
            ):
                y = random.randint(
                    area.centery - R - area.height // 2,
                    area.centery + R + area.height // 2,
                )
            else:
                y = random.choice(
                    [
                        random.randint(
                            area.centery - R - area.height // 2,
                            area.centery - area.height // 2,
                        ),
                        random.randint(
                            area.centery + area.height // 2,
                            area.centery + R + area.height // 2,
                        ),
                    ]
                )
            self.pos = pygame.Vector2(x, y)
            if (
                x < (constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES) * constant.TILE_SIZE + 4
                or x > (constant.SCREEN_WIDTH_TILES - constant.LEFT_RIGHT_BORDER_TILES - constant.WALL_TILES) * constant.TILE_SIZE - 4
                or y < (constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES) * constant.TILE_SIZE + 4
                or y > (constant.SCREEN_HEIGHT_TILES - constant.TOP_BOTTOM_BORDER_TILES - constant.WALL_TILES) * constant.TILE_SIZE - 4
            ):
                self.random_pos(area)
    
    def on_collision(self):
        """Xử lý khi va chạm với rắn"""
        if self.item_type.category == ItemCategory.INSTANT:
            # Item tức thời (coin, food) - áp dụng hiệu ứng ngay
            self.apply_instant_effect()
        else:
            # Các item khác - thêm vào inventory
            item_stack = self.to_item_stack()
            added = self.level.snake.add_item(item_stack)
            if not added:
                # Nếu inventory đầy, có thể hiển thị thông báo
                pass
        
        self.kill()
    
    def apply_instant_effect(self):
        """Áp dụng hiệu ứng tức thời - ghi đè trong lớp con"""
        pass
    
    def to_item_stack(self):
        """Chuyển đổi thành ItemStack khi được nhặt"""
        return ItemStack(self.item_type, self.quantity)
    
    def update(self):
        """Update item state"""
        # For INSTANT items, use collision detection
        if self.item_type.category == ItemCategory.INSTANT:
            if pygame.sprite.spritecollideany(self, self.level.snake.blocks): # type: ignore
                self.on_collision()
            return
        
        # For other items, check if in interaction range
        head_pos = self.level.snake.blocks[0].rect.center
        distance = pygame.math.Vector2(head_pos).distance_to(
            pygame.math.Vector2(self.rect.center) # type: ignore
        )
        
        # Check if snake is in range
        was_in_range = self.in_range
        self.in_range = distance <= self.interaction_radius
        
        # Just entered range - add to interaction manager
        if self.in_range and not was_in_range:
            self.level.interaction_manager.register_interact(self)
            
        # Just left range - remove from interaction manager
        elif not self.in_range and was_in_range:
            self.level.interaction_manager.unregister_interact(self)
            
        # Animate highlight effect
        self.pulse_animation = (self.pulse_animation + 0.05) % (2 * 3.14159)

        self.update_img()

    def update_img(self):
        # Draw the item itself
        self.image = self._image.copy()
        
        # Draw highlight effect if in range
        if self.in_range:
            # Pulsing effect
            alpha = int(100 + 50 * abs(math.sin(self.pulse_animation)))
            self.highlight_effect.set_alpha(alpha) # type: ignore
            
            # Position highlight behind item
            highlight_rect = self.highlight_effect.get_rect(center=self._image.get_rect().center) # type: ignore
            self.image.blit(self.highlight_effect, highlight_rect) # type: ignore
    
    def on_pickup(self):
        """Called when player picks up the item"""
        pass
        # TODO: hiển thị thông popup 
        self.level.game.state_stack.append(ItemInfoPopup(self.level, self))
        # print("aloooo")