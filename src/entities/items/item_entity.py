import math
import random
import pygame

from config import constant
from entities.items.item_stack import ItemStack
from entities.items.item_type import ActivationType
from systems.interaction_manager import InteractionObject
from ui.screens.item_info_popup import ItemInfoPopup
from utils import pixil


class ItemEntity(InteractionObject):
    from entities.items.item_type import ItemType
    def __init__(self, level, item_type: ItemType, area: pygame.Rect | None = None, r=2, quantity=1):
        super().__init__(level, "pickup "+item_type.name, constant.TILE_SIZE * 2)
        self.level = level
        self.item_type = item_type
        self.quantity = quantity
        self._image = pixil.Pixil.load(item_type.texture.pixil_path, item_type.texture.scale).frames[item_type.texture.entity_frame]
        self.image = self._image.copy()
        self.random_pos(area, r)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.shop_item = False 
        
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
        else:
            color = (255, 215, 0, 100)  # Gold
            
        pygame.draw.rect(
            self.highlight_effect, 
            color, 
            (0, 0, self.highlight_effect.get_width(), self.highlight_effect.get_height()),
            border_radius=5
        )

    def random_pos(self, area: pygame.Rect | None, r = 2):

        # Random position theo grid
        if not area:
            self.pos = pygame.Vector2(
                random.randint(
                    constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                    (
                        constant.SCREEN_WIDTH_TILES
                        - constant.LEFT_RIGHT_BORDER_TILES
                        - constant.WALL_TILES
                        - math.ceil(self.image.get_width()/constant.TILE_SIZE ) if self.image else 0
                    ),
                )
                * constant.TILE_SIZE,
                random.randint(
                    constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                    (
                        constant.SCREEN_HEIGHT_TILES
                        - constant.TOP_BOTTOM_BORDER_TILES
                        - constant.WALL_TILES
                        - math.ceil(self.image.get_height()/constant.TILE_SIZE ) if self.image else 0
                    ),
                )
                * constant.TILE_SIZE,
            )
        # Random position trong area đã cho
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
        if not self.check_pos(self.image):
            return self.random_pos(area, r)

    def check_pos(self, image):
        """Kiểm tra vị trí item có hợp lệ không"""
        try:
            if self.pos.x < constant.MAP_LEFT or self.pos.x > constant.MAP_RIGHT - image.get_width() or self.pos.y < constant.MAP_TOP or self.pos.y > constant.MAP_BOTTOM - image.get_height():
                return False
            for sprite in self.level.obstacle_group.sprites():
                if sprite.rect.colliderect(pygame.Rect(self.pos.x, self.pos.y, image.get_width(), image.get_height())):
                    return False
            
            return True
        except Exception as e:
            return True
    
    def on_collision(self):
        """Xử lý khi va chạm với rắn"""
        self.apply_instant_effect()
        self.kill()
    
    def apply_instant_effect(self):
        """Áp dụng hiệu ứng tức thời - ghi đè trong lớp con"""
        pass
    
    def to_item_stack(self):
        """Chuyển đổi thành ItemStack khi được nhặt"""
        return ItemStack(self.item_type, self.quantity)
    
    def update(self):
        """Update item state"""
        
        # Không add vào inventory nếu item là ON_COLLISION
        if self.item_type.activation_type == ActivationType.ON_COLLISION:
            if self._is_collision_with_snake():
                self.on_collision()
            return
        
        super().update()
            
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
        self.level.game.state_stack.append(ItemInfoPopup(self.level, self))

    def on_interact(self):
        self.on_pickup()

    def _is_collision_with_snake(self):
        return self.rect and len(self.level.snake.blocks) > 0 and self.rect.colliderect(self.level.snake.blocks[0].rect)