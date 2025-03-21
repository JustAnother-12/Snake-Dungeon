from operator import truediv
from states.Menu import Menu
from states.state import State
from gui_element.button_class import ButtonElement
from gui_element.Sprite_image import ImageElement
from gui_element.text_class import TextElement


import pygame

class GameOver_menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.Gamer_over_text = TextElement("GAME OVER", "white", 45, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 8)*game.TILE_SIZE, "center")
        self.black_rect = pygame.Rect(0,0,game.SCREEN_WIDTH_TILES*game.TILE_SIZE, game.SCREEN_HEIGHT_TILES*game.TILE_SIZE)
        self.Background_texture = pygame.Surface((self.black_rect.w,self.black_rect.h))
        # self.Background_rect = ImageElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE, self.Background_texture)

        self.restart_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE ,"NEW RUN", "white")
        self.main_menu_button = ButtonElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 8)*game.TILE_SIZE ,"MAIN MENU", "white")
        self.addBtn([self.restart_button, self.main_menu_button])

        # self.add(self.Background_rect,self.Gamer_over_text, self.restart_button, self.main_menu_button)
        self.add(self.Gamer_over_text, self.restart_button, self.main_menu_button)

    def update(self):
        return super().update()

    def get_event(self, event):
        super().get_event(event)
        if (self.game.selectBtnMode == "mouse" and event.type == pygame.MOUSEBUTTONDOWN) or (self.game.selectBtnMode == "key" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            if self.restart_button.on_click():
                self.game.state_stack.pop()
                self.game.state_stack[-1].reset()
                self.game.state_stack[-1].visible = True
            
            if self.main_menu_button.on_click():
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()