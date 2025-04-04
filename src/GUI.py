from __future__ import annotations
import pygame
import sys
import config.constant as constant

from systems.event_manager import EventManager
from ui.screens.game_menu import MainMenu
from ui.screens.state import State
from utils.help import Share

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100,-16,2,512)
        pygame.mixer.init()
        self.TILE_SIZE = constant.TILE_SIZE
        self.SCREEN_WIDTH_TILES = constant.SCREEN_WIDTH_TILES
        self.SCREEN_HEIGHT_TILES = constant.SCREEN_HEIGHT_TILES
        self.TOP_BOTTOM_BORDER_TILES = constant.TOP_BOTTOM_BORDER_TILES
        self.LEFT_RIGHT_BORDER_TILES = constant.LEFT_RIGHT_BORDER_TILES
        self.TOP_BOTTOM_BORDER_TILES = constant.TOP_BOTTOM_BORDER_TILES
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH_TILES*self.TILE_SIZE, self.SCREEN_HEIGHT_TILES*self.TILE_SIZE))
        self.clock = Share.clock
        self.running, self.playing = True, True
        self.selectBtnMode = "mouse"

        self.state_stack: list[State] = []
        self.load_states()
    
    def update(self):
        self.state_stack[-1].update()

    def get_events(self):
        for event in EventManager.get_events():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            self.state_stack[-1].get_event(event)

    def render(self):
        self.screen.fill("#000000")
        for state in self.state_stack:
            state.draw(self.screen)
        # self.state_stack[-1].(self.game_canvas)
        pygame.display.flip()
        
    def run(self):
        while self.playing:
            # print(self.state_stack, end=" " * 50 + "\r", flush=True)
            EventManager.update()
            self.get_events()
            self.render()
            self.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def load_states(self):
        self.Loading = MainMenu(self)
        self.state_stack.append(self.Loading)

if __name__ == '__main__':
    game = Game()
    while game.running:
        game.run()