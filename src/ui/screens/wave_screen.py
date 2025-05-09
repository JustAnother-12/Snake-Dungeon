

from config import constant
from ui.elements.text import TextElement
from ui.screens.state import State
from utils.help import Share


class WaveScreen(State):
    from levels import level

    def __init__(self, game, level_: "level.Level", message: str = "") -> None:
        super().__init__(game)
        self.game = game

        self.level_text = TextElement(f"wave {level_.wave_manager.current_wave_index} / {len(level_.wave_manager.waves)}", "white", 35, constant.SCREEN_WIDTH_TILES /
                                      2 * game.TILE_SIZE, constant.SCREEN_HEIGHT_TILES / 2 * game.TILE_SIZE - 50, "center")
        self.level_ = level_
        self.duration = self.level_.wave_manager.waves[self.level_.wave_manager.current_wave_index].delay

        self.count = TextElement("wave in " + str(self.duration), "white", 20, constant.SCREEN_WIDTH_TILES /
                                 2 * game.TILE_SIZE, constant.SCREEN_HEIGHT_TILES / 2 * game.TILE_SIZE, "center")

        # self.add(self.text)
        self.add(self.count)
        self.add(self.level_text)

    def update(self):
        self.duration -= Share.clock.get_time() / 1000
        self.count.set_text(f"Starting in {int(self.duration) + 1}")
        if self.duration <= 0:
            self.game.state_stack.pop()
            self.game.state_stack[-1].visible = True


    # chuyển hướng đến cho level
    def reset(self):
        self.game.state_stack.pop()
        self.level_.reset()
