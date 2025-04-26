import pygame
import math
from config.constant import TILE_SIZE
from entities.projectile import Projectile
from levels.components.bomb import Bomb
from levels.components.fire_bomb import FireBomb
from levels.components.fire_tile import Fire_Tile
from utils.help import Share

class Throw_projectile(Projectile):
    def __init__(self, level, x_pos, y_pos, target_x, target_y, color, max_range, speed,size, on_expire_class, on_expire_kwargs=None) -> None:
        super().__init__(level, x_pos, y_pos, target_x, target_y, color, max_range, speed, size)

        Share.audio.set_sound_volume("throw", 0.45)
        Share.audio.play_sound("throw")
        # Customizable on-expire behavior
        self.on_expire_class = on_expire_class
        self.on_expire_kwargs = on_expire_kwargs or {}

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
                return True
        return False

    def update(self):
        if not self.rect or not self.image:
            return
        trail_pos = self.rect.centerx, self.rect.centery
        self.trail.append(trail_pos)

        self.rect.x += self.dx
        self.rect.y += self.dy
        self.hitbox_rect.center = self.rect.center

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
        if (self.handle_enemy_collision() 
            or current_distance > self.max_range
            or self.handle_wall_collision()
        ):
            # Tạo object khi hết tầm, truyền tham số tự động
            self.rect.center = ((self.rect.center[0]//TILE_SIZE)*TILE_SIZE+8,(self.rect.center[1]//TILE_SIZE)*TILE_SIZE+8)
            expire_obj = self.on_expire_class(
                self.level, self.rect.center, **self.on_expire_kwargs
            )

            # Tự động thêm vào group nếu có thuộc tính group
            if hasattr(self.level, "bomb_group"):
                if isinstance(expire_obj, Bomb):
                    self.level.bomb_group.add(expire_obj)
                elif isinstance(expire_obj, FireBomb):
                    self.level.fire_bomb_group.add(expire_obj)
            if hasattr(self.level, "fire_group") and isinstance(
                expire_obj, Fire_Tile
            ):  
                Share.audio.set_sound_volume("glass-break", 0.5)
                Share.audio.play_sound("glass-break")
                Share.audio.set_sound_volume("short-fire-burst", 0.5)
                Share.audio.play_sound("short-fire-burst")
                self.level.fire_group.add(expire_obj)

            self.kill()
