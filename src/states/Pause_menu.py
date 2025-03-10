from states.state import State
from button_class import Button
from states.Stats import Stats

import pygame

class Pause_menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.Background_texture = pygame.image.load("game-assets/graphics/png/Pause_bg.png").convert_alpha()
        self.Background_rect = self.Background_texture.get_rect(center=((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE))

        self.button_base = game.button_texture_base
        self.button_glow = game.button_texture_glow

        self.restart_button = Button(self.button_base, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 9)*game.TILE_SIZE ,"NEW RUN", "white")
        self.continue_button = Button(self.button_base, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 2)*game.TILE_SIZE ,"CONTINUE", "white")
        self.stats_button = Button(self.button_base, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 5)*game.TILE_SIZE ,"STATS", "white")
        self.main_menu_button = Button(self.button_base, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 + 12)*game.TILE_SIZE ,"MAIN MENU", "white")
        self.button_list = [self.restart_button, self.continue_button, self.stats_button, self.main_menu_button]

    def update(self):
        pass

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                if(pygame.mouse.get_pressed()[0] and self.restart_button.checkForInputs(pygame.mouse.get_pos())):
                    while len(self.game.state_stack) > 3:
                        self.game.state_stack.pop()
                if(pygame.mouse.get_pressed()[0] and self.continue_button.checkForInputs(pygame.mouse.get_pos())):
                    self.exit_state()
                if(pygame.mouse.get_pressed()[0] and self.stats_button.checkForInputs(pygame.mouse.get_pos())):
                    new_state = Stats(self.game)
                    new_state.enter_state()
                if(pygame.mouse.get_pressed()[0] and self.main_menu_button.checkForInputs(pygame.mouse.get_pos())):
                    while len(self.game.state_stack) > 1:
                        self.game.state_stack.pop()

    def render(self, surface):
        surface.fill("black")
        surface.blit(self.Background_texture, self.Background_rect)
        self.game.draw_text("Pause", "white", 35, surface, (self.game.SCREEN_WIDTH_TILES/2)*self.game.TILE_SIZE, (self.game.SCREEN_HEIGHT_TILES/5)*self.game.TILE_SIZE,)

        for button in self.button_list:
            if button.checkForInputs(pygame.mouse.get_pos()):
                button.img = self.button_glow
            else:
                button.img = self.button_base
            button.update(surface)