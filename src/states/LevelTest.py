from __future__ import annotations
import pygame
from Stats import Stats
from level_components.Trap import Traps
from level_components.Chest import Chests
from level_components.Coin import Coins
from level_components.Key import Keys
from level_components.Pot import Pot_group
from level_components.Wall import Walls
from level_components.Bomb import Bomb_group
from level_components.Obstacle import Obstacle_group
from states import RoomCleared
from states.GameOver_menu import GameOver_menu
from states.state import State
from states.Pause_menu import Pause_menu
from states.RoomCleared import RoomCleared
import constant
from HUD import HUD
from region_generator import RegionGenerator
from level_components.Food import Food_Group
from time import time

class LevelTest(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()

    def init(self):
        from Player import Snake, GreenSnake, OrangeSnake, GraySnake
        self.remove(self.sprites())
        self.snake = Snake(self, 5)

        self.foods = Food_Group(self)

        self.region_generator = RegionGenerator()
        self.traps = Traps(self,self.region_generator.traps_initpos)
        self.chests = Chests(self, self.region_generator.chests_initpos)
        self.pots = Pot_group(self, self.region_generator.pots_initpos)
        self.obstacles = Obstacle_group(self, self.region_generator.obstacles_initpos)

        self.keys = Keys(self, 2)
        self.coins = Coins(self)
        self.bombs = Bomb_group(self, 5) 
        self.walls = Walls()
        
        self.hud = HUD(self.snake.gold, len(self.snake), self.snake.keys)
        self.is_paused = False
        self.is_finished = False
        self.timer = time() 
        self.add(self.hud, self.walls, self.traps, self.obstacles,
                 self.foods, self.chests, self.pots, self.coins, self.bombs, self.keys, self.snake)
        
    def reset_level(self):
        self.snake.auto_state, self.snake.manual_state = True, False
        self.timer = time()
        self.is_finished = False
        self.remove(self.foods, self.traps, self.chests, self.pots, self.obstacles, self.keys, self.coins, self.bombs, self.walls, self.snake)
        self.foods = Food_Group(self)

        self.region_generator = RegionGenerator()
        self.traps = Traps(self,self.region_generator.traps_initpos)
        self.chests = Chests(self, self.region_generator.chests_initpos)
        self.pots = Pot_group(self, self.region_generator.pots_initpos)
        self.obstacles = Obstacle_group(self, self.region_generator.obstacles_initpos)

        self.keys = Keys(self, 2)
        self.coins = Coins(self)
        self.bombs = Bomb_group(self, 5) 
        self.walls = Walls()
        self.add(self.foods, self.traps, self.chests, self.pots, self.obstacles, self.keys, self.coins, self.bombs, self.walls, self.snake)

    def reset(self):
        self.init()

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_r]:
            self.game.state_stack.append(RoomCleared(self.game))
            self.is_finished = True
            
        if self.is_finished:
            self.snake.auto_state, self.snake.manual_state = False, True
            # self.reset_level()
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

    def drawRoomCleared(self):
        pass

    def draw_grid(self, surface: pygame.Surface):
        surface.fill("black")
        pygame.draw.rect(
            surface,
            (51, 54, 71),
            (
                constant.MAP_LEFT,
                constant.MAP_TOP,
                constant.MAP_WIDTH,
                constant.MAP_HEIGHT,
            ),
        )
        for x in range(constant.MAP_LEFT, constant.MAP_RIGHT + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100),
                             (x, constant.MAP_TOP), (x, constant.MAP_BOTTOM))
        for y in range(constant.MAP_TOP, constant.MAP_BOTTOM + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100),
                             (constant.MAP_LEFT, y), (constant.MAP_RIGHT, y))

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
