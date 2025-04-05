import random
from time import sleep
import pygame
from pygame.math import Vector2

from config import constant
from entities.Player import Snake, SnakeBlock
from entities.items.instant.coin import CoinEntity
from entities.items.instant.food import FoodEntity
from levels.components.obstacle import Obstacle
from levels.components.trap import TrapState
from levels.components.wall import Wall
from loot import LootItem, LootPool
from levels.components.bomb import BombState
from utils.help import Share

class Monster(Snake):
    def __init__(self, level, init_len, pos = None):
        # Câu hình màu sắc và hình ảnh cho đầu rắn
        self.pos = pos if pos else random.choice([(constant.MAP_LEFT, constant.MAP_TOP), (constant.MAP_RIGHT - constant.TILE_SIZE, constant.MAP_BOTTOM - constant.TILE_SIZE), (constant.MAP_LEFT, constant.MAP_BOTTOM - constant.TILE_SIZE), (constant.MAP_RIGHT - constant.TILE_SIZE, constant.MAP_TOP)])
        self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.headImg = pygame.Surface((constant.TILE_SIZE, constant.TILE_SIZE))
        self.headImg.fill(self.color)
        pygame.draw.rect(self.headImg, (255, 255, 255), (3, 3, 2, 4))
        pygame.draw.rect(self.headImg, (255, 255, 255), (11, 3, 2, 4))

        super().__init__(level, init_len)

        self.player = None  # Reference to the player object
        self.avoidance_radius = 5 * constant.TILE_SIZE  # Radius to avoid traps and obstacles
        self.direction = Vector2(0, 0)
        self.is_curling = True
        self.base_stats.speed = 12

    def set_player_reference(self, player: Snake):
        self.player = player
    
    def update_stats(self):
        pass

    def handle_input(self):
        self.handle_ai_movement()
        return True
        # return super().handle_input()

    def update(self):
        return super().update()

    def handle_ai_movement(self):
        # Nếu đang di chuyển hoặc đã chết, không xử lý
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
        move_weights = []

        for move in potential_moves:
            # Không đi ngược lại
            if move == -self.direction:
                continue
                
            new_head_pos = head_pos + move * constant.TILE_SIZE
            
            # Kiểm tra va chạm trực tiếp
            if not self._is_collide(new_head_pos):
                valid_moves.append(move)
                move_weights.append(self._calculate_weight(move, new_head_pos))

        if len(valid_moves) > 0:
            self.direction = random.choices(valid_moves, weights=move_weights)[0] 
            self.is_curling = False
            # self._block_positions.insert(0, head_pos + self.direction * constant.TILE_SIZE)
        else:
            self.is_dead = True
            return
            
    def _calculate_weight(self, move, position):
        weight = 100 if move == self.direction else 10
                
        # Kiểm tra các trở ngại trong bán kính tránh
        trap_danger = self._calculate_trap_danger(position)
        bomb_danger = self._calculate_bomb_danger(position)
        
        # Giảm trọng số nếu gần bẫy hoặc chướng ngại vật
        danger_factor = trap_danger + bomb_danger
        if danger_factor > 0:
            weight = max(1, weight / danger_factor)
        
        # Ưu tiên di chuyển về phía đồ ăn hoặc vật phẩm
        food_attraction = self._calculate_food_attraction(position)
        if food_attraction > 0:
            weight *= (1 + food_attraction)
        
        return weight

    def _calculate_trap_danger(self, position):
        """Tính toán mức độ nguy hiểm từ bẫy trong bán kính tránh."""
        danger = 0
        for trap in self.level.trap_group:
            trap_pos = Vector2(trap.rect.x, trap.rect.y)
            distance = (Vector2(position) - trap_pos).length()
            if distance < self.avoidance_radius:
                # Nguy hiểm tăng khi khoảng cách giảm
                danger += 1 - (distance / self.avoidance_radius)
                if trap.state == TrapState.ACTIVATED:
                    return 10
        return danger

    def _calculate_bomb_danger(self, position):
        """Tính toán mức độ nguy hiểm từ chướng ngại vật trong bán kính tránh."""
        danger = 0
        for bomb in self.level.bomb_group:
            bomb_pos = Vector2(bomb.rect.x, bomb.rect.y)
            distance = (Vector2(position) - bomb_pos).length()
            if distance < self.avoidance_radius:
                # Nguy hiểm tăng khi khoảng cách giảm
                danger += 1 - (distance / self.avoidance_radius)
                if bomb.state == BombState.ACTIVE or bomb.state == BombState.EXPLOSION:
                    return 10
        return danger

    def _calculate_food_attraction(self, position):
        """Tính toán độ hấp dẫn từ thức ăn hoặc vật phẩm."""
        attraction = 0
        pos_vector = Vector2(position)
        
        # Tìm kiếm thức ăn gần đó
        for item in self.level.item_group:
            item_pos = Vector2(item.rect.x, item.rect.y)
            distance = (pos_vector - item_pos).length()
            if distance < self.avoidance_radius * 2:  # Phạm vi tìm kiếm thức ăn xa hơn
                # Độ hấp dẫn tăng khi khoảng cách giảm
                attraction += 0.5 * (1 - (distance / (self.avoidance_radius * 2)))   
        return attraction
    
    def _init_snake_blocks(self, init_len):
        x, y = self.pos
        for i in range(init_len):
            block = SnakeBlock(int(i==0) ,(x, y), self.color)
            self.blocks.append(block)

        self.blocks[0].is_head = True

        self._block_positions = [block.pos.copy() for block in self.blocks]

        for block in self.blocks[::-1]:
            self.add(block)

    def die(self):
        loot_pool = LootPool((5, 10, 7, 3, 0, 0, 0))
        if len(self.sprites()) == 0:
            self.level.snake_group.remove(self)
            return
        block = self.sprites()[-1]
        block.kill()
        item = loot_pool.get_item()
        if item == LootItem.COIN:
            self.level.item_group.add(CoinEntity(self.level, block.rect, 1, random.randint(10, 15)))
        elif item == LootItem.FOOD:
            self.level.item_group.add(FoodEntity(self.level, block.rect, 1))
        elif item == LootItem.EMPTY:
            pass
        else:
            print(f"[{item.value}]: Instant item")
