import config.constant as constant
from ui.elements.button import ButtonElement
from ui.elements.image import ImageElement
from ui.elements.text import TextElement
from ui.screens.menu import Menu
from ui.screens.Stats_Menu import Stats_menu
from utils.pixil import Pixil


import pygame

class Pause_menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.Paused_text = TextElement("PAUSED", "white", 35, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 15)*game.TILE_SIZE, "center")

        self.Background_texture = Pixil.load(constant.Texture.pasue_menu_bg, 2).frames[0]
        self.Background_rect = ImageElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE, self.Background_texture)

        self.restart_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 9)*game.TILE_SIZE ,"NEW RUN", "white", callback=self.restart_button_event)
        self.continue_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 2)*game.TILE_SIZE ,"CONTINUE", "white", callback=self.continue_button_event)
        self.stats_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 5)*game.TILE_SIZE ,"STATS", "white", callback=self.stats_button_event)
        self.main_menu_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 12)*game.TILE_SIZE ,"MAIN MENU", "white", callback=self.main_menu_button_event)
        self.addBtn([self.restart_button, self.continue_button, self.stats_button, self.main_menu_button])

        self.add(self.Background_rect, self.Paused_text, self.restart_button, self.continue_button, self.stats_button, self.main_menu_button)

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game.state_stack.pop()
            self.game.state_stack[-1].visible = True
        return super().update()

    def get_event(self, event):
        super().get_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.isHovered():
                    button.on_click()

    def restart_button_event(self):
        self.game.state_stack.pop()
        self.game.state_stack[-1].reset()
        self.game.state_stack[-1].visible = True

    def continue_button_event(self):
        self.game.state_stack.pop()
        self.game.state_stack[-1].visible = True

    def stats_button_event(self):
        new_state = Stats_menu(self.game)
        self.game.state_stack.pop()
        new_state.enter_state()
        self.game.state_stack[-1].visible = True
    
    def main_menu_button_event(self):
        while len(self.game.state_stack) > 1:
            self.game.state_stack.pop()
        self.game.state_stack[-1].reset()