import pygame
import math
from collections import deque
from config.constant import MAP_TOP, MAP_BOTTOM, MAP_LEFT, MAP_RIGHT
from levels.components.bomb import Bomb
from levels.components.fire_tile import Fire_Tile


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
        on_expire_class, # Class được tạo khi va chạm hoặc hết tầm
        on_expire_kwargs=None,
    ) -> None:
        super().__init__()
        self.level = level
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.base_color = color
        pygame.draw.circle(self.image, color, (50, 50), 5)  
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.speed = speed
        self.start_pos = (x_pos, y_pos)
        self.max_range = max_range

        # Customizable on-expire behavior
        self.on_expire_class = on_expire_class
        self.on_expire_kwargs = on_expire_kwargs or {}

        # Trail setup
        self.trail = deque(maxlen=20)
        self.trail_alpha_step = 255 // 50

        dx = target_x - x_pos
        dy = target_y - y_pos
        distance = math.hypot(dx, dy)
        self.dx = dx / distance * speed if distance != 0 else 0
        self.dy = dy / distance * speed if distance != 0 else 0

    def update(self):
        if not self.rect or not self.image:
            return
        trail_pos = self.rect.centerx, self.rect.centery
        self.trail.append(trail_pos)

        self.rect.x += self.dx
        self.rect.y += self.dy

        self.image.fill((0, 0, 0, 0))

        for i, pos in enumerate(self.trail):
            alpha = 0 + (i * self.trail_alpha_step)
            rel_x = pos[0] - self.rect.centerx + 50
            rel_y = pos[1] - self.rect.centery + 50
            pygame.draw.circle(
                self.image,
                (255, 255, 255, alpha),
                (int(rel_x), int(rel_y)),
                1 + (i * 0.2),
            )

        pygame.draw.circle(self.image, self.base_color, (50, 50), 4)

        current_distance = math.hypot(
            self.rect.centerx - self.start_pos[0], self.rect.centery - self.start_pos[1]
        )

        if (
            current_distance > self.max_range
            or self.rect.right < MAP_LEFT
            or self.rect.left > MAP_RIGHT
            or self.rect.bottom < MAP_TOP
            or self.rect.top > MAP_BOTTOM
        ):

            # Tạo object khi hết tầm, truyền tham số tự động
            expire_obj = self.on_expire_class(
                self.level, self.rect.center, **self.on_expire_kwargs
            )

            # Tự động thêm vào group nếu có thuộc tính group
            if hasattr(self.level, "bomb_group") and isinstance(
                expire_obj, Bomb
            ):
                self.level.bomb_group.add(expire_obj)
            if hasattr(self.level, "fire_group") and isinstance(
                expire_obj, Fire_Tile
            ):
                self.level.fire_group.add(expire_obj)

            self.kill()
