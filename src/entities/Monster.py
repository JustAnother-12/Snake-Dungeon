import random
import pygame
from pygame.math import Vector2

from config import constant
from entities.Player import Snake, SnakeBlock
from levels.components.obstacle import Obstacle
from levels.components.wall import Wall

class AIMonster(Snake):
    def __init__(self, level, init_len, pos):
        self.pos = pos
        super().__init__(level, init_len)
        self.player = None  # Reference to the player object
        self.avoidance_radius = 5 * constant.TILE_SIZE  # Radius to avoid traps and obstacles
        self.direction = Vector2(0, 0)
        self.is_curling = True

    def set_player_reference(self, player: Snake):
        self.player = player

    def update(self):
        if len(self.blocks) <= constant.MIN_LEN:
            self.is_death = True
            return
        dt = self.level.game.clock.get_time()
        self.handle_severed_blocks()
        if self.auto_state:
            self.handle_ai_movement()
        self.handle_go_out_of_bounds(dt)
        self.handle_speed_boost()
        self.handle_collision()
        self.handle_skills(dt)
        for i, block in enumerate(self.blocks):
            block.set_target(
                self.base_stats.speed, self._block_positions[i]
            )
            if i == 0:
                block.rotate(self.direction, self.headImg)
            block.move(
                dt / 100,
                i != 0
                and block.target_pos - block._last_target
                != self.blocks[i - 1].target_pos
                - self.blocks[i - 1]._last_target,
            )

    def handle_ai_movement(self):
        for snake_block in self.blocks:
            if snake_block.moving:
                return

        if self.is_dead:
            return

        head_pos = self._block_positions[0]
        potential_moves = [
            Vector2(1, 0), Vector2(-1, 0),
            Vector2(0, 1), Vector2(0, -1)
        ]

        valid_moves = []
        w = []
        for move in potential_moves:
            if move == -self.direction:
                continue
            new_head_pos = head_pos + move * constant.TILE_SIZE
            if not self._is_collide(new_head_pos):
                valid_moves.append(move)
                w.append(20 if move == self.direction else 1)

        if len(valid_moves) > 0:
            self.direction = random.choices(valid_moves, w)[0] 
            self.is_curling = False
            self._block_positions.insert(0, head_pos + self.direction * constant.TILE_SIZE)
        else:
            self.is_death = True
            return
        if len(self._block_positions) > len(self.blocks):
            self._block_positions.pop()

    def _is_collide(self, position):
        if self._is_collide_with_wall(position) or self._is_collide_with_Obstacle(position) or self._is_collide_with_self(position) or self._is_collide_with_player(position):
            return True
        return False

    def _is_collide_with_wall(self, position):
        for wall in self.level.wall_group:
            wall: Wall
            if wall.rect and wall.rect.colliderect(
                (
                    position[0],
                    position[1],
                    constant.TILE_SIZE,
                    constant.TILE_SIZE,
                )
            ):
                return True
        return False

    def _is_collide_with_Obstacle(self, position):
        for obstacle in self.level.obstacle_group:
            obstacle: Obstacle
            if obstacle.rect and obstacle.rect.colliderect((position[0], position[1], constant.TILE_SIZE, constant.TILE_SIZE)):
                return True
        return False

    def _is_collide_with_self(self, position):
        if self.is_curling:
            return False
        for block in self.blocks[1:]:
            if block.rect.colliderect(
                (
                    position[0],
                    position[1],
                    constant.TILE_SIZE,
                    constant.TILE_SIZE,
                )
            ):
                return True
        return False

    def _is_collide_with_player(self, position):
        if not self.player: return False
        for block in self.player.blocks:
            if block.rect.colliderect(
                (
                    position[0],
                    position[1],
                    constant.TILE_SIZE,
                    constant.TILE_SIZE,
                )
            ):
                return True
        return False
    
    def _init_snake_blocks(self, init_len):
        x, y = self.pos
        for i in range(init_len):
            block = SnakeBlock(int(i==0) ,(x, y), self.color)
            self.blocks.append(block)

        self.blocks[0].is_head = True

        self._block_positions = [block.pos.copy() for block in self.blocks]

        for block in self.blocks[::-1]:
            self.add(block)