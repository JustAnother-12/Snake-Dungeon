import pygame
from states.state import State
from states.LevelTest import LevelTest
from gui_element.button_class import ButtonElement
from pixil import Pixil

class Menu_logo(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos) -> None:
        super().__init__()
        self.image = Pixil.load("game-assets/graphics/pixil/MENU_LOGO.pixil", 3).frames[0]
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

class Main_menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init(game)

    def init(self, game):
        self.music = pygame.mixer.music
        self.music.load('game-assets/audio/Sekiro Shadows Die Twice _ OST Main Menu Theme ♪.wav')
        self.music.set_volume(0.6)
        self.music.play(-1)

        self.play_button = ButtonElement((game.SCREEN_WIDTH_TILES + game.LEFT_RIGHT_BORDER_TILES*2)/2*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES + game.TOP_BOTTOM_BORDER_TILES*2)/2*game.TILE_SIZE, "PLAY", "white")
        self.quit_button = ButtonElement((game.SCREEN_WIDTH_TILES + game.LEFT_RIGHT_BORDER_TILES*2)/2*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES + game.TOP_BOTTOM_BORDER_TILES*2)/1.5*game.TILE_SIZE, "QUIT", "white")

        self.Main_menu = Menu_logo((game.SCREEN_WIDTH_TILES + game.LEFT_RIGHT_BORDER_TILES*2)/2*game.TILE_SIZE, (game.SCREEN_WIDTH_TILES + game.LEFT_RIGHT_BORDER_TILES*2)/4*game.TILE_SIZE)

        self.add(self.play_button, self.quit_button, self.Main_menu)

    def reset(self):
        self.music.stop()
        self.music.play(-1)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.on_click():
                self.music.fadeout(5000)
                new_state = LevelTest(self.game)
                new_state.enter_state()
            if self.quit_button.on_click():
                self.game.running = False
                self.game.playing = False

    # def render(self, surface):
    #     surface.fill("black")
    #     surface.blit(self.Main_menu_img, self.Main_menu_rect)
    #     for button in self.Button_List:
    #         if(button.checkForInputs(pygame.mouse.get_pos())):
    #             button.img = self.button_glow
    #         else:
    #             button.img = self.button_base
    #         button.update(surface)
    