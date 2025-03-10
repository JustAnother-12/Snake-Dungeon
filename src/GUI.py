import pygame
import sys
import pixil
from states.Loading import Loading_screen
import constant
from states.state import State
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
        for state in self.state_stack:
            state.draw(self.screen)
        # self.state_stack[-1].(self.game_canvas)
        pygame.display.flip()
        # self.clock.tick(60)
    
    def draw_text(self, text, text_colr, font_size, surface, pos_x, pos_y):
        text_font = pygame.font.Font("game-assets/font/default-pixilart-text.ttf", font_size)
        img:pygame.Surface = text_font.render(text, True, text_colr)
        rect = img.get_rect(center=(pos_x,pos_y))
        surface.blit(img, rect)
        
    def run(self):
        while self.playing:
            self.get_events()
            self.render()
            self.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def load_states(self):
        self.Loading = Loading_screen(self)
        self.state_stack.append(self.Loading)

if __name__ == '__main__':
    game = Game()
    while game.running:
        game.run()