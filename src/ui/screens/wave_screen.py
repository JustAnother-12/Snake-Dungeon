

import pygame
from config import constant
from ui.elements.text import TextElement
from ui.screens.pause import Pause_menu
from ui.screens.state import State
from utils.help import Share


class WaveScreen(State):
    from levels import level

    def __init__(self, game, level_: "level.Level", message: str = "") -> None:
        super().__init__(game)
        self.game = game

        self.level_text = TextElement(f"wave {level_.wave_manager.current_wave_index} / {level_.wave_manager.waves}", "white", 35, constant.SCREEN_WIDTH_TILES /
                                      2 * game.TILE_SIZE, constant.SCREEN_HEIGHT_TILES / 2 * game.TILE_SIZE - 50, "center")
        # self.text = TextElement(message, "white", 35, constant.SCREEN_WIDTH_TILES / 2 * game.TILE_SIZE, constant.SCREEN_HEIGHT_TILES / 2 * game.TILE_SIZE, "center")
        self.count = TextElement("wave in 3", "white", 20, constant.SCREEN_WIDTH_TILES /
                                 2 * game.TILE_SIZE, constant.SCREEN_HEIGHT_TILES / 2 * game.TILE_SIZE, "center")
        self.level_ = level_
        self.duration = 3

        # self.add(self.text)
        self.add(self.count)
        self.add(self.level_text)

    def update(self):
        self.duration -= Share.clock.get_time() / 1000
        self.count.set_text(f"Starting in {int(self.duration) + 1}")
        if self.duration <= 0:
            self.game.state_stack.pop()
            from levels.level import LevelStatus
            self.level_.level_status = LevelStatus.PLAYING
            self.level_.snake.auto_state = True
            self.level_.snake.is_curling = False
            self.level_.snake.direction = pygame.Vector2(0, -1)
            self.level_.wave_manager.start()
            # print(self.level_.snake.direction)
            self.game.state_stack[-1].visible = True

        allow_key = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
                     pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        keys = pygame.key.get_just_pressed()
        for key in allow_key:
            if keys[key]:
                self.game.state_stack.pop()
                from levels.level import LevelStatus
                self.level_.level_status = LevelStatus.PLAYING
                self.level_.snake.auto_state = True
                self.level_.snake.is_curling = False
                self.game.state_stack[-1].visible = True
                self.level_.wave_manager.start()

        if keys[pygame.K_ESCAPE]:
            self.game.state_stack.append(Pause_menu(self.game))

    # chuyển hướng đến cho level
    def reset(self):
        self.game.state_stack.pop()
        self.level_.reset()
