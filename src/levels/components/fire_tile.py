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
    def __init__(self, level, pos, burn_time) -> None:
        super().__init__()
        self.level = level
        self.fireImgs = pixil.Pixil.load("game-assets/graphics/pixil/FIRE_ANIMATION.pixil").frames
        self.frame_duration = 0.1
        self.frame_index = 0
        self.image = self.fireImgs[self.frame_index]
        self.image.set_alpha(0)
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.time_animation = 0
        self.state_time = 0
        self.state = FIRE_STATE.APPEAR
        self.state_duration = {
            FIRE_STATE.APPEAR: 500,
            FIRE_STATE.ACTIVE: burn_time,
            FIRE_STATE.DISAPPEAR: 500,
        }        
    def update(self):
        
        dt = Share.clock.get_time()
        self.time_animation += dt
        self.state_time += dt
        
        if self.time_animation >= self.frame_duration:
            self.time_animation = 0
            self.frame_index = (self.frame_index + 1) % len(self.fireImgs)
            
        self.image = self.fireImgs[self.frame_index]
        
        if self.state == FIRE_STATE.APPEAR:
            alpha = int(150 * (self.state_time/self.state_duration[FIRE_STATE.APPEAR]))
            self.image.set_alpha(alpha)
            if self.state_time >= self.state_duration[FIRE_STATE.APPEAR]:
                self.change_state(FIRE_STATE.ACTIVE)
                
        if self.state == FIRE_STATE.ACTIVE:
            if Share.audio.is_sound_playing('burning-sound') == False:
                Share.audio.play_sound('burning-sound',maxtime=max(0, self.state_duration[FIRE_STATE.ACTIVE]- self.state_time))
                Share.audio.set_sound_volume('burning-sound', 0.5)
            self.image.set_alpha(random.randint(150, 200))
            # TODO: Implement burn logic
            self.handle_collision(self.level.snake)
            
            if self.state_time >= self.state_duration[FIRE_STATE.ACTIVE]:
                self.change_state(FIRE_STATE.DISAPPEAR)
                
        if self.state == FIRE_STATE.DISAPPEAR:
            Share.audio.stop_sound('burning-sound', self.state_duration[FIRE_STATE.DISAPPEAR])
            alpha = int(150 * (1 - max(self.state_time/self.state_duration[FIRE_STATE.DISAPPEAR], 0)))
            self.image.set_alpha(alpha)
            if self.state_time >= self.state_duration[FIRE_STATE.DISAPPEAR]:
                self.kill()
            
                
    def change_state(self, new_state: FIRE_STATE) -> None:
        self.state = new_state
        self.state_time = 0
        
    def handle_collision(self, player):
        for sprite in player.sprites():
            if pygame.sprite.collide_rect(self, sprite):
                sprite.take_fire_damage(1)
        

class Fire_Group(pygame.sprite.AbstractGroup):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level
        

    def addComponents(self, x: int, y: int, width_tile: int, height_tile: int, burn_time) -> None:
        for i in range(0, width_tile):
            for j in range(0, height_tile):
                fire_tile = Fire_Tile(self.level, (i*constant.TILE_SIZE + x, j*constant.TILE_SIZE + y), burn_time)
                self.add(fire_tile)