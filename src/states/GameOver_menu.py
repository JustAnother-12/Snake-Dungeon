from operator import truediv
from states.state import State
from gui_element.button_class import ButtonElement
from states.Stats import Stats

import pygame

class GameOver_menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.Background_texture = pygame.image.load("game-assets/graphics/png/Pause_bg.png").convert_alpha()
        self.Background_rect = self.Background_texture.get_rect(center=((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE))

        self.restart_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 8)*game.TILE_SIZE ,"NEW RUN", "white")
        self.main_menu_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 2)*game.TILE_SIZE ,"MAIN MENU", "white")

        self.button_list = [self.restart_button, self.main_menu_button]
        self.add(self.restart_button, self.main_menu_button)

    def update(self):
        pass
        # if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
        #     self.game.state_stack.pop()
        #     self.game.state_stack[-1].visible = True

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.on_click():
                self.game.state_stack.pop()
                self.game.state_stack[-1].reset()
                self.game.state_stack[-1].visible = True
            
            if self.main_menu_button.on_click():
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()