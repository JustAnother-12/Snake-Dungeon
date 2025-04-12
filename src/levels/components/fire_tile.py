from ast import Tuple
from enum import Enum
import random
from re import S
import pygame
from config import constant
from utils import pixil
from utils.help import Share

class FIRE_STATE(Enum):
    APPEAR = 1
    ACTIVE = 2
    DISAPPEAR = 3
    
class Fire_Tile(pygame.sprite.Sprite):
    def __init__(self, level, pos, width_tile, height_tile, burn_time, damage = 1) -> None:
        super().__init__()
        self.level = level
        self.width_tile = width_tile
        self.height_tile = height_tile
        self.burn_time = burn_time
        self.damage = damage
        self.frames = pixil.Pixil.load("game-assets/graphics/pixil/FIRE_ANIMATION.pixil").frames
        self.frame_duration = 0.1
        self.frame_index = 0
        self.image = pygame.Surface((constant.TILE_SIZE*width_tile, constant.TILE_SIZE*height_tile), pygame.SRCALPHA)
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.time_animation = 0
        self.state_time = 0
        self.state = FIRE_STATE.APPEAR
            
        
    def draw_img(self):
        if self.image is None: return
        
        for x in range(self.width_tile):
            for y in range(self.height_tile):
                self.image.blit(self.frames[self.frame_index], (x*constant.TILE_SIZE, y*constant.TILE_SIZE))
        
    def update(self):
        self.state_duration = {
            FIRE_STATE.APPEAR: 0.5,
            FIRE_STATE.ACTIVE: self.burn_time,
            FIRE_STATE.DISAPPEAR: 0.5,
        }    
        if self.image is None: return
        self.image = pygame.Surface((constant.TILE_SIZE*self.width_tile, constant.TILE_SIZE*self.height_tile), pygame.SRCALPHA)
        self.draw_img()
        dt = Share.clock.get_time() / 1000
        self.time_animation += dt
        self.state_time += dt
        
        if self.time_animation >= self.frame_duration:
            self.time_animation = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        
        if self.state == FIRE_STATE.APPEAR:
            alpha = int(150 * (self.state_time/self.state_duration[FIRE_STATE.APPEAR]))
            self.image.set_alpha(alpha)
            if self.state_time >= self.state_duration[FIRE_STATE.APPEAR]:
                self.change_state(FIRE_STATE.ACTIVE)
                
        if self.state == FIRE_STATE.ACTIVE:
            if Share.audio.is_sound_playing('burning-sound') == False:
                Share.audio.play_sound('burning-sound',maxtime=max(0, int((self.state_duration[FIRE_STATE.ACTIVE] - self.state_time) * 1000)))
                Share.audio.set_sound_volume('burning-sound', 0.5)
            self.image.set_alpha(random.randint(150, 200))
            # TODO: Implement burn logic
            self.handle_collision()
            
            if self.state_time >= self.state_duration[FIRE_STATE.ACTIVE]:
                self.change_state(FIRE_STATE.DISAPPEAR)
                
        if self.state == FIRE_STATE.DISAPPEAR:
            Share.audio.stop_sound('burning-sound', int(self.state_duration[FIRE_STATE.DISAPPEAR]*1000))
            alpha = int(150 * (1 - max(self.state_time/self.state_duration[FIRE_STATE.DISAPPEAR], 0)))
            self.image.set_alpha(alpha)
            if self.state_time >= self.state_duration[FIRE_STATE.DISAPPEAR]:
                self.kill()
            
                
    def change_state(self, new_state: FIRE_STATE) -> None:
        self.state = new_state
        self.state_time = 0
        
    def handle_collision(self):
        for group in self.level.snake_group._sub_group__:
            for sprite in group.sprites():
                if pygame.sprite.collide_rect(self, sprite):
                    sprite.take_fire_damage(self.damage)
        

# class Fire_Group(pygame.sprite.AbstractGroup):
#     def __init__(self, level) -> None:
#         super().__init__()
#         self.level = level
        

#     def addComponents(self, x: int, y: int, width_tile: int, height_tile: int, burn_time) -> None:
#         for i in range(0, width_tile):
#             for j in range(0, height_tile):
#                 fire_tile = Fire_Tile(self.level, (i*constant.TILE_SIZE + x, j*constant.TILE_SIZE + y), burn_time)
#                 self.add(fire_tile)