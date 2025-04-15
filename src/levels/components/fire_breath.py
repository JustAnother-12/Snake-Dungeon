import random
import pygame
import math
from config import constant
from utils import pixil


class FireBreath(pygame.sprite.Sprite):
    def __init__(self, level, length=3, damage=1.0):
        super().__init__()
        self.level = level
        self.length = length
        self.breath = pixil.Pixil.load(constant.Texture.fire_breath).frames
        self.image = self.breath[0]
        self.rect = self.image.get_rect()
        self.angle = None
        self.target_angle = 0
        self.rotation_speed = 8  # Degrees per frame - adjust for faster/slower rotation
        self.animation_timer = 0
        self.damage = damage
        
    def update_pos(self, pos, direction: pygame.Vector2):
        if self.angle == None:
            self.angle = pygame.Vector2(1, 0).angle_to(direction)
            self.image = pygame.transform.rotate(self.breath[0], self.angle)
        # Calculate target angle between direction vector and reference vector (1,0)
        if self.target_angle != pygame.Vector2(1, 0).angle_to(direction):
            self.animation_timer = 0
            self.target_angle = pygame.Vector2(1, 0).angle_to(direction)
        else:
            self.animation_timer += 0.2
        # Smoothly rotate toward the target angle
        self._rotate_smoothly()
        
        # Rotate the breath surface to match the current angle
        self.image = pygame.transform.rotate(self.breath[int(self.animation_timer) if self.animation_timer < 3 else random.randint(3, 5)], -self.angle)
        self.rect = self.image.get_rect()
        
        # Calculate the position to center the breath on the snake's head
        angle_rad = math.radians(self.angle)
        offset_x = (constant.TILE_SIZE * (self.length+1) // 2) * math.cos(angle_rad)
        offset_y = (constant.TILE_SIZE * (self.length+1) // 2) * math.sin(angle_rad)
        
        # Center the breath at the calculated position
        self.rect.center = (pos[0] + offset_x, pos[1] + offset_y)
        self.handle_collision()
    
    def _rotate_smoothly(self):
        if self.angle is None:
            return
        """Gradually rotate the fire breath toward the target angle"""
        # Find the shortest rotation path (clockwise or counterclockwise)
        angle_diff = (self.target_angle - self.angle) % 360
        if angle_diff > 180:
            angle_diff -= 360
            
        # If we're close enough to the target angle, snap to it
        if abs(angle_diff) < self.rotation_speed:
            self.angle = self.target_angle
        else:
            # Otherwise, rotate with the defined speed in the correct direction
            rotation_amount = self.rotation_speed * (1 if angle_diff > 0 else -1)
            self.angle = (self.angle + rotation_amount) % 360

    def handle_collision(self):
        for group in self.level.snake_group._sub_group__:
            from entities.Player import Snake
            if isinstance(group, Snake):
                continue
            for sprite in group.sprites():
                if pygame.sprite.collide_rect(self, sprite):
                    sprite.take_fire_damage(self.damage)