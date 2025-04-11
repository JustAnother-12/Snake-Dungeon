import pygame
import math
from collections import deque
from config.constant import MAP_TOP, MAP_BOTTOM, MAP_LEFT, MAP_RIGHT
from levels.components.bomb import Bomb, BombState


class Projectile(pygame.sprite.Sprite):
    def __init__(self, level, x_pos, y_pos, target_x, target_y, color, max_range, speed) -> None:
        super().__init__()
        self.level = level
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)  # Increased size for longer trail
        self.base_color = color
        pygame.draw.circle(self.image, color, (50, 50), 5)  # Center of larger surface
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.speed = speed
        self.start_pos = (x_pos, y_pos)
        self.max_range = max_range
        
        # Trail settings
        self.trail = deque(maxlen=20)  # Increased length for a longer trail
        self.trail_alpha_step = 255 // 50
        
        dx = target_x - x_pos
        dy = target_y - y_pos
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            self.dx = dx / distance * self.speed
            self.dy = dy / distance * self.speed
        else:
            self.dx = 0
            self.dy = 0

    def update(self):
        # Store current center position for trail
        trail_pos = (self.rect.centerx, self.rect.centery) #type: ignore
        self.trail.append(trail_pos)
        
        # Update position
        self.rect.x += self.dx #type: ignore
        self.rect.y += self.dy #type: ignore
         
        # Redraw the entire image with trail
        self.image.fill((0, 0, 0, 0))  # Clear the surface (transparent) #type: ignore
        
        # Draw trail
        for i, pos in enumerate(self.trail):
            # Calculate fading alpha
            alpha = 0 + (i * self.trail_alpha_step)
            
            # Calculate relative position to the sprite's center
            rel_x = pos[0] - self.rect.centerx + 50  #type: ignore
            rel_y = pos[1] - self.rect.centery + 50  #type: ignore
            
            # Draw trail segment with decreasing size
            pygame.draw.circle(self.image,  #type: ignore
                             (255, 255, 255, alpha),
                             (int(rel_x), int(rel_y)),
                             1 + (i * 0.2))  # Gradual size decrease for smoother look

        # Draw the projectile itself on top
        pygame.draw.circle(self.image, self.base_color, (50, 50), 4) #type: ignore
        
        # Check for removal conditions
        current_distance = math.sqrt((self.rect.centerx - self.start_pos[0])**2 + #type: ignore
                                   (self.rect.centery - self.start_pos[1])**2) #type: ignore
        
        if (current_distance > self.max_range or
            self.rect.right < MAP_LEFT or self.rect.left > MAP_RIGHT or #type: ignore
            self.rect.bottom < MAP_TOP or self.rect.top > MAP_BOTTOM): #type: ignore
            # TODO: code vậy hơi cứng quá, cần làm mềm hơn
            self.level.bomb_group.add(Bomb(self.level, self.rect.topleft, BombState.ACTIVE)) #type: ignore
            self.kill()
