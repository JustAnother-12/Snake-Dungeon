import random
from enum import Enum
import pygame
from pygame.math import Vector2

from config import constant
from entities.Monster import Monster
from levels.components.bomb import Bomb, BombState
from levels.components.trap import Trap
from levels.level import LevelStatus
from utils.help import Share


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
    def __init__(self, level):
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
            
    def _create_entity(self, entity_type):
        """Create an entity based on type"""
        if entity_type == "monster":
            monster = Monster(self.level, random.randint(5, 8))
            monster.set_player_reference(self.level.snake)
            self.level.snake_group.add(monster)
            return monster
            
        elif entity_type == "bomb":
            # Random position for bomb
            x = random.randint(
                constant.MAP_LEFT + constant.TILE_SIZE*2,
                constant.MAP_RIGHT - constant.TILE_SIZE*2
            )
            y = random.randint(
                constant.MAP_TOP + constant.TILE_SIZE*2,
                constant.MAP_BOTTOM - constant.TILE_SIZE*2
            )
            bomb = Bomb(self.level, Vector2(x, y), BombState.ACTIVE)
            self.level.bomb_group.add(bomb)
            return bomb
            
        elif entity_type == "trap":
            x = random.randint(
                constant.MAP_LEFT + constant.TILE_SIZE*2,
                constant.MAP_RIGHT - constant.TILE_SIZE*2
            )
            y = random.randint(
                constant.MAP_TOP + constant.TILE_SIZE*2,
                constant.MAP_BOTTOM - constant.TILE_SIZE*2
            )
            trap = Trap(self.level, (x, y))
            self.level.trap_group.add(trap)
            return trap
            
        return None
    
    def _is_wave_clear(self, wave):
        """Check if all monsters in the wave are defeated"""
        # Count alive monsters from this wave
        active_monsters = [e for e in wave.spawned_entities 
                         if isinstance(e, Monster) and e.alive()]
        return len(active_monsters) == 0
    
    def _handle_all_waves_completed(self):
        """Handle completion of all waves"""
        self.running = False
        self.level.level_status = LevelStatus.ROOM_CLEARED
    
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
    
    def generate_waves(self, difficulty=1.0):
        """Generate waves based on difficulty level"""
        self.waves = []
        
        # Simple template-based generation
        if difficulty <= 1.0:  # Easy
            self.add_wave(Wave({"monster": 2}, delay=2.0))
            self.add_wave(Wave({"monster": 3}, delay=5.0))
            
        elif difficulty <= 2.0:  # Medium
            self.add_wave(Wave({"monster": 3}, delay=1.5))
            self.add_wave(Wave({"monster": 2, "bomb": 2}, delay=3.0))
            self.add_wave(Wave({"monster": 4, "trap": 1}, delay=3.0))
            
        else:  # Hard
            self.add_wave(Wave({"monster": 4}, delay=1.0))
            self.add_wave(Wave({"monster": 3, "bomb": 3}, delay=2.5))
            self.add_wave(Wave({"monster": 3, "trap": 2}, delay=2.0))
            self.add_wave(Wave({"monster": 5, "bomb": 2, "trap": 1}, delay=2.0))
        
        return self