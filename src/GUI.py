import pygame
import sys
from states.Loading import Loading_screen
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100,-16,2,512)
        pygame.mixer.init()

        self.TILE_SIZE = 16
        self.SCREEN_WIDTH_TILES = 56
        self.SCREEN_HEIGHT_TILES = 48
        self.game_canvas = pygame.Surface((self.SCREEN_WIDTH_TILES*self.TILE_SIZE, self.SCREEN_HEIGHT_TILES*self.TILE_SIZE))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH_TILES*self.TILE_SIZE, self.SCREEN_HEIGHT_TILES*self.TILE_SIZE))
        self.clock = pygame.time.Clock()
        self.running, self.playing = True, True

        self.button_texture_base = pygame.image.load("game-assets/graphics/png/pixil-frame-0.png").convert_alpha()
        self.button_texture_glow = pygame.image.load("game-assets/graphics/png/pixil-frame-1.png").convert_alpha()
        self.button_texture_base = pygame.transform.scale(self.button_texture_base, (self.button_texture_base.get_width()*2, self.button_texture_base.get_height()*2))
        self.button_texture_glow = pygame.transform.scale(self.button_texture_glow, (self.button_texture_glow.get_width()*2, self.button_texture_glow.get_height()*2))

        self.state_stack = []
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
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(self.game_canvas, (0,0))
        pygame.display.flip()
        self.clock.tick(60)
    
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
        pygame.quit()
        sys.exit()

    def load_states(self):
        self.Loading = Loading_screen(self)
        self.state_stack.append(self.Loading)


class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_State(self):
        return self.currentState
    def set_State(self, newState):
        self.currentState = newState

if __name__ == '__main__':
    game = Game()
    while game.running:
        game.run()