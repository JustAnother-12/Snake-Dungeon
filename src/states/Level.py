from states.state import State
from states.Pause_menu import Pause_menu
import pygame
from generators.region_generator import generate_frame_L_region, generate_L_shaped_region, generate_square_border_region, Generate_rectangle_region

# Trap_possible_regions = [generate_square_border_region(10,10,6,2),
#                         generate_square_border_region(7,7,4,2),
#                         generate_square_border_region(5,5,8,2),
#                         list(set(generate_L_shaped_region))]

class Level(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.rect = pygame.Rect(0,0,game.TILE_SIZE*20, game.TILE_SIZE*20)

    def update(self):
        pass

    def get_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                new_state = Pause_menu(self.game)
                new_state.enter_state()
