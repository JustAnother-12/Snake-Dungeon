from states.state import State
from states.Main_menu import Main_menu
from states.LevelTest import LevelTest
import time, pygame

# không cần bởi pygame chỉ chạy trên một luân nên không cần phải chờ
# class Loading_screen(State):
#     def __init__(self, game) -> None:
#         super().__init__(game)
#         self.draw

#     def update(self):
#         if self.prev_state != None:
#             pygame.time.wait(2000)
#             new_state = LevelTest(self.game)
#             new_state.enter_state()
#         else:
#             new_state = Main_menu(self.game)
#             new_state.enter_state()

#     def get_event(self, event):
#         pass

#     def draw(self, surface): # type: ignore
#         surface.fill("black")
#         # self.game.draw_text("LOADING", "white", 30, surface, (self.game.SCREEN_WIDTH_TILES/2)*self.game.TILE_SIZE, (self.game.SCREEN_HEIGHT_TILES/2)*self.game.TILE_SIZE)