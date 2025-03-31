from __future__ import annotations
import pygame
from time import time

import config.constant as constant
from entities.items.TestItem import ShieldEntity
from entities.items.coin import CoinEntity
from entities.items.food import FoodEntity
from levels.components.bomb import BombGroup
from levels.components.chest import ChestGroup
from levels.components.floor_tile import Floor
from levels.components.food import FoodGroup
from levels.components.key import Keys
from levels.components.obstacle import Obstacle, Obstacle_group
from levels.components.pot import Pot, Pot_group
from levels.components.trap import Trap
from levels.components.wall import Wall, Walls
from stats import Stats
from systems.interaction_manager import InteractionManager
from ui.hud.HUD import HUD
from levels.region_generator import RegionGenerator
from ui.screens.game_over import GameOver_menu
from ui.screens.pause import Pause_menu
from ui.screens.state import State

# làm cho nó gọn để kế thừa
class Level(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()

    def init(self):
        from entities.Player import Snake, GreenSnake, OrangeSnake, GraySnake
        self.empty()
        self.is_paused = False
        self.is_finished = False
        self.timer = time() 
        self.interaction_manager = InteractionManager(self)

        self.remove(self.sprites())
        self.snake = GreenSnake(self, 5)
        # self.hud = HUD(self.snake.gold, len(self.snake), self.snake.keys)
        self.hud = HUD(self)
        self.wall_group = Walls()

        # self.foods = Food_Group(self)
        self.obstacle_group = pygame.sprite.Group()
        self.trap_group = pygame.sprite.Group()
        self.pot_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()

        # TODO: test
        for i in range(4):
            coin = CoinEntity(self)
            self.item_group.add(coin)
        
        for i in range(2):
            food = FoodEntity(self)
            self.item_group.add(food)
        
        self.item_group.add(ShieldEntity(self))

        # end test

        self.generator()

        self.add(
            Floor(),
            self.obstacle_group,
            self.trap_group,
            self.pot_group,
            
            self.wall_group,
            self.snake,
            self.item_group,
            self.hud,
            
        )
        
    def generator(self):

        region_generator = RegionGenerator()
        # Make wall

        
        # Make obstacle
        self.obstacle_group.empty()
        for x, y in region_generator.obstacles_initpos:
            self.obstacle_group.add(Obstacle(self, (x, y)))
        
        # Make trap
        self.trap_group.empty()
        for x, y in region_generator.traps_initpos:
            self.trap_group.add(Trap(self, (x, y)))
        
        # Make pot
        self.pot_group.empty()
        for x, y in region_generator.pots_initpos:
            self.pot_group.add(Pot(self, (x, y)))

    def reset(self):
        self.init()
    
    def __dev_test(self):
        # TODO: nhớ bỏ cái này nếu test xong
        # tự tạo lại map khi nhấn phím
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_r]:
            self.generator()

    def handle_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(Pause_menu(self.game))
        
        self.interaction_manager.handle_input()
        
    def update(self):

        self.__dev_test()

        if self.snake.isDeath:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(GameOver_menu(self.game))
        
        self.handle_input()

        super().update()


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
        # self.draw_grid(surface)
        self.draw_stamina(surface)

        t = super().draw(surface)
        self.interaction_manager.draw(surface)
        return t
