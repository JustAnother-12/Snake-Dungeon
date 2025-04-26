import pygame

from ui.elements.button import ButtonElement
from ui.elements.text import TextElement
from ui.screens.menu import Menu
from config.constant import SCREEN_HEIGHT_TILES, SCREEN_WIDTH_TILES, TILE_SIZE

class YouWin_menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.You_win_text = TextElement("YOU WIN!", "white", 45, (SCREEN_WIDTH_TILES//2)*TILE_SIZE, (SCREEN_HEIGHT_TILES//2 - 10)*TILE_SIZE, "center")
        
        self.bg_sprite = pygame.sprite.Sprite()
        self.bg_sprite.image = pygame.Surface((SCREEN_WIDTH_TILES*TILE_SIZE, SCREEN_HEIGHT_TILES*TILE_SIZE))
        self.bg_sprite.rect = self.bg_sprite.image.get_rect(topleft=(0,0))

        self.restart_button = ButtonElement((SCREEN_WIDTH_TILES//2)*TILE_SIZE, (SCREEN_HEIGHT_TILES//2 + 2)*TILE_SIZE ,"NEW RUN", "white", callback=self.restart_button_event)
        self.main_menu_button = ButtonElement((SCREEN_WIDTH_TILES//2)*TILE_SIZE, (SCREEN_HEIGHT_TILES//2 + 10)*TILE_SIZE ,"MAIN MENU", "white", callback=self.main_menu_button_event)
        
        self.addBtn([self.restart_button, self.main_menu_button])

        self.total_time_text = TextElement(f'Total time: 00:00','yellow', 25, (SCREEN_WIDTH_TILES//2)*TILE_SIZE, (SCREEN_HEIGHT_TILES//2 - 6)*TILE_SIZE, "center")

        self.add(self.bg_sprite, self.You_win_text,self.total_time_text, self.restart_button, self.main_menu_button)
       

    def update(self):
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

    def main_menu_button_event(self):
        while len(self.game.state_stack) > 1:
            self.game.state_stack.pop()
        self.game.state_stack[-1].reset()