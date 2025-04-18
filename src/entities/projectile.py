import pygame
import math
from collections import deque
from config.constant import MAP_TOP, MAP_BOTTOM, MAP_LEFT, MAP_RIGHT, TILE_SIZE
from levels.components.bomb import Bomb
from levels.components.fire_tile import Fire_Tile
from utils.help import Share

class Projectile(pygame.sprite.Sprite):
    def __init__(
        self,
        level,
        x_pos,
        y_pos,
        target_x,
        target_y,
        color,
        max_range,
        speed,
        size
    ) -> None:
        super().__init__()
        self.level = level
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.base_color = color
        self.size = size
        pygame.draw.circle(self.image, color, (50, 50), self.size)  
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.hitbox_rect = pygame.Rect(0, 0, self.size*2,self.size*2)
        self.hitbox_rect.center = self.rect.center
        self.speed = speed
        self.start_pos = (x_pos, y_pos)
        self.max_range = max_range
        # Trail setup
        self.trail = deque(maxlen=20)
        self.trail_alpha_step = 255 // 50

        dx = target_x - x_pos
        dy = target_y - y_pos
        distance = math.hypot(dx, dy)
        self.dx = dx / distance * speed if distance != 0 else 0
        self.dy = dy / distance * speed if distance != 0 else 0

    def handle_enemy_collision(self):
        for group in self.level.snake_group._sub_group__:
            if group is self.level.snake:
                continue
            for sprite in group.sprites():
                if self.hitbox_rect.colliderect(sprite.rect):
                    return True
        return False
    
    def handle_wall_collision(self):
        for sprite in self.level.wall_group.sprites():
            if self.hitbox_rect.colliderect(sprite.rect):
                self.kill()
                return True
        return False

    def handle_obstacle_collision(self):
        for sprite in self.level.obstacle_group.sprites():
            if self.hitbox_rect.colliderect(sprite.rect):
                self.kill()
                return True
        return False

    def update(self):
        pass