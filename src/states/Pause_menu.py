from operator import truediv
from states.state import State
from gui_element.button_class import ButtonElement
from states.Stats import Stats

import pygame

class Pause_menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.Background_texture = pygame.image.load("game-assets/graphics/png/Pause_bg.png").convert_alpha()
        self.Background_rect = self.Background_texture.get_rect(center=((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE))

        self.button_base = game.button_texture_base
        self.button_glow = game.button_texture_glow

        self.restart_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 9)*game.TILE_SIZE ,"NEW RUN", "white")
        self.continue_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 3)*game.TILE_SIZE ,"CONTINUE", "white")
        self.stats_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 3)*game.TILE_SIZE ,"STATS", "white")
        self.main_menu_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 9)*game.TILE_SIZE ,"MAIN MENU", "white")

        self.button_list = [self.restart_button, self.continue_button, self.stats_button, self.main_menu_button]
        self.add(self.restart_button, self.continue_button, self.stats_button, self.main_menu_button)

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game.state_stack.pop()
            self.game.state_stack[-1].visible = True

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.on_click():
                self.game.state_stack.pop()
                self.game.state_stack[-1].reset()
                self.game.state_stack[-1].visible = True

            if self.continue_button.on_click():
                self.game.state_stack.pop()
                self.game.state_stack[-1].visible = True

            if self.stats_button.on_click():
                new_state = Stats(self.game)
                self.game.state_stack.pop()
                new_state.enter_state()
            
            if self.main_menu_button.on_click():
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()