import pygame

from ui.elements.button import ButtonElement
from ui.screens.state import State

class Menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.game = game
        self.buttons = []
        self.keymap = {}

    def addBtn(self, btns: list[ButtonElement]):
        for btn in btns:
            self.buttons.append(btn)
        for i in range(len(self.buttons)):
            self.keymap[pygame.K_1 + i] = i
            self.keymap[pygame.K_KP1 + i] = i

    def update(self):
        return super().update()
    
    def get_event(self, event):
        if (event.type == pygame.KEYDOWN):
            if event.key in self.keymap.keys():
                self.buttons[self.keymap[event.key]].on_click()