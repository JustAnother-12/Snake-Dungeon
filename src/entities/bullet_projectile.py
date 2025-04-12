import pygame
import math
from config.constant import MAP_TOP, MAP_BOTTOM, MAP_LEFT, MAP_RIGHT, TILE_SIZE
from entities.projectile import Projectile
from levels.components.bomb import Bomb
from levels.components.fire_tile import Fire_Tile
from utils.help import Share

class Bullet_projectile(Projectile):
    def __init__(self, level, x_pos, y_pos, target_x, target_y, color, max_range, speed, size, max_pierce) -> None:
        super().__init__(level, x_pos, y_pos, target_x, target_y, color, max_range, speed, size)
        self.max_pierce = max_pierce
        self.pierce_count = 0


    def handle_enemy_collision(self):
        for group in self.level.snake_group._sub_group__:
            if group is self.level.snake:
                continue
            for sprite in group.sprites():
                if self.hitbox_rect.colliderect(sprite.rect):
                    self.pierce_count+=1
                    group.is_dead = True
                    return True
        return False
    
    def handle_wall_collision(self):
        for sprite in self.level.wall_group.sprites():
            if self.hitbox_rect.colliderect(sprite.rect):
                self.kill()

    def handle_obstacle_collision(self):
        for sprite in self.level.obstacle_group.sprites():
            if self.hitbox_rect.colliderect(sprite.rect):
                self.kill()
    
    def handle_pot_collision(self):
        for sprite in self.level.pot_group.sprites():
            if self.hitbox_rect.colliderect(sprite.rect):
                self.pierce_count+=1
                sprite.on_collision()

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

        pygame.draw.circle(self.image, self.base_color, (50, 50), self.size)

        current_distance = math.hypot(
            self.rect.centerx - self.start_pos[0], self.rect.centery - self.start_pos[1]
        )

        self.handle_enemy_collision()
        self.handle_obstacle_collision()
        self.handle_wall_collision()
        self.handle_pot_collision()

        if self.pierce_count >= self.max_pierce:
            self.kill()
        

        # if (self.handle_enemy_collision() 
        #     or current_distance > self.max_range
        #     or self.rect.right < MAP_LEFT+64
        #     or self.rect.left > MAP_RIGHT-64
        #     or self.rect.bottom < MAP_TOP+64
        #     or self.rect.top > MAP_BOTTOM-64
        # ):
        #     self.kill()