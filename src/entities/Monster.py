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
            self.direction = random.choices(
                valid_moves, weights=move_weights)[0]
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
                attraction += 0.5 * \
                    (1 - (distance / (self.avoidance_radius * 2)))
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
        loot_pool = LootPool((5, 10, 5, 2, 3, 0, 0, 0))
        block = self.blocks.pop(0)
        self._block_positions.pop(0)
        item, rarity = loot_pool.get_item()
        if item == LootItem.COIN:
            self.level.item_group.add(CoinEntity(
                self.level, block.rect, 1, random.randint(10, 15)))
        elif item == LootItem.FOOD:
            self.level.item_group.add(FoodEntity(self.level, block.rect, 1))
        elif item == LootItem.KEY:
            self.level.item_group.add(KeyEntity(self.level, block.rect, 1))
        elif item == LootItem.EMPTY:
            pass
        else:
            from entities.items.item_registry import ItemRegistry
            self.level.item_group.add(ItemRegistry.create_item(
                item, rarity, self.level, block.rect))
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
        self.color = pygame.Color(0, 150, 150)  # Teal color
        super().__init__(level, init_len, pos)
        self.headImg.fill(self.color)
        # Add distinctive eyes to identify this monster type
        pygame.draw.rect(self.headImg, (255, 255, 0), (3, 3, 2, 4))  # Yellow eyes
        pygame.draw.rect(self.headImg, (255, 255, 0), (11, 3, 2, 4))
        # Interception parameters
        self.look_ahead = 3  # How many tiles ahead to look
        
    def handle_ai_movement(self):
        # For debugging - verify the direction
        if self.player is None or self.player.is_dead or self.is_dead:
            return
        
        # Ensure we're not processing this if blocks are already moving
        for snake_block in self.blocks:
            if snake_block.moving:
                return
                
        # Get positions and current direction
        head_pos = self._block_positions[0]
        player_head_pos = self.player._block_positions[0]
        player_direction = self.player.direction
        
        # Initialize direction if it's (0,0)
        if self.direction.length() == 0:
            # Set initial direction towards player
            if abs(head_pos.x - player_head_pos.x) > abs(head_pos.y - player_head_pos.y):
                self.direction = Vector2(1 if player_head_pos.x > head_pos.x else -1, 0)
            else:
                self.direction = Vector2(0, 1 if player_head_pos.y > head_pos.y else -1)
        
        # Calculate player's projected path
        projected_player_pos = Vector2(player_head_pos)
        if player_direction.length() > 0:  # Only project if player is moving
            for _ in range(self.look_ahead):
                projected_player_pos += player_direction * constant.TILE_SIZE
                
        # Calculate best interception move - using our filtered moves
        possible_moves = self._get_non_reverse_moves(head_pos)
        if not possible_moves:  # No valid moves available
            self.is_dead = True  # Monster is trapped
            return
            
        best_direction = self._calculate_interception_from_moves(
            head_pos, player_head_pos, projected_player_pos, 
            player_direction, possible_moves)
            
        # Verify that the best direction is not a reverse of current direction
        if self._is_reverse_direction(best_direction):
            # This should never happen due to our filtering, but just in case
            alternative_directions = [d for d in possible_moves if not self._is_reverse_direction(d)]
            if alternative_directions:
                best_direction = alternative_directions[0]
            else:
                # Keep current direction if no other options
                return
        
        self.direction = best_direction
        self.is_curling = False
    
    def _is_reverse_direction(self, direction):
        """Check if a direction is the reverse of the current direction"""
        if self.direction.length() == 0:
            return False
            
        # Exact component-wise comparison for reversal
        return (abs(direction.x + self.direction.x) < 0.01 and 
                abs(direction.y + self.direction.y) < 0.01)
    
    def _get_non_reverse_moves(self, current_pos):
        """Get all valid moves that aren't reversals or collisions"""
        possible_directions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        valid_moves = []
        
        for direction in possible_directions:
            # Skip if this is a reverse direction
            if self._is_reverse_direction(direction):
                continue
                
            # Skip if this would cause collision
            next_pos = current_pos + direction * constant.TILE_SIZE
            if self._would_hit_obstacle(next_pos):
                continue
                
            valid_moves.append(direction)
                
        return valid_moves
    
    def _calculate_interception_from_moves(self, head_pos, player_pos, projected_player_pos, 
                                         player_direction, possible_moves):
        """Calculate best interception from pre-filtered valid moves"""
        best_direction = None
        best_score = float('inf')
        
        for direction in possible_moves:
            # Calculate where this move would put us
            next_pos = head_pos + direction * constant.TILE_SIZE
            
            # Calculate distance to player's projected path
            score = self._distance_to_line(next_pos, player_pos, projected_player_pos)
            
            # Bonus for positions directly in front of player
            player_front = player_pos + player_direction * constant.TILE_SIZE
            distance_to_front = (next_pos - player_front).length()
            if distance_to_front < constant.TILE_SIZE * 2:
                score -= 100  # Huge bonus for blocking player's immediate path
                
            # Bonus for moves that align with player's direction
            alignment = abs(direction.dot(player_direction))
            if alignment > 0.5:  # Moving roughly parallel to player
                score -= 20
            
            if score < best_score:
                best_score = score
                best_direction = direction
        
        # If no direction found, use the first valid move or current direction
        if best_direction is None and possible_moves:
            return possible_moves[0]
        elif best_direction is None:
            return self.direction
            
        return best_direction
    
    def _distance_to_line(self, point, line_start, line_end):
        """Calculate the perpendicular distance from a point to a line segment"""
        if line_start == line_end:
            return (point - line_start).length()
            
        line_vec = line_end - line_start
        point_vec = point - line_start
        line_len = line_vec.length()
        line_unit_vec = line_vec / line_len
        
        # Project point to line
        projection = point_vec.dot(line_unit_vec)
        
        # If projection is outside the line segment, use distance to endpoint
        if projection < 0:
            return (point - line_start).length()
        elif projection > line_len:
            return (point - line_end).length()
        else:
            # Perpendicular distance
            return abs((point_vec - projection * line_unit_vec).length())
    
    def _would_hit_obstacle(self, position):
        """Check if a position would result in collision"""
        # Check map boundaries
        if (position.x < constant.MAP_LEFT or position.x >= constant.MAP_RIGHT or
            position.y < constant.MAP_TOP or position.y >= constant.MAP_BOTTOM):
            return True
            
        # Check for collisions with obstacles and other snake blocks
        return (self._is_collide_with_obstacle(position) or 
                self._is_collide_with_orther_snake(position))