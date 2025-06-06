import random
from enum import Enum

import pygame

from config import constant
from entities.Monster import BlockerMonster, BombMonster, Monster
from ui.screens.wave_screen import WaveScreen


class WaveState(Enum):
    WAITING = 0
    SPAWNING = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Wave:
    def __init__(self, entities_config, delay=2.0, difficulty_modifier=1.0):
        """
        Create a wave of entities
        
        Args:
            entities_config: Dict mapping entity types to quantities
                e.g. {"monster": 3, "bomb": 2}
            delay: Delay in seconds before starting this wave
            difficulty_modifier: Multiplier for quantities based on difficulty
        """
        self.entities_config = entities_config
        self.delay = delay
        self.difficulty_modifier = difficulty_modifier
        self.state = WaveState.WAITING
        self.spawned_entities = []  # Track entities we spawn


class WaveManager:
    from levels import level as lv
    def __init__(self, level: "lv.Level"):
        self.level = level
        self.waves = []
        self.current_wave_index = 0
        self.timer = 0
        self.running = False
        self.spawn_cooldown = 0  # For gradual spawning
        self.spawn_interval = 0.5  # Time between individual spawns
    
    def add_wave(self, wave):
        """Add a wave to the sequence"""
        self.waves.append(wave)
    
    def start(self):
        """Start the wave sequence"""
        self.current_wave_index = 0
        self.timer = 0
        self.running = True
        # Register the first wave with delay
        self.show_countdown()
        if self.waves:
            self.waves[0].state = WaveState.WAITING
    
    def update(self, dt):
        """Update wave status, dt is time delta in seconds"""
        if not self.running or self.current_wave_index >= len(self.waves):
            return
        
        current_wave = self.waves[self.current_wave_index]
        
        # Handle different wave states
        if current_wave.state == WaveState.WAITING:
            # Wait for delay
            self.timer += dt
            if self.timer >= current_wave.delay:
                current_wave.state = WaveState.SPAWNING
                self.timer = 0
                self.spawn_cooldown = 0
        
        elif current_wave.state == WaveState.SPAWNING:
            # Spawn entities gradually for a more interesting experience
            self.spawn_cooldown -= dt
            if self.spawn_cooldown <= 0:
                if self._spawn_next_entity(current_wave):
                    self.spawn_cooldown = self.spawn_interval
                else:
                    # All entities spawned
                    current_wave.state = WaveState.IN_PROGRESS
        
        elif current_wave.state == WaveState.IN_PROGRESS:
            # Check if this wave is cleared (all monsters defeated)
            if self._is_wave_clear(current_wave):
                self.timer += dt
                if self.timer >= 1.0:  # Wait for 1 second before clearing
                    self.timer = 0
                    current_wave.state = WaveState.COMPLETED
                    self._play_wave_cleared_sound()
                    
                    # Move to next wave
                    self.current_wave_index += 1
                    self.timer = 0
                    
                    # Check if all waves completed
                    if self.current_wave_index >= len(self.waves):
                        self._handle_all_waves_completed()
                        return
                    
                    # Start next wave
                    self.waves[self.current_wave_index].state = WaveState.WAITING
                    self.show_countdown()
    
    def show_countdown(self):
        WaveScreen(self.level.game, self.level).enter_state()
    
    def _spawn_next_entity(self, wave):
        """Spawn the next entity from the wave config, return True if spawned"""
        remaining = {k: v for k, v in wave.entities_config.items() if v > 0}
        
        if not remaining:
            return False
            
        # Select an entity type to spawn
        entity_type = random.choice(list(remaining.keys()))
        
        # Spawn the entity
        entity = self._create_entity(entity_type)
        if entity:
            wave.spawned_entities.append(entity)
            wave.entities_config[entity_type] -= 1
            return True
            
        return False
    
    def is_valid_spawn_position(self, pos):
        """Check if the spawn position is valid"""
        # min distance from player
        min_distance = constant.TILE_SIZE * 5
        pos_ = pygame.Vector2(pos[0] * constant.TILE_SIZE, pos[1] * constant.TILE_SIZE)
        if pos_.distance_to(self.level.snake._block_positions[0]) < min_distance:
            return False
        
        # Check if the position is colliding with any existing entities
        for entity in self.level.snake_group:
            if entity.rect.collidepoint(pos_):
                return False
        
        # Check if the position is colliding with any obstacles
        for obstacle in self.level.obstacle_group:
            if obstacle.rect.collidepoint(pos_):
                return False
        
        return True
        
    def _create_entity(self, entity_type):
        """Create an entity based on type"""

        for _ in range(10):
            x = random.randint(
                (constant.MAP_LEFT + constant.TILE_SIZE*2)//constant.TILE_SIZE,
                (constant.MAP_RIGHT - constant.TILE_SIZE*2)//constant.TILE_SIZE
            )
            y = random.randint(
                (constant.MAP_TOP + constant.TILE_SIZE*2)//constant.TILE_SIZE,
                (constant.MAP_BOTTOM - constant.TILE_SIZE*2)//constant.TILE_SIZE
            )
            if self.is_valid_spawn_position((x,y)):
                break
        else:
            return None
        
        if entity_type == "monster":
            print(x,y)
            monster = Monster(self.level, random.randint(5, 8), (x*constant.TILE_SIZE,y*constant.TILE_SIZE))
            monster.set_player_reference(self.level.snake)
            self.level.snake_group.add(monster)
            return monster
        elif entity_type == "blocker":
            blocker = BlockerMonster(self.level, random.randint(5, 8), (x*constant.TILE_SIZE,y*constant.TILE_SIZE))
            blocker.set_player_reference(self.level.snake)
            self.level.snake_group.add(blocker)
            return blocker
        
        elif entity_type == "bomb":
            bomb = BombMonster(self.level, 4)
            bomb.set_player_reference(self.level.snake)
            self.level.snake_group.add(bomb)
            return bomb
            
        return None
    
    def _is_wave_clear(self, wave):
        """Check if all monsters in the wave are defeated"""
        # Count alive monsters from this wave
        for entity in wave.spawned_entities:
            if isinstance(entity, Monster) and entity.is_dead and len(entity.blocks) == 0:
                continue
            return False
        return True
    
    def _handle_all_waves_completed(self):
        """Handle completion of all waves"""
        self.running = False
    
    def _play_wave_cleared_sound(self):
        """Play sound when a wave is cleared"""
        from utils.help import Share
        if hasattr(Share, 'audio_manager'):
            # Share.audio_manager.play_sound("wave_cleared")
            pass
            # TODO: chưa làm âm thanh
    
    def is_complete(self):
        """Check if all waves are completed"""
        return (self.current_wave_index >= len(self.waves) and 
                all(wave.state == WaveState.COMPLETED for wave in self.waves))