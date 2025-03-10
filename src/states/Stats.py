import pygame
from states.state import State

class Stats(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.Background_texture = pygame.image.load("game-assets/graphics/png/Stats_bg.png").convert_alpha()
        self.Background_rect = self.Background_texture.get_rect(center=((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE))

    def update(self):
        pass

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_state()
                     
    def render(self, surface):
        surface.blit(self.Background_texture, self.Background_rect)