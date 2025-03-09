from states.state import State
from states.Main_menu import Main_menu
from states.Level import Level
import time, pygame

class Loading_screen(State):
    def __init__(self, game) -> None:
        super().__init__(game)

    def update(self):
        if self.prev_state != None:
            pygame.time.wait(2000)
            new_state = Level(self.game)
            new_state.enter_state()
        else:
            new_state = Main_menu(self.game)
            new_state.enter_state()

    def get_event(self, event):
        pass

    def render(self, surface):
        surface.fill("black")
        self.game.draw_text("LOADING", "white", 30, surface, (self.game.SCREEN_WIDTH_TILES/2)*self.game.TILE_SIZE, (self.game.SCREEN_HEIGHT_TILES/2)*self.game.TILE_SIZE)