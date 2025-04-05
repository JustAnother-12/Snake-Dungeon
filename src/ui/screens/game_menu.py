import pygame
from levels.level import Level
from ui.elements.button import ButtonElement
from ui.screens.menu import Menu
from utils.pixil import Pixil

class Menu_logo(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos) -> None:
        super().__init__()
        self.image = Pixil.load("game-assets/graphics/pixil/MENU_LOGO.pixil", 3).frames[0]
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

class MainMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init(game)

    def init(self, game):
        self.music = pygame.mixer.music
        self.music.load('game-assets/audio/main_menu.wav')
        self.music.set_volume(0.6)
        self.music.play(-1)

        self.play_button = ButtonElement(game.SCREEN_WIDTH_TILES/2*game.TILE_SIZE, game.SCREEN_HEIGHT_TILES/2*game.TILE_SIZE, "PLAY", "white", 30,self.play_button_event)
        self.quit_button = ButtonElement(game.SCREEN_WIDTH_TILES/2*game.TILE_SIZE, game.SCREEN_HEIGHT_TILES/1.5*game.TILE_SIZE, "QUIT", "white", 30,self.quit_button_event)
        self.addBtn([self.play_button, self.quit_button])

        self.Main_menu = Menu_logo(game.SCREEN_WIDTH_TILES/2*game.TILE_SIZE, game.SCREEN_WIDTH_TILES/4*game.TILE_SIZE)

        self.add(self.play_button, self.quit_button, self.Main_menu)

    def reset(self):
        self.music.stop()
        self.music.play(-1)

    def get_event(self, event):
        super().get_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.isHovered():
                    button.on_click()

    def play_button_event(self):
        self.music.fadeout(5000)
        new_state = Level(self.game)
        new_state.enter_state()

    def quit_button_event(self):
        self.game.running = False
        self.game.playing = False