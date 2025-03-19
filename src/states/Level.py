from states.state import State
from states.Pause_menu import Pause_menu
import pygame

class Level(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.rect = pygame.Rect(0,0,game.TILE_SIZE*20, game.TILE_SIZE*20)

    def update(self):
        pass

    def get_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                new_state = Pause_menu(self.game)
                new_state.enter_state()
