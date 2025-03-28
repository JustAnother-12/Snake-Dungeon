from __future__ import annotations
import pygame
from Stats import Stats
from level_component import Chests, Coins, Food_Group, Keys, Pot_group, Traps, Walls, Bomb_group, Obstacle_group, Food_Group
from states.GameOver_menu import GameOver_menu
from states.state import State
from states.Pause_menu import Pause_menu
from pixil import Pixil
import constant
import random
from logic.help import check_collision
from HUD import HUD

MAP_WIDTH = (
    constant.SCREEN_WIDTH_TILES -
    constant.LEFT_RIGHT_BORDER_TILES * 2 - constant.WALL_TILES * 2
) * constant.TILE_SIZE
MAP_HEIGHT = (
    constant.SCREEN_HEIGHT_TILES -
    constant.TOP_BOTTOM_BORDER_TILES * 2 - constant.WALL_TILES * 2
) * constant.TILE_SIZE
MAP_LEFT = (constant.LEFT_RIGHT_BORDER_TILES +
            constant.WALL_TILES) * constant.TILE_SIZE
MAP_RIGHT = MAP_LEFT + MAP_WIDTH
MAP_TOP = (constant.TOP_BOTTOM_BORDER_TILES +
           constant.WALL_TILES) * constant.TILE_SIZE
MAP_BOTTOM = MAP_TOP + MAP_HEIGHT


class LevelTest(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()

    def init(self):
        from Player import Snake, GreenSnake, OrangeSnake, GraySnake
        self.remove(self.sprites())
        self.snake = GraySnake(self, 5)
        self.foods = Food_Group(self)
        self.traps = Traps(self, 10)
        self.keys = Keys(self, 2)
        self.coins = Coins(self)
        self.walls = Walls()
        self.obstacles = Obstacle_group(self, 3)
        self.chests = Chests(self, 3)
        self.bombs = Bomb_group(self, 5)
        self.pots = Pot_group(self, 20)
        self.hud = HUD(self.snake.gold, len(self.snake), self.snake.keys)
        self.is_paused = False
        self.add(self.hud, self.walls, self.traps, self.obstacles,
                 self.foods, self.chests, self.pots, self.coins, self.bombs, self.keys, self.snake)

    def reset(self):
        # self.remove(self.hud,self.walls, self.traps,self.obstacles, self.snake, self.food, self.chests, self.coins, self.bombs, self.keys)
        self.init()

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(Pause_menu(self.game))

        if self.is_paused or self.snake.isDeath:
            return
        self.snake.update()
        self.traps.update()
        self.keys.update()
        self.chests.update()
        self.pots.update()
        self.bombs.update()
        self.coins.update()
        self.foods.update()
        self.hud.update(self.snake.gold, len(
            self.snake.blocks), self.snake.keys)
        
        Stats.setValue("LENGTH", len(self.snake.blocks))

        if self.snake.isDeath:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(GameOver_menu(self.game))

    def draw_grid(self, surface: pygame.Surface):
        surface.fill("black")
        pygame.draw.rect(
            surface,
            (51, 54, 71),
            (
                MAP_LEFT,
                MAP_TOP,
                MAP_WIDTH,
                MAP_HEIGHT,
            ),
        )
        for x in range(MAP_LEFT, MAP_RIGHT + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100),
                             (x, MAP_TOP), (x, MAP_BOTTOM))
        for y in range(MAP_TOP, MAP_BOTTOM + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100),
                             (MAP_LEFT, y), (MAP_RIGHT, y))

    def draw_stamina(self, surface: pygame.Surface):
        if self.snake.stamina > 0:
            pygame.draw.rect(
                surface, "cyan", (6.5*constant.TILE_SIZE, 2.5 *
                                  constant.TILE_SIZE+4, self.snake.stamina * 128 // 100, 24)
            )
            pygame.draw.rect(
                surface, (192, 237, 250), (6.5*constant.TILE_SIZE, 2.5 *
                                           constant.TILE_SIZE+4, self.snake.stamina * 128 // 100, 4)
            )
        pygame.draw.rect(
            surface, (133, 133, 133), (6.5*constant.TILE_SIZE-4, 2.5*constant.TILE_SIZE,
                                       self.snake.max_stamina * 128 // 100 + 6, 32), 4, 0, 0, 10, 0, 10
        )

    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        self.draw_grid(surface)
        self.draw_stamina(surface)

        return super().draw(surface)


def main():
    pass


if __name__ == "__main__":
    main()
