
from typing import Any

from loot import LootPool
from systems.interaction_manager import InteractionObject
from systems.level_manager import DifficultyLevel, DoorConfig, DoorType, LevelConfig, LootPoolConfig, RegionGeneratorConfig, RoomType, WaveManagerConfig
from utils import pixil


template = {
    # Độ khó DỄ
    DifficultyLevel.EASY: LevelConfig(
        region_generator=RegionGeneratorConfig(
            has_trap=0.2,       # Ít bẫy
            has_obstacle=0.3,    # Ít chướng ngại vật
            has_chest=0.7,       # Nhiều rương
            has_pot=0.8          # Nhiều bình
        ),
        wave_manager=WaveManagerConfig(
            wave_interval=2,     # 2 giây giữa các đợt
            max_wave_count=5,    # Tối đa 2 đợt
            max_wave_entities=29,  # Tối đa 4 quái mỗi đợt
            enemy_types={
                'weak_monster': 0.7,
                'bomb': 0.3,
                # 'strong_monster': 0.0
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
            wave_interval=1,
            max_wave_count=3,
            max_wave_entities=10,
            enemy_types={
                'weak_monster': 0.4,
                'bomb': 0.3,
                # 'strong_monster': 0.3
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
            max_wave_entities=10,
            enemy_types={
                'weak_monster': 0.1,
                'bomb': 0.3,
                # 'strong_monster': 0.6
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


class Door(InteractionObject):
    import levels.level as L

    def __init__(self, level: "L.Level", pos) -> None:
        super().__init__(level, 'door', 45)
        self.image = pixil.Pixil.load(
            r"game-assets/graphics/pixil/DOOR_SPRITE.pixil").frames[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.door_config: DoorConfig = DoorConfig(
            difficulty=DifficultyLevel.NORMAL,
            door_type=DoorType.NORMAL
        )

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def on_interact(self):
        if self.level.level_index < 3:
            level_config = template[DifficultyLevel.EASY]
        elif self.level.level_index < 6:
            level_config = template[DifficultyLevel.NORMAL]
        elif self.level.level_index < 9:
            level_config = template[DifficultyLevel.HARD]
        else:
            level_config = template[DifficultyLevel.BOSS]

        self.level.next_level(level_config)
