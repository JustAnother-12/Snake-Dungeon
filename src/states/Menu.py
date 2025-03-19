from states.state import State
from gui_element.button_class import ButtonElement
import pygame

class Menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.game = game
        self.indexOfSelectedBtn = 0
        self.buttons = []

    def addBtn(self, btns: list[ButtonElement]):
        for btn in btns:
            self.buttons.append(btn)

    def change_mode(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            print("CHANGE MODE!")
            if self.game.selectBtnMode == "mouse":
                self.game.selectBtnMode = "key"
                self.indexOfSelectedBtn = 0
                self.change_selected_btn()
            else:
                self.game.selectBtnMode = "mouse"
                self.change_selected_btn(True)

    def update(self):
        if self.game.selectBtnMode == "key":
            self.change_selected_btn()
        return super().update()
    
    def move_by_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.indexOfSelectedBtn = (self.indexOfSelectedBtn + 1) % len(self.buttons)
        if keys[pygame.K_UP]:
            self.indexOfSelectedBtn = (self.indexOfSelectedBtn - 1) % len(self.buttons)

    def get_event(self, event):
        self.change_mode()
        if self.game.selectBtnMode == "key":
            self.move_by_key()
            
    def change_selected_btn(self, no_choose = False):
        for i in range(len(self.buttons)):
            if not no_choose:
                self.buttons[i].set_selected(1 if i == self.indexOfSelectedBtn else 0)
            else:
                self.buttons[i].set_selected(-1)
