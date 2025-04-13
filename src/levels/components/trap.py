import random
import config.constant as constant
from entities.items.item_stack import F
from utils.help import Share
import utils.pixil as pixil
from time import time
import pygame
from enum import Enum

class TrapState(Enum):
    VISIBLE = 1  # Chỉ hiển thị, chưa kích hoạt (trạng thái mặc định)
    WAITING = 2  # Đang kích hoạt (gai xuất hiện)
    ACTIVATED = 3  # Đang trong quá trình lặp lại (trở về trạng thái ban đầu)

class Trap(pygame.sprite.Sprite):
    from levels import level
    def __init__(self, level_: "level.Level", pos) -> None:
        super().__init__()
        self._level = level_
        self.pos = pos
        # Tải sprite sheet cho bẫy
        self.sprite_sheet = pixil.Pixil.load(
            "game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1
        )
        self.image = self.sprite_sheet.frames[0]  # Frame mặc định (chưa kích hoạt)
        self.rect = self.image.get_rect(topleft=self.pos)
        
        # Trạng thái và thời gian
        self.state = TrapState.VISIBLE
        self.state_time = 0  # Thời gian ở trạng thái hiện tại
        
        # Cấu hình thời gian cho mỗi trạng thái
        self.duration = {
            TrapState.VISIBLE: 0,  # Trạng thái mặc định, không hết hạn
            TrapState.WAITING: 1.5,  # Thời gian gai xuất hiện
            TrapState.ACTIVATED: 0.5,  # Thời gian để lặp lại
        }

    def update(self):
        # Kiểm tra va chạm với rắn
        if (self.__is_collision_with_snake()) and self.state == TrapState.VISIBLE:
            self.change_state(TrapState.WAITING)
        
        # Cập nhật trạng thái dựa trên thời gian
        if self.state != TrapState.VISIBLE:
            self.state_time += Share.clock.get_time() / 1000
            
            if self.state == TrapState.WAITING and self.state_time >= self.duration[TrapState.WAITING]:
                self.change_state(TrapState.ACTIVATED)
                
            elif self.state == TrapState.ACTIVATED and self.state_time >= self.duration[TrapState.ACTIVATED]:
                self.change_state(TrapState.VISIBLE)
    
    def change_state(self, new_state):
        self.state = new_state
        self.state_time = 0
        
        # Cập nhật hình ảnh dựa trên trạng thái
        if new_state == TrapState.VISIBLE:
            self.image = self.sprite_sheet.frames[0]
        elif new_state == TrapState.WAITING:
            self.image = self.sprite_sheet.frames[0]
        elif new_state == TrapState.ACTIVATED:
            Share.audio.set_sound_volume("stabbed", 0.6)
            Share.audio.play_sound("stabbed")
            self.image = self.sprite_sheet.frames[1]
    
    def __is_collision_with_snake(self):
        for snake in self._level.snake_group._sub_group__:
            if pygame.sprite.spritecollideany(self, snake.blocks): # type: ignore
                return True
        return False
        # return pygame.sprite.spritecollideany(self, self._level.snake.blocks) # type: ignore
    
    # def __is_collision_with_monster(self):
    #     for snake in self._level.monster_group._sub_group__:
    #         if pygame.sprite.spritecollideany(self, snake.blocks): # type: ignore
    #             return True
    #     return False