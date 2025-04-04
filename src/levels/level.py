from __future__ import annotations
from operator import contains
import random
import pygame
from time import time

import config.constant as constant
from entities.Monster import AIMonster
from entities.items.bomb_item import BombEntity
from entities.items.TestItem import ShieldEntity
from entities.items.coin import CoinEntity
from entities.items.food import FoodEntity
from entities.items.key import KeyEntity
from entities.items.speed_boot import SpeedBootEntity
from levels.components.bomb import BombGroup
from levels.components.chest import ChestGroup
from levels.components.floor_tile import Floor
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
from ui.screens.room_cleared import RoomCleared
from ui.screens.state import State

# làm cho nó gọn để kế thừa
class Level(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()

    def init(self):
        from entities.Player import Snake, GreenSnake, OrangeSnake, GraySnake
        # Clear previous state
        self.empty()
        self.remove(self.sprites())
        
        # Game state
        self.is_paused = False
        self.is_finished = False
        self.timer = time()
        
        # Main entities
        self.snake = GreenSnake(self, 5)
        self.monster = AIMonster(self, 5, (constant.MAP_LEFT, constant.MAP_TOP))
        self.monster.set_player_reference(self.snake)
        self.hud = HUD(self)
        self.interaction_manager = InteractionManager(self)
        
        # Environment groups
        self.wall_group = Walls()
        self.obstacle_group = pygame.sprite.Group()
        self.trap_group = pygame.sprite.Group()
        self.pot_group = pygame.sprite.Group()
        self.bomb_group = BombGroup(self)
        
        # Items
        self.item_group = pygame.sprite.Group()
        # self.item_group.add(ShieldEntity(self))
        
        # Generate level components
        self.generator()
        
        # Add all components to the level
        self.add(
            Floor(),
            self.wall_group,
            self.obstacle_group,
            self.trap_group,
            self.pot_group,
            self.snake,
            self.monster,
            self.item_group,
            self.hud,
            self.bomb_group
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

        
        # tạo item
        for i in range(10):
            coin = CoinEntity(self)
            self.item_group.add(coin)
        
        for i in range(3):
            food = FoodEntity(self)
            self.item_group.add(food)
        
        for i in range(3):
            key = KeyEntity(self)
            self.item_group.add(key)

        for i in range(3):
            bomb = BombEntity(self, quantity=random.randint(2,4))
            self.item_group.add(bomb)
        
        for i in range(3):
            item = ShieldEntity(self)
            self.item_group.add(item)
        for i in range(3):
            self.item_group.add(SpeedBootEntity(self, quantity=random.randint(2,4)))

    def reset(self):
        self.init()
    
    def __dev_test(self):
        # TODO: nhớ bỏ cái này nếu test xong
        # tự tạo lại map khi nhấn phím
        # keys = pygame.key.get_just_pressed()
        # if keys[pygame.K_r]:
        #     # self.generator()
        #     self.is_finished = True
        pass

    def handle_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(Pause_menu(self.game))
        
        self.interaction_manager.handle_input()
        
    def update(self):

        self.__dev_test()

        if self.is_finished:
            self.game.state_stack.append(RoomCleared(self.game))
            self.snake.auto_state = False
            self.is_finished = False

        if self.snake.is_dead:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(GameOver_menu(self.game))
        
        Stats.setValue("LENGTH", len(self.snake))

        self.handle_input()

        super().update()

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


    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        # self.draw_grid(surface)

        t = super().draw(surface)
        self.interaction_manager.draw(surface)
        return t
