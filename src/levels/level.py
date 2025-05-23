from enum import Enum
import random
import pygame

import config.constant as constant
from entities.items.consumable.fire_bomb_item import FireBombStack
from entities.items.consumable.molotov import MolotovStack
from entities.items.equipment.blood_bomb_devil import BloodBombDevilEntity
from entities.items.equipment.credit_card import CreditCardStack
from entities.items.equipment.hephaestus_blood import HephaestusBloodEntity
from entities.items.equipment.fire_gem_amulet import FireGemAmuletEntity
from entities.items.equipment.midas_blood import MidasBloodEntity
from entities.items.equipment.trail_of_flame import FlameTrailEntity
from entities.items.instant.food import FoodEntity
from entities.items.skill.celestine_amulet import CelestineAmuletStack
from entities.items.skill.dragon_breath import DragonBreathStack
from entities.items.skill.gun_devil_contract import GunEntity
from entities.items.skill.ritual_dagger import RitualDaggerStack
from levels.components.chest import Chest
from levels.components.door import Door
from levels.components.floor_tile import Floor
from levels.components.obstacle import Obstacle
from levels.components.pot import Pot
from levels.components.trap import Trap
from levels.components.wall import Walls
from loot import LootPool
from stats import StatType, Stats
from systems.interaction_manager import InteractionManager
from systems.level_manager import DoorType, LevelConfig, LootPoolConfig, RegionGeneratorConfig, RoomType, WaveManagerConfig
from systems.wave_manager import Wave, WaveManager
from ui.hud.HUD import HUD
from levels.region_generator import RegionGenerator
from ui.screens.Instruction import Instruction
from ui.screens.count_down import Count_down
from ui.screens.pause import Pause_menu
from ui.screens.room_cleared import RoomCleared
from ui.screens.state import NestedGroup, State
from ui.screens.you_win import YouWin_menu
from utils.help import Share
from levels.shop import Shop_level


class LevelStatus(Enum):
    CREATED = 0
    PLAYING = 1
    GAME_OVER = 2
    ROOM_CLEARED = 3
    PAUSED = 4
    ROOM_COMPLETED = 5

class Level(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.module = True
        from entities.Player import Snake
        self.snake_history: list[Snake] = []
        self.max_level = 5
        self.current_level = 0

        self.wall_group = Walls()
        self.chest_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.trap_group = pygame.sprite.Group()
        self.pot_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        self.fire_bomb_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.snake_group = NestedGroup()
        self.fire_group = pygame.sprite.Group()
        self.snake = Snake(self, 5)
        

        # TODO: nhớ xóa
        # Stats.setValue(StatType.ENERGY_CAPACITY, 100)
        # self.snake.inventory.add_item(CelestineAmuletStack())
        # self.snake.inventory.add_item(FireBombStack(5))
        # self.snake.inventory.add_item(MolotovStack(5))
        # self.snake.inventory.add_item(CreditCardStack())
        # TODO: nhớ xóa
        
        self.hud = HUD(self)
        self.interaction_manager = InteractionManager(self)

        self.snake_group.add(self.snake)
        self.wave_manager = WaveManager(self)
        self.shop = Shop_level(self)

        # level đầu tiên lúc nào cũng giống nhau
        self._config: LevelConfig = LevelConfig(
            region_generator=RegionGeneratorConfig(0.3, 0.7, 1.0, 1.0),
            wave_manager=WaveManagerConfig(2, 1, 1, {
                "monster": 1
            }),
            loot_pool=LootPoolConfig(
                chest=LootPool((60, 63, 42,14, 12, 0, 0, 0), (70, 25, 5)),
                pot=LootPool((60, 63, 42,14, 12, 0, 0, 0), (70, 25, 5)),
                enemy=LootPool((60, 63, 42,14, 12, 0, 0, 0), (70, 25, 5))
            )
        )

        self.create_config_room(self._config)
        self.generator()

        self.add(
            Floor(),
            self.wall_group,
            self.obstacle_group,
            self.trap_group,
            self.pot_group,
            self.chest_group,
            self.fire_group,
            self.item_group,
            self.snake_group,
            self.hud,
            self.bomb_group,
            self.fire_bomb_group
        )

    def create_config_room(self, room_config: LevelConfig):
        region_generator = room_config.region_generator
        self.region_generator = RegionGenerator(
            has_trap=random.random() <= region_generator.has_trap,
            has_obstacle=random.random() <= region_generator.has_obstacle,
            has_pot=random.random() <= region_generator.has_pot,
            has_chest=random.random() <= region_generator.has_chest,
        )

        self.wave_manager = WaveManager(self)
        wave_config = room_config.wave_manager
        print(wave_config)
        

        for i in range(wave_config.max_wave_count):
            entities_config = {
                "monster": 0,
                "bomb": 0,
                "blocker": 0,
            }

            # enemy_count = random.randint(1, wave_config.max_wave_entities)
            enemy_count = wave_config.max_wave_entities
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

        # self.region_generator = RegionGenerator()
        self.snake.is_curling = True
        for i, v in enumerate(self.snake.blocks):
            self.snake._block_positions[i] = pygame.Vector2(
                (constant.SCREEN_WIDTH_TILES // 2) * constant.TILE_SIZE, constant.MAP_BOTTOM - constant.TILE_SIZE)
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

        # Make chests
        self.chest_group.empty()
        for x, y in self.region_generator.chests_initpos:
            self.chest_group.add(Chest(self, (x - constant.TILE_SIZE, y - constant.TILE_SIZE))) 

        # Make pot
        self.pot_group.empty()
        for x, y in self.region_generator.pots_initpos:
            self.pot_group.add(Pot(self, (x, y)))

        self.item_group.empty()

    def reset(self):
        Stats.reset()
        self.exit_state()
        Level(self.game).enter_state()

    def get_event(self, event: pygame.Event):
        self.snake.inventory.handle_key_event(event)

    def handle_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE]:
            Pause_menu(self.game).enter_state()

        self.interaction_manager.handle_input()

    def update(self):

        if self.level_status == LevelStatus.CREATED:
            Count_down(self.game, self).enter_state()
            if self.current_level == 0:
                Instruction(self.game, self).enter_state()
            Share.audio.play_music("level", -1, 2000)

        if self.level_status == LevelStatus.PLAYING:
            self.wave_manager.update(Share.clock.get_time() / 1000)
            self.check_room_cleared()

        if self.level_status == LevelStatus.ROOM_CLEARED:
            self._room_cleared()

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
        
    def _room_cleared(self):
        if self._config.room_type != RoomType.SHOP:
            RoomCleared(self.game).enter_state()

        # tạo random từ 2 -> 3 cửa
        doors = random.randint(2, 3)
        # nếu là shop | hoặc level cuối thì chỉ có 1 cửa
        if self._config.room_type == RoomType.SHOP or self.current_level >= self.max_level - 1:
            doors = 1
        shope_index = random.randint(0, doors - 1)
        if self._config.room_type == RoomType.SHOP or self.current_level >= self.max_level - 1: 
            shope_index = -1

        spacing = 128

        for index, x in enumerate(range(constant.MAP_LEFT + spacing, constant.MAP_RIGHT, spacing)):
            if index >= doors:
                break
            door = Door(self, (x, constant.MAP_TOP - 64),
                        DoorType.SHOP if index == shope_index else None)
            print(door)
            self.add(door)

        self.level_status = LevelStatus.ROOM_COMPLETED

        if self._config.room_type == RoomType.SHOP: return
        self.region_generator.get_reward_chest_region()
        for x, y in self.region_generator.reward_chests_initpos:
            self.chest_group.add(Chest(self, (x - constant.TILE_SIZE, y - constant.TILE_SIZE), False))

    def next_level(self, config: LevelConfig):
        if self.current_level >= self.max_level - 1:
            YouWin_menu(self.game).enter_state()
            Share.audio.stop_music()
            return

        self._config = config
        # xóa những phần tử cũ đi
        self.chest_group.empty()
        self.obstacle_group.empty()
        self.trap_group.empty()
        self.pot_group.empty()
        self.bomb_group.empty()
        self.fire_bomb_group.empty()
        self.item_group.empty()
        self.fire_group.empty()

        # xoa shop
        if hasattr(self, "shop"):
            self.shop.remove_Stock()

        # xóa cửa
        for i in self.sprites():
            if isinstance(i, Door):
                i.kill()

        if config.room_type == RoomType.SHOP:
            self.shop = Shop_level(self)
            self.shop.init_Stock()
            self.shop.display_Stock()
            self.level_status = LevelStatus.ROOM_CLEARED
            return

        self.current_level += 1
        self.create_config_room(config)
        self.generator()

    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        t = super().draw(surface)
        self.interaction_manager.draw(surface)
        return t
