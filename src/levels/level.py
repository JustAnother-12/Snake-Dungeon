from enum import Enum
import importlib
import random
import pygame

import config.constant as constant
from entities.items.consumable.energy_drink import EnergyDrinkEntity
from entities.items.consumable.fire_bomb_item import FireBombStack
from entities.items.consumable.resistance_potion import ResistancePotionEntity
from entities.items.consumable.celestine_fragment import CelestineFragmentEntity
from entities.items.consumable.bomb_item import BombEntity, BombStack
from entities.items.consumable.speed_potion import SpeedPotionEntity
from entities.items.consumable.reverse import ReverseEntity
from entities.items.consumable.molotov import MolotovStack
from entities.items.instant.gale_essence import GaleEssenceEntity
from entities.items.instant.coin import CoinEntity
from entities.items.instant.food import FoodEntity
from entities.items.instant.key import KeyEntity
from entities.items.instant.water_essence import WaterEssenceEntity
from entities.items.equipment.time_efficiency import TimeEfficiencyEntity
from entities.items.equipment.ouroboros import OuroborosEntity
from entities.items.equipment.blood_bomb_devil import BloodBombDevilEntity, BloodBombDevilStack
from entities.items.equipment.hephaestus_blood import HephaestusBloodEntity
from entities.items.equipment.midas_blood import MidasBloodStack
from entities.items.equipment.fire_gem_amulet import FireGemAmuletEntity
from entities.items.equipment.trail_of_flame import FlameTrailEntity
from entities.items.skill.ghost_body import GhostEntity
from entities.items.skill.ritual_dagger import RitualDaggerEntity
from entities.items.skill.thanos import ThanosEntity, ThanosItemStack
from entities.items.skill.gun_devil_contract import GunEntity
from entities.items.skill.dragon_breath import DragonBreathStack
from entities.projectile import Projectile
from levels.components.bomb import Bomb
from levels.components.chest import Chest
from levels.components.door import Door
from levels.components.floor_tile import Floor
from levels.components.obstacle import Obstacle
from levels.components.pot import Pot
from levels.components.trap import Trap
from levels.components.wall import Walls
from stats import Stats
from systems.interaction_manager import InteractionManager
from systems.level_manager import LevelConfig, LevelManager
from systems.wave_manager import Wave, WaveManager
from ui.hud.HUD import HUD
from levels.region_generator import RegionGenerator
from ui.screens.game_over import GameOver_menu
from ui.screens.pause import Pause_menu
from ui.screens.room_cleared import RoomCleared
from ui.screens.state import NestedGroup, State
from ui.screens.title_screen import TitleScreen
from utils.help import Share
from levels.shop import Shop_level


class LevelStatus(Enum):
    CREATED = 0
    PLAYING = 1
    GAME_OVER = 2
    ROOM_CLEARED = 3
    PAUSED = 4
    ROOM_COMPLETED = 5

# làm cho nó gọn để kế thừa
class Level(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        from entities.Player import Snake
        self.level_manager = LevelManager()
        self.level_manager.generate_game(5)
        self.snake_history: list[Snake] = []

        self.wall_group = Walls()
        self.obstacle_group = pygame.sprite.Group()
        self.trap_group = pygame.sprite.Group()
        self.pot_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.snake_group = NestedGroup()
        self.fire_group = pygame.sprite.Group()
        self.snake = Snake(self, 5)
        # TODO: nhớ xóa
        self.snake.inventory.add_item(DragonBreathStack())
        self.snake.inventory.add_item(FireBombStack(5))
        self.snake.inventory.add_item(MolotovStack(5))

        self.hud = HUD(self)
        self.interaction_manager = InteractionManager(self)

        self.snake_group.add(self.snake)
        self.wave_manager = WaveManager(self)
        self.shop = Shop_level(self)

        room_config = self.level_manager.get_current_config()
        if not room_config is None:
            self.create_config_room(room_config)
            self.generator()

        self.add(
            Floor(),
            self.wall_group,
            self.obstacle_group,
            self.trap_group,
            self.pot_group,
            self.fire_group,
            self.item_group,
            self.snake_group,
            self.hud,
            self.bomb_group
        )
    
    def create_config_room(self, room_config: LevelConfig):
        # self.snake_history.append(self.snake.copy())
        # room_config = self.level_manager.get_current_config()
        # if room_config is None:
        #     return
        region_generator = room_config.region_generator
        self.region_generator = RegionGenerator(
            has_trap=random.random() < region_generator.has_trap,
            has_obstacle=random.random() < region_generator.has_obstacle,
            has_pot=random.random() < region_generator.has_pot,
            has_chest=random.random() < region_generator.has_chest,
        )

        self.wave_manager = WaveManager(self)
        wave_config = room_config.wave_manager
        print(wave_config)

        for i in range(wave_config.max_wave_count):
            entities_config = {
                "monster": 0,
                "bomb": 0,
                "trap": 0,
                "obstacle": 0,
            }

            enemy_count = random.randint(0, wave_config.max_wave_entities)
            for _ in range(enemy_count):
                entity_type = random.choice(list(entities_config.keys()))
                entities_config[entity_type] += 1
            

            wave = Wave(
                entities_config=entities_config,
                delay=wave_config.wave_interval
            )
            self.wave_manager.add_wave(wave)

        
    def generator(self):
        self.level_status = LevelStatus.CREATED

        self.region_generator = RegionGenerator()
        self.snake.is_curling = True
        for i, v in enumerate(self.snake._block_positions):
            self.snake._block_positions[i] = pygame.Vector2((constant.SCREEN_WIDTH_TILES // 2) * constant.TILE_SIZE, constant.MAP_BOTTOM - constant.TILE_SIZE)
            self.snake.blocks[i].pos = self.snake._block_positions[i]

        # Make wall
        
        # Make obstacle
        self.obstacle_group.empty()
        for x, y in self.region_generator.obstacles_initpos:
            self.obstacle_group.add(Obstacle(self, (x, y)))
        
        # Make trap
        self.trap_group.empty()
        for x, y in self.region_generator.traps_initpos:
            self.trap_group.add(Trap(self, (x, y)))
        
        # Make pot
        self.pot_group.empty()
        for x, y in self.region_generator.pots_initpos:
            self.pot_group.add(Pot(self, (x, y)))
                
        self.item_group.add(BloodBombDevilEntity(self))
        # for i in range(3):
        #     bomb = BombEntity(self, quantity=random.randint(2,4))
        #     self.item_group.add(bomb)
        self.item_group.add(RitualDaggerEntity(self))
        self.item_group.add(HephaestusBloodEntity(self))
        self.item_group.add(FireGemAmuletEntity(self))
        self.item_group.add(GunEntity(self))
        self.item_group.add(FlameTrailEntity(self))
        # self.item_group.add(CelestineFragmentEntity(self))
        # self.item_group.add(EnergyDrinkEntity(self))
        # # self.item_group.add(ThanosEntity(self))
        # for i in range(2):
        #     self.item_group.add(ReverseEntity(self, quantity=random.randint(2,4)))
        #     self.item_group.add(SpeedPotionEntity(self, quantity=random.randint(2,4)))

    def reset(self):
        Stats.reset()
        self.game.state_stack.pop()
        self.game.state_stack.append(Level(self.game))
        
    def get_event(self, event: pygame.Event):
        self.snake.inventory.handle_key_event(event)

    def handle_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(Pause_menu(self.game))
        # TODO: test xong thì xóa   
        if keys[pygame.K_p]:
            self.to_shop()
        if keys[pygame.K_r]:
            self.shop.reStock()
        
        self.interaction_manager.handle_input()
        
    def update(self):
        
        if self.level_status == LevelStatus.CREATED:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(TitleScreen(self.game, self, "PRESS MOVEMENT KEYS TO START"))

        if self.level_status == LevelStatus.PLAYING:
            # self.wave_manager.update(Share.clock.get_time() / 1000)
            self.check_room_cleared()
        
        if self.level_status == LevelStatus.ROOM_CLEARED:
            self.game.state_stack.append(RoomCleared(self.game))
            doors = self.level_manager.complete_level()
            print(doors)
            if len(doors) == 0:
                self.game.state_stack[-1].visible = False
                self.game.state_stack.append(GameOver_menu(self.game))
                return 
            d = constant.MAP_RIGHT - constant.MAP_LEFT
            ix = 0
            for i in range(constant.MAP_LEFT, constant.MAP_RIGHT ,d // len(doors)):
                door = Door(self, (i, constant.MAP_TOP), ix)
                self.add(door)
                ix += 1
                if ix >= len(doors):
                    break

            self.level_status = LevelStatus.ROOM_COMPLETED
            print(self.region_generator.chests_initpos)
            for x, y in self.region_generator.chests_initpos if self.region_generator.chests_initpos else [((constant.SCREEN_WIDTH_TILES * constant.TILE_SIZE) // 2, (constant.SCREEN_HEIGHT_TILES * constant.TILE_SIZE) // 2)]:
                self.add(Chest(self, (x - constant.TILE_SIZE, y - constant.TILE_SIZE), False))
            # self.snake.auto_state = False
        
        # self.check_for_secret_input()
        
        self.handle_input()
        t = self.snake._will_go_out_of_bounds
        super().update()
        if self.snake._will_go_out_of_bounds and not t:
            Share.audio.set_sound_volume("hit_hurt", 0.5)
            Share.audio.play_sound('hit_hurt', 1)
    
    def check_room_cleared(self):
        if self.wave_manager.is_complete():
            self.level_status = LevelStatus.ROOM_CLEARED
            self.snake.auto_state = False

    def to_shop(self):
        self.snake.auto_state = False
        # xóa những phần tử cũ đi
        self.obstacle_group.empty()
        self.trap_group.empty()
        self.pot_group.empty()
        self.bomb_group.empty()
        self.item_group.empty()

        self.shop.init_Stock()
        self.shop.display_Stock()

        # # xóa cửa
        # for i in self.sprites():
        #     if isinstance(i, Door):
        #         i.kill()

        # next_ = self.level_manager.choose_door(index)
    
    def next_level(self, index: int):
        # xóa những phần tử cũ đi
        self.obstacle_group.empty()
        self.trap_group.empty()
        self.pot_group.empty()
        self.bomb_group.empty()
        self.item_group.empty()

        # xóa cửa
        for i in self.sprites():
            if isinstance(i, Door):
                i.kill()

        next_ = self.level_manager.choose_door(index)
    
        print(next_)
        if next_ is None:
            return
        self.create_config_room(next_)
        self.generator()
    
    def check_for_secret_input(self):
        SECRET_IMPUTS = [
            pygame.K_t, pygame.K_h, pygame.K_a, pygame.K_n,pygame.K_o,pygame.K_s
        ]
        input_keys = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                input_keys.append(event.key)

        if len(input_keys) > len(SECRET_IMPUTS):
            input_keys.pop(0)
        if input_keys == SECRET_IMPUTS:
            print("test")
            input_keys.clear()

    # def draw_grid(self, surface: pygame.Surface):
    #     surface.fill("black")
    #     pygame.draw.rect(
    #         surface,
    #         (51, 54, 71),
    #         (
    #             constant.MAP_LEFT,
    #             constant.MAP_TOP,
    #             constant.MAP_WIDTH,
    #             constant.MAP_HEIGHT,
    #         ),
    #     )
    #     for x in range(constant.MAP_LEFT, constant.MAP_RIGHT + 1, constant.TILE_SIZE):
    #         pygame.draw.line(surface, (100, 100, 100),
    #                          (x, constant.MAP_TOP), (x, constant.MAP_BOTTOM))
    #     for y in range(constant.MAP_TOP, constant.MAP_BOTTOM + 1, constant.TILE_SIZE):
    #         pygame.draw.line(surface, (100, 100, 100),
    #                          (constant.MAP_LEFT, y), (constant.MAP_RIGHT, y))


    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        # self.draw_grid(surface)

        t = super().draw(surface)
        self.interaction_manager.draw(surface)
        return t
