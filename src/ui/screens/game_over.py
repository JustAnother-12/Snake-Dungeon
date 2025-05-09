import pygame

from ui.elements.button import ButtonElement
from ui.elements.text import TextElement
from ui.screens.menu import Menu
from config.constant import SCREEN_HEIGHT_TILES, SCREEN_WIDTH_TILES, TILE_SIZE

class GameOver_menu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.module = True

        self.Gamer_over_text = TextElement("GAME OVER", "white", 45, (SCREEN_WIDTH_TILES//2)*TILE_SIZE, (SCREEN_HEIGHT_TILES//2 - 8)*TILE_SIZE, "center")

        self.restart_button = ButtonElement((SCREEN_WIDTH_TILES/2)*TILE_SIZE, (SCREEN_HEIGHT_TILES/2)*TILE_SIZE ,"NEW RUN", "white", callback=self.restart_button_event)
        self.main_menu_button = ButtonElement((SCREEN_WIDTH_TILES/2)*TILE_SIZE, (SCREEN_HEIGHT_TILES/2 + 8)*TILE_SIZE ,"MAIN MENU", "white", callback=self.main_menu_button_event)
        self.addBtn([self.restart_button, self.main_menu_button])

 
        self.add(self.Gamer_over_text, self.restart_button, self.main_menu_button)


    def update(self):
        return super().update()

    def get_event(self, event):
        super().get_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.isHovered():
                    button.on_click()

    def restart_button_event(self):
        print("Restarting game...")
        self.exit_state()
        self.game.get_state().exit_state()
        from levels.level import Level
        new_state = Level(self.game)
        new_state.enter_state()

    def main_menu_button_event(self):
        while len(self.game.state_stack) > 1:
            self.game.get_state().exit_state()   
        self.game.get_state().reset()