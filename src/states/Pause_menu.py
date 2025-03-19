import constant
from states.Menu import Menu
from states.state import State
from gui_element.button_class import ButtonElement
from gui_element.Sprite_image import ImageElement
from gui_element.text_class import TextElement
from states.Stats import Stats
from pixil import Pixil


import pygame

class Pause_menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.Paused_text = TextElement("PAUSED", "white", 35, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 15)*game.TILE_SIZE, "center")

        self.Background_texture = Pixil.load(constant.Texture.pasue_menu_bg, 2).frames[0]
        self.Background_rect = ImageElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE, self.Background_texture)

        self.restart_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 9)*game.TILE_SIZE ,"NEW RUN", "white")
        self.continue_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 2)*game.TILE_SIZE ,"CONTINUE", "white")
        self.stats_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 5)*game.TILE_SIZE ,"STATS", "white")
        self.main_menu_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 12)*game.TILE_SIZE ,"MAIN MENU", "white")
        self.addBtn([self.restart_button, self.continue_button, self.stats_button, self.main_menu_button])

        self.add(self.Background_rect, self.Paused_text, self.restart_button, self.continue_button, self.stats_button, self.main_menu_button)

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game.state_stack.pop()
            self.game.state_stack[-1].visible = True
        return super().update()

    def get_event(self, event):
        super().get_event(event)
        if (self.game.selectBtnMode == "mouse" and event.type == pygame.MOUSEBUTTONDOWN) or (self.game.selectBtnMode == "key" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
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
                self.game.state_stack[-1].visible = True
            
            if self.main_menu_button.on_click():
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()
                self.game.state_stack[-1].reset()