import random
import pygame
from pygame.math import Vector2

from config import constant
from entities.Player import Snake, SnakeBlock
from entities.items.instant.coin import CoinEntity
from entities.items.instant.food import FoodEntity
from entities.items.instant.key import KeyEntity
from levels.components.trap import TrapState
from loot import LootItem, LootPool
from levels.components.bomb import Bomb, BombState
from utils import pixil


class Monster(Snake):
    def __init__(self, level, init_len, pos=None):
        # Câu hình màu sắc và hình ảnh cho đầu rắn
        self.pos = pos if pos else random.choice([(constant.MAP_LEFT, constant.MAP_TOP), (constant.MAP_RIGHT - constant.TILE_SIZE, constant.MAP_BOTTOM -
                                                 constant.TILE_SIZE), (constant.MAP_LEFT, constant.MAP_BOTTOM - constant.TILE_SIZE), (constant.MAP_RIGHT - constant.TILE_SIZE, constant.MAP_TOP)])
        self.color = self.color if hasattr(self, "color") else pygame.Color(0, 255, 0)
        self.headImg = pygame.Surface((constant.TILE_SIZE, constant.TILE_SIZE))
        self.headImg.fill(self.color)
        pygame.draw.rect(self.headImg, (255, 255, 255), (3, 3, 2, 4))
        pygame.draw.rect(self.headImg, (255, 255, 255), (11, 3, 2, 4))
        self.auto_state = True

        super().__init__(level, init_len)

        self.player = None  # Reference to the player object
        # Radius to avoid traps and obstacles
        self.avoidance_radius = 5 * constant.TILE_SIZE
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
        if self.is_dead and len(self.blocks) == 1:
            block = self.blocks.pop(0)
            for _ in range(random.randint(3,5)):
                self.level.item_group.add(CoinEntity(self.level, block.rect, 1)) # luôn luôn drop tiền

            loot_pool = LootPool((0, 0, 40, 10, 17, 15, 13, 5))
            item, rarity = loot_pool.get_item()       
            if item == LootItem.FOOD:
                for _ in range(random.randint(1,2)):
                    self.level.item_group.add(FoodEntity(self.level, block.rect, 1))
            elif item == LootItem.KEY:
                self.level.item_group.add(KeyEntity(self.level, block.rect, 1))
            else:
                from entities.items.item_registry import ItemRegistry
                self.level.item_group.add(ItemRegistry.create_item(
                    item, rarity, self.level, block.rect))
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
                weight = max(self._calculate_weight(move, new_head_pos), 1)
                valid_moves.append(move)
                move_weights.append(self._calculate_weight(move, new_head_pos))

        if len(valid_moves) > 0:
            self.direction = random.choices(
                valid_moves, weights=move_weights)[0]
            self.is_curling = False

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
            weight = max(1, weight * (1 + food_attraction))

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
            block = SnakeBlock(int(i == 0), (x, y), self.color)
            self.blocks.append(block)

        self.blocks[0].is_head = True

        self._block_positions = [block.pos.copy() for block in self.blocks]

        for block in self.blocks[::-1]:
            self.add(block)

    def die(self):
        if len(self.blocks) == 0:
            self.level.snake_group.remove(self)
            return
        
        block = self.blocks.pop(0)
        self._block_positions.pop(0)
        block.kill()
class BombMonster(Monster):
    def __init__(self, level, init_len, pos=None):
        self.color = pygame.Color(79,79,79)
        super().__init__(level, init_len, pos)
        self.headImg = pixil.Pixil.load(constant.Texture.bomb_snake_head, 1).frames[0]

    def handle_ai_movement(self):
        if not self.player is None and self.player.is_dead == False:

            d = self._block_positions[0] - self.player._block_positions[0]

            if abs(d.x) > abs(d.y):
                self.direction = Vector2(-1 if d.x > 0 else 1, 0)
            else:
                self.direction = Vector2(0, -1 if d.y > 0 else 1)

    def update(self):
        if not self.is_dead:
            if self._is_collide_with_obstacle(self._block_positions[0]) or self._is_collide_with_orther_snake(self._block_positions[0]):
                self.is_dead = True
        super().update()

    def die(self):
        if len(self.blocks) == 0:
            self.level.snake_group.remove(self)
            return
        block = self.blocks.pop(0)
        if block:
            self.level.bomb_group.add(
                Bomb(self.level, block.pos, BombState.EXPLOSION))
            
class BlockerMonster(Monster):
    def __init__(self, level, init_len, pos=None):
        self.color = pygame.Color(0, 150, 150)
        super().__init__(level, init_len, pos)
        self.headImg.fill(self.color)
        pygame.draw.rect(self.headImg, (255, 255, 0), (3, 3, 2, 4))
        pygame.draw.rect(self.headImg, (255, 255, 0), (11, 3, 2, 4))
        self.look_ahead = 3
    
    def _calculate_weight(self, move, position):
        """Calculate weight for each potential move to block player's movement paths"""
        if self.player is None or self.player.is_dead:
            return super()._calculate_weight(move, position)
            
        # Start with base weight
        weight = 100 if move == self.direction else 10
        
        # Calculate individual scores
        blocking_score = self._calculate_blocking_score(move, position)
        trapping_score = self._calculate_wall_trapping_score(move, position)
        interception_score = self._calculate_interception_score(move, position)
        
        # Apply all scoring factors
        weight = weight + blocking_score + trapping_score + interception_score
        
        # Get player position
        player_pos = self.player._block_positions[0]
        distance_to_player = (Vector2(position) - player_pos).length()
        
        # Reduce weight if moving away from player
        if distance_to_player > constant.TILE_SIZE * 10:
            weight /= 2
        
        # Factor in danger avoidance from parent class (traps, etc.)
        trap_danger = self._calculate_trap_danger(position)
        bomb_danger = self._calculate_bomb_danger(position)
        danger_factor = trap_danger + bomb_danger
        if danger_factor > 0:
            weight = max(1, weight / (danger_factor * 2))
        
        return weight

    def _calculate_blocking_score(self, move, position):
        """Calculate score for moves that directly block player's path"""
        if self.player is None:
            return 0
            
        # Get player position and direction
        player_pos = self.player._block_positions[0]
        player_direction = self.player.direction
        
        # Predict player's possible movement paths (current + turns)
        player_possible_moves = []
        
        # Current direction
        if player_direction.length() > 0:
            player_possible_moves.append(player_direction)
            
            # Left turn (perpendicular direction)
            left_turn = Vector2(-player_direction.y, player_direction.x)
            player_possible_moves.append(left_turn)
            
            # Right turn (perpendicular direction)
            right_turn = Vector2(player_direction.y, -player_direction.x)
            player_possible_moves.append(right_turn)
        else:
            # If player isn't moving, consider all 4 directions
            player_possible_moves = [Vector2(1, 0), Vector2(-1, 0), 
                                Vector2(0, 1), Vector2(0, -1)]
        
        # Calculate how well this move blocks player paths
        blocking_score = 0
        for player_move in player_possible_moves:
            # Create a vector for where player would go
            player_next_pos = player_pos + player_move * constant.TILE_SIZE
            
            # Check if our position would block this path
            if (position.x == player_next_pos.x and position.y == player_next_pos.y):
                # Direct blocking position!
                blocking_score += 1000
            
            # Check if we'd be in line with player's path (within 2 tiles)
            for i in range(1, 3):
                check_pos = player_pos + player_move * constant.TILE_SIZE * i
                check_distance = (Vector2(position) - check_pos).length()
                if check_distance < constant.TILE_SIZE:
                    # We'd be directly in player's path!
                    blocking_score += 800 / (i + 0.1)  # Closer is better
        
        return blocking_score

    def _calculate_wall_trapping_score(self, move, position):
        """Calculate score for moves that trap player against walls or obstacles"""
        if self.player is None:
            return 0
            
        # Get player position and direction
        player_pos = self.player._block_positions[0]
        player_direction = self.player.direction
        distance_to_player = (Vector2(position) - player_pos).length()
        
        # Only consider wall trapping when close enough
        if distance_to_player > constant.TILE_SIZE * 5:
            return 0
            
        # Predict player's possible movement paths
        player_possible_moves = []
        
        # Current direction
        if player_direction.length() > 0:
            player_possible_moves.append(player_direction)
            
            # Left and right turns
            left_turn = Vector2(-player_direction.y, player_direction.x)
            right_turn = Vector2(player_direction.y, -player_direction.x)
            player_possible_moves.append(left_turn)
            player_possible_moves.append(right_turn)
        else:
            # If player isn't moving, consider all 4 directions
            player_possible_moves = [Vector2(1, 0), Vector2(-1, 0), 
                                Vector2(0, 1), Vector2(0, -1)]
        
        # Calculate trapping score
        wall_trapping_score = 0
        
        # Check how many directions are blocked
        blocked_directions = 0
        for player_move in player_possible_moves:
            player_future_pos = player_pos + player_move * constant.TILE_SIZE
            
            # Check if this direction would hit a wall/boundary
            if (player_future_pos.x < constant.MAP_LEFT or
                player_future_pos.x >= constant.MAP_RIGHT or
                player_future_pos.y < constant.MAP_TOP or
                player_future_pos.y >= constant.MAP_BOTTOM):
                blocked_directions += 1
                wall_trapping_score += 200
                
            # Check for obstacles that would trap player
            elif self._is_collide_with_obstacle(player_future_pos):
                blocked_directions += 1
                wall_trapping_score += 300
                
            # Check if our new position would block this direction
            elif position.x == player_future_pos.x and position.y == player_future_pos.y:
                blocked_directions += 1
                wall_trapping_score += 400
        
        # Huge bonus if we're blocking the last escape route (3 directions already blocked)
        if blocked_directions >= 3:
            wall_trapping_score += 1500
        
        return wall_trapping_score

    def _calculate_interception_score(self, move, position):
        """Calculate score for intercepting the player's path"""
        if self.player is None:
            return 0
            
        # Get player position and direction
        player_pos = self.player._block_positions[0]
        player_direction = self.player.direction
        
        # If player isn't moving, no interception is possible
        if player_direction.length() == 0:
            return 0
            
        interception_score = 0
        
        # Calculate ideal interception point (ahead of player)
        for i in range(1, self.look_ahead + 1):
            interception_point = player_pos + player_direction * constant.TILE_SIZE * i
            
            # Check if our move gets us closer to intercepting player
            current_to_intercept = (Vector2(self._block_positions[0]) - interception_point).length()
            new_to_intercept = (Vector2(position) - interception_point).length()
            
            # Higher score if we're moving closer to interception point
            if new_to_intercept < current_to_intercept:
                # More points for closer interception points
                interception_score += 300 * (1 - (new_to_intercept / (constant.TILE_SIZE * 10))) / i
                
            # Huge bonus if we're exactly at the interception point
            if abs(position.x - interception_point.x) < 0.1 and abs(position.y - interception_point.y) < 0.1:
                interception_score += 700 / i  # More points for earlier interception
        
        return interception_score