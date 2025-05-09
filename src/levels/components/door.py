
import random
from typing import Any

from loot import LootPool
from systems.interaction_manager import InteractionObject
from systems.level_manager import DifficultyLevel, DoorConfig, DoorType, LevelConfig, LootPoolConfig, RegionGeneratorConfig, RoomType, WaveManagerConfig
from utils import pixil


# shope
shope_template = LevelConfig(
    region_generator=RegionGeneratorConfig(
        has_trap=0.0,       # Không có bẫy
        has_obstacle=0.0,    # Không có chướng ngại vật
        has_chest=0.0,       # Không có rương
        has_pot=0.0          # Không có bình
    ),
    wave_manager=WaveManagerConfig(
        wave_interval=0,     # Không có đợt
        max_wave_count=0,    # Không có đợt
        max_wave_entities=0,  # Không có quái
        enemy_types={
            'weak_monster': 0.0,
            'bomb': 0.0,
            # 'strong_monster': 0.0
        }
    ),
    loot_pool=LootPoolConfig(
        chest=LootPool((0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0)),
        pot=LootPool((0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0)),
        enemy=LootPool((0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0))
    ),
    room_type=RoomType.SHOP
)

# cho nhung room nomal and boss
template = {
    # Độ khó DỄ
    DifficultyLevel.EASY: LevelConfig(
        region_generator=RegionGeneratorConfig(
            has_trap=0.2,       # Ít bẫy
            has_obstacle=0.5,    # Ít chướng ngại vật
            has_chest=0.7,       # Nhiều rương
            has_pot=0.8          # Nhiều bình
        ),
        wave_manager=WaveManagerConfig(
            wave_interval=2,     # 2 giây giữa các đợt
            max_wave_count=2,    # Tối đa 2 đợt
            max_wave_entities=3,  # Tối đa 4 quái mỗi đợt
            enemy_types={
                'weak_monster': 0.7,
                'bomb': 0.3,
                # 'strong_monster': 0.0
            }
        ),
        loot_pool=LootPoolConfig(
            chest=LootPool((60, 63, 42,14, 12, 0, 0, 0), (70, 25, 5)),
            pot=LootPool((60, 63, 42,14, 12, 0, 0, 0), (70, 25, 5)),
            enemy=LootPool((60, 63, 42,14, 12, 0, 0, 0), (70, 25, 5))
        )
    ),

    # Độ khó THƯỜNG
    DifficultyLevel.NORMAL: LevelConfig(
        region_generator=RegionGeneratorConfig(
            has_trap=0.5,
            has_obstacle=0.7,
            has_chest=0.7,
            has_pot=0.8
        ),
        wave_manager=WaveManagerConfig(
            wave_interval=1,
            max_wave_count=3,
            max_wave_entities=3,
            enemy_types={
                'weak_monster': 0.4,
                'bomb': 0.3,
                # 'strong_monster': 0.3
            }
        ),
        loot_pool=LootPoolConfig(
            chest=LootPool((5, 30, 20, 10, 15, 10, 10, 0), (50, 35, 15)),
            pot=LootPool((5, 30, 20, 10, 15, 10, 10, 0), (50, 35, 15)),
            enemy=LootPool((5, 30, 20, 10, 15, 10, 10, 0), (50, 35, 15))
        )
    ),

    # Độ khó KHÓ
    DifficultyLevel.HARD: LevelConfig(
        region_generator=RegionGeneratorConfig(
            has_trap=0.7,
            has_obstacle=0.8,
            has_chest=0.8,
            has_pot=1.0
        ),
        wave_manager=WaveManagerConfig(
            wave_interval=3,
            max_wave_count=4,
            max_wave_entities=4,
            enemy_types={
                'weak_monster': 0.1,
                'bomb': 0.3,
                # 'strong_monster': 0.6
            }
        ),
        loot_pool=LootPoolConfig(
            chest=LootPool((0, 15, 10, 10, 10, 20, 25, 10), (30, 40, 30)),
            pot=LootPool((0, 15, 10, 10, 10, 20, 25, 10), (30, 40, 30)),
            enemy=LootPool((0, 15, 10, 10, 10, 20, 25, 10), (30, 40, 30))
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
            chest=LootPool((0, 0, 10, 5, 15, 30, 30, 10), (10, 40, 50)),
            pot=LootPool((0, 0, 10, 5, 15, 30, 30, 10), (10, 40, 50)),
            enemy=LootPool((0, 0, 10, 5, 15, 30, 30, 10), (10, 40, 50))
        ),
        room_type=RoomType.BOSS
    )
}


class Door(InteractionObject):
    import levels.level as L

    def __init__(self, level: "L.Level", pos, door_type: DoorType | None = None) -> None:
        super().__init__(level, 'go in', 45)
        # randome the door type
        # if door type is normal, set randomw difficulty base on level
        # if door type is boss, set difficulty to boss

        door_difficulty = DifficultyLevel.EASY

        if door_type is None:
            choices = [DifficultyLevel.EASY]
            # 3 so luong do kho
            s = level.max_level // 3

            if self.level.current_level < s:
                choices.append(DifficultyLevel.NORMAL)
            elif self.level.current_level < s * 2:
                choices.append(DifficultyLevel.HARD)
            else:
                choices.append(DifficultyLevel.BOSS)

            door_type = DoorType.NORMAL if self.level.current_level < s * 2 else DoorType.BOSS
            door_difficulty = random.choice(choices)

        self.door_config: DoorConfig = DoorConfig(
            difficulty=door_difficulty,
            door_type=door_type
        )

        if self.door_config.door_type == DoorType.SHOP:
            self.image = pixil.Pixil.load(
                r"game-assets/graphics/pixil/DOOR_SPRITE.pixil").frames[3]
        else:
            self.image = pixil.Pixil.load(
                r"game-assets/graphics/pixil/DOOR_SPRITE.pixil").frames[0]

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def on_interact(self):
        level_config = template[self.door_config.difficulty]
        if self.door_config.door_type == DoorType.SHOP:
            level_config = shope_template

        self.level.next_level(level_config)
