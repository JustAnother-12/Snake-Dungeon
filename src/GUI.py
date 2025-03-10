import pygame
import sys
import pixil
from states import Main_menu
from states.state import State
import constant

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100,-16,2,512)
        pygame.mixer.init()

        self.TILE_SIZE = constant.TILE_SIZE
        self.SCREEN_WIDTH_TILES = constant.SCREEN_WIDTH_TILES
        self.SCREEN_HEIGHT_TILES = constant.SCREEN_HEIGHT_TILES
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH_TILES*self.TILE_SIZE, self.SCREEN_HEIGHT_TILES*self.TILE_SIZE))
        self.clock = pygame.time.Clock()
        self.running, self.playing = True, True

        t = pixil.Pixil.load("game-assets/graphics/pixil/PAUSE_MENU_BTN_BG_SHEET.pixil", 2)
        self.button_texture_base = t.frames[0]
        self.button_texture_glow = t.frames[1]

        self.state_stack: list[State] = []
        self.load_states()

    def update(self):
        self.state_stack[-1].update()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            self.state_stack[-1].get_event(event)

    def render(self):
        self.screen.fill("#000000")
        for state in self.state_stack:
            state.draw(self.screen)
        # self.state_stack[-1].(self.game_canvas)
        pygame.display.flip()
        # self.clock.tick(60)
        
    def run(self):
        while self.playing:
            print(self.state_stack, end=" " * 50 + "\r", flush=True)
            self.get_events()
            self.render()
            self.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def load_states(self):
        self.Loading = Main_menu.Main_menu(self)
        self.state_stack.append(self.Loading)

if __name__ == '__main__':
    game = Game()
    while game.running:
        game.run()