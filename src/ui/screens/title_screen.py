

import pygame
from config import constant
from ui.elements.text import TextElement
from ui.screens.pause import Pause_menu
from ui.screens.state import State


class TitleScreen(State):
    def __init__(self, game, level, message: str = "") -> None:
        super().__init__(game)
        self.game = game
        
        self.text = TextElement(message, "white", 35, constant.SCREEN_WIDTH_TILES / 2 * game.TILE_SIZE, constant.SCREEN_HEIGHT_TILES / 2 * game.TILE_SIZE, "center")
        self.level = level
    
        self.add(self.text)
    
    def update(self):
        allow_key = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        keys = pygame.key.get_pressed()
        for key in allow_key:
            if keys[key]:
                self.game.state_stack.pop()
                from levels.level import LevelStatus
                self.level.level_status = LevelStatus.PLAYING
                self.level.snake.auto_state = True
                self.level.snake.is_curling = False
                self.game.state_stack[-1].visible = True
        
        if keys[pygame.K_ESCAPE]:
            self.game.state_stack.append(Pause_menu(self.game))
    
    # chuyển hướng đến cho level
    def reset(self):
        self.game.state_stack.pop()
        self.level.reset()
    
     