import pygame
from states.state import State
from states.Level import Level
from button_class import Button


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

        self.Main_menu_img = pygame.image.load("game-assets/graphics/png/Main_Logo.png").convert_alpha()
        self.Main_menu_img = pygame.transform.scale(self.Main_menu_img, (self.Main_menu_img.get_width()*3, self.Main_menu_img.get_height()*3))
        self.Main_menu_rect = self.Main_menu_img.get_rect(center=((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/4)*game.TILE_SIZE))

    def update(self):
        pass

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

    def render(self, surface):
        surface.fill("black")
        surface.blit(self.Main_menu_img, self.Main_menu_rect)
        for button in self.Button_List:
            if(button.checkForInputs(pygame.mouse.get_pos())):
                button.img = self.button_glow
            else:
                button.img = self.button_base
            button.update(surface)
    