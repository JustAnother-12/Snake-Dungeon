from enum import Enum
import importlib
import random
import pygame

import config.constant as constant
from entities.items.skill.ghost_body import GhostEntity
from entities.items.instant.gale_essence import GaleEssenceEntity
from entities.items.instant.coin import CoinEntity
from entities.items.instant.food import FoodEntity
from entities.items.instant.key import KeyEntity
from entities.items.equipment.ouroboros import OuroborosEntity
from entities.items.equipment.time_efficiency import TimeEfficiencyEntity
from entities.items.comsumalbe.bomb_item import BombEntity
from entities.items.comsumalbe.speed_potion import SpeedPotionEntity
from entities.items.instant.water_essence import WaterEssenceEntity
from entities.items.comsumalbe.reverse import ReverseEntity
from entities.items.skill.ritual_dagger import RitualDaggerEntity
from entities.projectile import Projectile
from levels.components.bomb import Bomb
from levels.components.chest import ChestGroup
from levels.components.floor_tile import Floor
from levels.components.obstacle import Obstacle
from levels.components.pot import Pot
from levels.components.trap import Trap
from levels.components.wall import Walls
from stats import Stats
from systems.interaction_manager import InteractionManager
from systems.wave_manager import WaveManager
from ui.hud.HUD import HUD
from levels.region_generator import RegionGenerator
from ui.screens.game_over import GameOver_menu
from ui.screens.pause import Pause_menu
from ui.screens.room_cleared import RoomCleared
from ui.screens.state import NestedGroup, State
from ui.screens.title_screen import TitleScreen
from utils.help import Share


class LevelStatus(Enum):
    CREATED = 0
    PLAYING = 1
    GAME_OVER = 2
    ROOM_CLEARED = 3
    PAUSED = 4

# làm cho nó gọn để kế thừa
class Level(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()
        

    def init(self):
        from entities.Player import Snake

        # Clear previous state
        self.empty()
        self.remove(self.sprites())
        
        # Game state
        self.level_status = LevelStatus.CREATED
        
        # Main entities
        self.snake_group = NestedGroup()
        self.snake = Snake(self, 5)
        self.snake_group.add(self.snake)

        self.hud = HUD(self)
        self.interaction_manager = InteractionManager(self)
        self.wave_manager = WaveManager(self)
        
        # Environment groups
        self.wall_group = Walls()
        self.obstacle_group = pygame.sprite.Group()
        self.trap_group = pygame.sprite.Group()
        self.pot_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        
        # Items
        self.item_group = pygame.sprite.Group()
        # self.item_group.add(ShieldEntity(self))
        
        # Generate level components
        
        # Add all components to the level
        self.add(
            Floor(),
            self.wall_group,
            self.obstacle_group,
            self.trap_group,
            self.pot_group,
            # self.snake,
            self.snake_group,
            self.item_group,
            self.hud,
            self.bomb_group
        )

        self.generator()
        
    def generator(self):

        region_generator = RegionGenerator()
        # Make wall

        self.wave_manager.generate_waves()
        
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

        # tạo bom
        # self.bomb_group.empty()
        # for i in range(3):
        #     self.bomb_group.add(Bomb(self))
            
        # # tạo monster
        # from entities.Monster import Monster
        # for i in range(3):
        #     monster = Monster(self, random.randint(5, 8))
        #     monster.set_player_reference(self.snake)
        #     self.snake_group.add(monster)
        
        # # tạo item
        # for i in range(10):
        #     coin = CoinEntity(self)
        #     self.item_group.add(coin)
        
        # for i in range(10):
        #     food = FoodEntity(self)
        #     self.item_group.add(food)
        
        # for i in range(2):
        #     gale_essence = GaleEssenceEntity(self)
        #     self.item_group.add(gale_essence)

        # for i in range(2):
        #     water_essence = WaterEssenceEntity(self)
        #     self.item_group.add(water_essence)
            
        # for i in range(3):
        #     key = KeyEntity(self)
        #     self.item_group.add(key)

        for i in range(3):
            bomb = BombEntity(self, quantity=random.randint(2,4))
            self.item_group.add(bomb)
        
        # for i in range(1):
        #     item = GhostEntity(self)
        #     self.item_group.add(item)
        # for i in range(2):
        #     self.item_group.add(SpeedPotionEntity(self, quantity=random.randint(2,4)))
        
        # for i in range(1):
        #     self.item_group.add(RitualDaggerEntity(self))

        self.item_group.add(OuroborosEntity(self))
        for i in range(2):
            self.item_group.add(ReverseEntity(self, quantity=random.randint(2,4)))

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
        
        if self.level_status == LevelStatus.CREATED:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(TitleScreen(self.game, self, "PRESS MOVEMENT KEYS TO START"))
        
        self.__dev_test()

        if self.level_status == LevelStatus.PLAYING:
            self.wave_manager.update(Share.clock.get_time() / 1000)
            self.check_room_cleared()
            self.handle_input()
            t = self.snake._will_go_out_of_bounds
            super().update()
            if self.snake._will_go_out_of_bounds and not t:
                Share.audio.play_sound('hit_hurt', 1)
        
        if self.level_status == LevelStatus.ROOM_CLEARED:
            self.game.state_stack.append(RoomCleared(self.game))
            self.snake.auto_state = False
            self.is_finished = False
    
    def check_room_cleared(self):
        if self.wave_manager.is_complete():
            self.level_status = LevelStatus.ROOM_CLEARED
            self.snake.auto_state = False

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
