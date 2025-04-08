from dataclasses import dataclass, field
from enum import Enum
import random
from typing import List, Dict, Any, Optional

from entities.items.item_registry import ItemRegistry
from levels import region_generator
from levels.components import chest
from loot import LootPool

class DifficultyLevel(Enum):
    EASY = "EASY"
    NORMAL = "NORMAL"
    HARD = "HARD"
    BOSS = "BOSS"

class RoomType(Enum):
    NORMAL = "NORMAL"     # Phòng chiến đấu thông thường
    SHOP = "SHOP"         # Phòng cửa hàng
    TREASURE = "TREASURE" # Phòng chứa rương báu
    KEY = "KEY"           # Phòng chứa chìa khóa
    BOSS = "BOSS"         # Phòng chứa boss

class DoorType(Enum):
    NORMAL = "NORMAL"     # Cửa thông thường
    SHOP = "SHOP"         # Cửa dẫn đến cửa hàng
    TREASURE = "TREASURE" # Cửa dẫn đến phòng chứa rương
    KEY = "KEY"           # Cửa dẫn đến phòng chìa khóa
    BOSS = "BOSS"         # Cửa dẫn đến phòng boss

@dataclass
class RegionGeneratorConfig:
    has_trap: float
    has_obstacle: float
    has_chest: float
    has_pot: float

@dataclass
class WaveManagerConfig:
    wave_interval: int
    max_wave_count: int
    max_wave_entities: int
    enemy_types: dict[str, float]  # Tỉ lệ xuất hiện của các loại quái vật

@dataclass
class LootPoolConfig:
    chest: LootPool
    pot: LootPool
    enemy: LootPool

@dataclass
class DoorConfig:
    door_type: DoorType
    difficulty: DifficultyLevel
    locked: bool = False

@dataclass
class LevelConfig:
    region_generator: RegionGeneratorConfig
    wave_manager: WaveManagerConfig
    loot_pool: LootPoolConfig
    room_type: RoomType = RoomType.NORMAL
    door_configs: list[DoorConfig] = field(default_factory=list)


class LevelManager:
    """
    Quản lý các màn chơi trong game.
    - Tạo các màn chơi với độ khó và loại phòng khác nhau
    - Quản lý chuyển đổi giữa các màn chơi
    - Tạo cửa để người chơi lựa chọn
    """
    
    def __init__(self):
        self.current_level_index = 0
        self.levels: List[LevelConfig] = []
        
        # Các template cấu hình theo độ khó
        self.difficulty_templates = self._create_difficulty_templates()

    def _create_difficulty_templates(self) -> Dict[DifficultyLevel, LevelConfig]:
        """Khởi tạo các template cấu hình theo độ khó"""
        return {
            # Độ khó DỄ
            DifficultyLevel.EASY: LevelConfig(
                region_generator=RegionGeneratorConfig(
                    has_trap=0.2,       # Ít bẫy
                    has_obstacle=0.3,    # Ít chướng ngại vật
                    has_chest=0.7,       # Nhiều rương
                    has_pot=0.8          # Nhiều bình
                ),
                wave_manager=WaveManagerConfig(
                    wave_interval=5,     # 5 giây giữa các đợt
                    max_wave_count=2,    # Tối đa 2 đợt
                    max_wave_entities=4, # Tối đa 4 quái mỗi đợt
                    enemy_types={
                        'weak_monster': 0.7,
                        'bomb': 0.3,
                        'strong_monster': 0.0
                    }
                ),
                loot_pool=LootPoolConfig(
                    chest=LootPool((10, 45, 30, 15, 0, 0, 0), (70, 25, 5)),
                    pot=LootPool((10, 45, 30, 15, 0, 0, 0), (70, 25, 5)),
                    enemy=LootPool((10, 45, 30, 15, 0, 0, 0), (70, 25, 5))
                )
            ),
            
            # Độ khó THƯỜNG
            DifficultyLevel.NORMAL: LevelConfig(
                region_generator=RegionGeneratorConfig(
                    has_trap=0.4,
                    has_obstacle=0.5,
                    has_chest=0.5,
                    has_pot=0.6
                ),
                wave_manager=WaveManagerConfig(
                    wave_interval=4,
                    max_wave_count=3,
                    max_wave_entities=5,
                    enemy_types={
                        'weak_monster': 0.4,
                        'bomb': 0.3,
                        'strong_monster': 0.3
                    }
                ),
                loot_pool=LootPoolConfig(
                    chest=LootPool((5, 30, 25, 15, 15, 10, 0), (50, 35, 15)),
                    pot=LootPool((5, 30, 25, 15, 15, 10, 0), (50, 35, 15)),
                    enemy=LootPool((5, 30, 25, 15, 15, 10, 0), (50, 35, 15))
                )
            ),
            
            # Độ khó KHÓ
            DifficultyLevel.HARD: LevelConfig(
                region_generator=RegionGeneratorConfig(
                    has_trap=0.7,
                    has_obstacle=0.6,
                    has_chest=0.4,
                    has_pot=0.5
                ),
                wave_manager=WaveManagerConfig(
                    wave_interval=3,
                    max_wave_count=4,
                    max_wave_entities=6,
                    enemy_types={
                        'weak_monster': 0.1,
                        'bomb': 0.3,
                        'strong_monster': 0.6
                    }
                ),
                loot_pool=LootPoolConfig(
                    chest=LootPool((0, 15, 10, 15, 25, 25, 10), (30, 40, 30)),
                    pot=LootPool((0, 15, 10, 15, 25, 25, 10), (30, 40, 30)),
                    enemy=LootPool((0, 15, 10, 15, 25, 25, 10), (30, 40, 30))
                )
            ),
            
            # Độ khó BOSS
            DifficultyLevel.BOSS: LevelConfig(
                region_generator=RegionGeneratorConfig(
                    has_trap=0.6,
                    has_obstacle=0.3,
                    has_chest=1.0,  # Boss luôn có rương
                    has_pot=0.3
                ),
                wave_manager=WaveManagerConfig(
                    wave_interval=0,  # Boss xuất hiện ngay lập tức
                    max_wave_count=1,  # Chỉ có 1 đợt boss
                    max_wave_entities=1,  # Chỉ có 1 boss
                    enemy_types={
                        'boss': 1.0  # 100% là boss
                    }
                ),
                loot_pool=LootPoolConfig(
                    chest=LootPool((0, 0, 10, 20, 30, 30, 10), (10, 40, 50)),
                    pot=LootPool((0, 0, 10, 20, 30, 30, 10), (10, 40, 50)),
                    enemy=LootPool((0, 0, 10, 20, 30, 30, 10), (10, 40, 50))
                ),
                room_type=RoomType.BOSS
            )
        }

    def generate_game(self, level_count: int = 10) -> None:
        """Tạo mới một game với số level được chỉ định"""
        self.levels = []
        self.current_level_index = 0
        
        # Xác định vị trí của các boss level
        boss_positions = self._generate_boss_positions(level_count)
        
        # Tạo các level thông thường
        for i in range(level_count):
            if i in boss_positions:
                # Level boss
                self.levels.append(self._copy_level_config(self.difficulty_templates[DifficultyLevel.BOSS]))
            else:
                # Level thường với độ khó tăng dần
                if i < 3:  # 3 level đầu luôn dễ
                    difficulty = DifficultyLevel.EASY
                elif i < level_count - 3:  # Phần giữa tăng dần độ khó
                    difficulties = [DifficultyLevel.EASY, DifficultyLevel.NORMAL, DifficultyLevel.HARD]
                    weights = [max(0, 5-i//3), 2+i//3, i//3]  # Càng về sau càng khó
                    difficulty = random.choices(difficulties, weights=weights, k=1)[0]
                else:  # 3 level cuối luôn khó
                    difficulty = DifficultyLevel.HARD
                    
                self.levels.append(self._copy_level_config(self.difficulty_templates[difficulty]))
    
    def _generate_boss_positions(self, level_count: int) -> List[int]:
        """Tạo vị trí của các boss level"""
        positions = []
        next_boss = random.randint(3, 5)  # Boss đầu tiên xuất hiện sau 3-5 level
        
        while next_boss < level_count:
            positions.append(next_boss)
            next_boss += random.randint(3, 5)  # Boss tiếp theo cách 3-5 level
            
        return positions
    
    def _copy_level_config(self, template: LevelConfig) -> LevelConfig:
        """Tạo bản sao của một template config để tránh thay đổi template gốc"""
        # Tạo bản sao của RegionGeneratorConfig
        region_config = RegionGeneratorConfig(
            has_trap=template.region_generator.has_trap,
            has_obstacle=template.region_generator.has_obstacle,
            has_chest=template.region_generator.has_chest,
            has_pot=template.region_generator.has_pot
        )
        
        # Tạo bản sao của WaveManagerConfig
        wave_config = WaveManagerConfig(
            wave_interval=template.wave_manager.wave_interval,
            max_wave_count=template.wave_manager.max_wave_count,
            max_wave_entities=template.wave_manager.max_wave_entities,
            enemy_types=template.wave_manager.enemy_types.copy()
        )
        
        # Tạo bản sao của LootPoolConfig
        # LootPool là immutable nên không cần deep copy
        loot_config = LootPoolConfig(
            chest=template.loot_pool.chest,
            pot=template.loot_pool.pot,
            enemy=template.loot_pool.enemy
        )
        
        # Tạo LevelConfig mới
        return LevelConfig(
            region_generator=region_config,
            wave_manager=wave_config,
            loot_pool=loot_config,
            room_type=template.room_type
        )
        
    def get_current_config(self) -> Optional[LevelConfig]:
        """Lấy cấu hình của màn chơi hiện tại"""
        if 0 <= self.current_level_index < len(self.levels):
            return self.levels[self.current_level_index]
        return None
    
    def complete_level(self) -> List[DoorConfig]:
        """
        Đánh dấu level hiện tại là đã hoàn thành và tạo các cửa.
        Trả về danh sách các cửa được tạo.
        """
        # Kiểm tra xem còn level tiếp theo không
        if self.current_level_index >= len(self.levels) - 1:
            return []
        
        current_level = self.levels[self.current_level_index]
        next_level_index = self.current_level_index + 1
        next_level = self.levels[next_level_index]
        
        # Tạo danh sách các cửa
        doors = []
        
        # Nếu level tiếp theo là boss, chỉ có một cửa dẫn tới boss
        if next_level.room_type == RoomType.BOSS:
            doors.append(DoorConfig(
                door_type=DoorType.BOSS,
                difficulty=DifficultyLevel.BOSS,
                locked=True  # Cửa boss luôn khóa
            ))
        else:
            # Level thường: tạo 2-3 cửa với độ khó khác nhau
            door_count = random.randint(2, 3)
            
            # Danh sách độ khó có thể có
            difficulties = [DifficultyLevel.EASY, DifficultyLevel.NORMAL]
            if self.current_level_index > 2:  # Chỉ cho phép cửa khó sau level 3
                difficulties.append(DifficultyLevel.HARD)
                
            # Tạo các cửa
            for _ in range(door_count):
                difficulty = random.choice(difficulties)
                doors.append(DoorConfig(
                    door_type=DoorType.NORMAL,
                    difficulty=difficulty,
                    locked=difficulty != DifficultyLevel.EASY  # Cửa dễ không khóa
                ))
        
        # Lưu danh sách cửa vào level hiện tại
        current_level.door_configs = doors
        
        return doors
    
    def choose_door(self, door_index: int) -> Optional[LevelConfig]:
        """
        Chọn một cửa để tiến vào level tiếp theo.
        Trả về cấu hình của level tiếp theo.
        """
        # Kiểm tra chỉ số door_index hợp lệ
        current_level = self.levels[self.current_level_index]
        if not (0 <= door_index < len(current_level.door_configs)):
            return None
            
        # Lấy thông tin cửa được chọn
        door = current_level.door_configs[door_index]
        
        # Tăng level index
        self.current_level_index += 1
        
        # Nếu đã hết level
        if self.current_level_index >= len(self.levels):
            return None
        
        # Lấy level tiếp theo
        next_level = self.levels[self.current_level_index]
        
        # Nếu không phải boss level, cập nhật độ khó theo cửa
        if next_level.room_type != RoomType.BOSS:
            # Thay thế bằng template mới theo độ khó của cửa
            new_config = self._copy_level_config(self.difficulty_templates[door.difficulty])
            
            # Copy cấu hình mới vào level hiện tại
            next_level.region_generator = new_config.region_generator
            next_level.wave_manager = new_config.wave_manager
            next_level.loot_pool = new_config.loot_pool

        return next_level
    
    def is_game_complete(self) -> bool:
        """Kiểm tra xem game đã hoàn thành chưa"""
        return self.current_level_index >= len(self.levels)
