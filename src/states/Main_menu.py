import pygame
from states.state import State
from states.LevelTest import LevelTest
from button_class import Button
from pixil import Pixil

class Menu_logo(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos) -> None:
        super().__init__()
        self.image = Pixil.load("game-assets/graphics/pixil/MENU_LOGO.pixil", 3).frames[0]
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Main_menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.music = pygame.mixer.music
        self.music.load('game-assets/audio/Sekiro Shadows Die Twice _ OST Main Menu Theme ♪.wav')
        self.music.set_volume(0.6)
        self.music.play(-1)

        self.button_base = game.button_texture_base
        self.button_glow = game.button_texture_glow

        self.play_button = Button(self.button_base, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE, "PLAY", "white")
        self.quit_button = Button(self.button_base, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/1.5)*game.TILE_SIZE, "QUIT", "white")
        self.Button_List = [self.play_button, self.quit_button]

        # self.Main_menu_img = pygame.image.load("game-assets/graphics/png/Main_Logo.png").convert_alpha()
        self.Main_menu = Menu_logo((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/4)*game.TILE_SIZE)

        self.add(self.play_button, self.quit_button, self.Main_menu)

    def update(self):
        for button in self.Button_List:
            if(button.checkForInputs(pygame.mouse.get_pos())):
                button.image = self.button_glow
            else:
                button.image = self.button_base

    def get_event(self, event):
        from states.Loading import Loading_screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(pygame.mouse.get_pressed()[0] and self.play_button.checkForInputs(pygame.mouse.get_pos())):
                new_state = Loading_screen(self.game)
                self.music.fadeout(5000)
                new_state.enter_state()
            if(pygame.mouse.get_pressed()[0] and self.quit_button.checkForInputs(pygame.mouse.get_pos())):
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
    