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

        # # Customizable on-expire behavior
        # self.on_expire_class = on_expire_class
        # self.on_expire_kwargs = on_expire_kwargs or {}

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
        # if not self.rect or not self.image:
        #     return
        # trail_pos = self.rect.centerx, self.rect.centery
        # self.trail.append(trail_pos)

        # self.rect.x += self.dx
        # self.rect.y += self.dy
        # self.hitbox_rect.center = self.rect.center

        # self.image.fill((0, 0, 0, 0))

        # for i, pos in enumerate(self.trail):
        #     alpha = 0 + (i * self.trail_alpha_step)
        #     rel_x = pos[0] - self.rect.centerx + 50
        #     rel_y = pos[1] - self.rect.centery + 50
        #     pygame.draw.circle(
        #         self.image,
        #         (255, 255, 255, alpha),
        #         (int(rel_x), int(rel_y)),
        #         1 + (i * 0.2),
        #     )

        # pygame.draw.circle(self.image, self.base_color, (50, 50), 4)

        # current_distance = math.hypot(
        #     self.rect.centerx - self.start_pos[0], self.rect.centery - self.start_pos[1]
        # )
        # if (self.handle_collision() 
        #     or current_distance > self.max_range
        #     or self.rect.right < MAP_LEFT+64
        #     or self.rect.left > MAP_RIGHT-64
        #     or self.rect.bottom < MAP_TOP+64
        #     or self.rect.top > MAP_BOTTOM-64
        # ):
        #     # Tạo object khi hết tầm, truyền tham số tự động
        #     self.rect.center = ((self.rect.center[0]//TILE_SIZE)*TILE_SIZE+8,(self.rect.center[1]//TILE_SIZE)*TILE_SIZE+8)
        #     expire_obj = self.on_expire_class(
        #         self.level, self.rect.center, **self.on_expire_kwargs
        #     )

        #     # Tự động thêm vào group nếu có thuộc tính group
        #     if hasattr(self.level, "bomb_group") and isinstance(
        #         expire_obj, Bomb
        #     ):
        #         self.level.bomb_group.add(expire_obj)
        #     if hasattr(self.level, "fire_group") and isinstance(
        #         expire_obj, Fire_Tile
        #     ):
        #         Share.audio.set_sound_volume("short-fire-burst", 0.5)
        #         Share.audio.play_sound("short-fire-burst")
        #         self.level.fire_group.add(expire_obj)

        #     self.kill()
        pass
            
