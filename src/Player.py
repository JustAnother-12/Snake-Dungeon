import random
import pygame
from time import time
from pygame.math import Vector2
from states.LevelTest import LevelTest
from states.Stats_menu import base_stats_value
from level_component import Wall, Obstacle
import constant
from typing import Any




class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface((constant.TILE_SIZE, constant.TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.image.fill((255, 139, 38))
        self.target_pos = pygame.Vector2(self.rect.topleft)
        self.pos = pygame.Vector2(self.rect.topleft)
        self._last_target = pygame.Vector2(self.rect.topleft)

        self.speed = 0
        self.moving = False
        self.isOutside = False
        self._is_head = False
        self.timeSevered: float | None = None 
    
    @property
    def is_head(self):
        return self._is_head

    @is_head.setter
    def is_head(self, value):
        self._is_head = value
        if value:
            self.image = pygame.transform.rotate(constant.HEAD_IMG, -90)

    def rotate(self):
        if not self.is_head: return
        direction = self.target_pos - self.pos
        direction = direction.normalize()
        if direction == Vector2(1, 0):
            self.image = pygame.transform.rotate(constant.HEAD_IMG, -90)
        elif direction == Vector2(-1, 0):
            self.image = pygame.transform.rotate(constant.HEAD_IMG, 90)
        elif direction == Vector2(0, 1):
            self.image = pygame.transform.rotate(constant.HEAD_IMG, 180)
        elif direction == Vector2(0, -1):
            self.image = constant.HEAD_IMG

    def set_target(self, speed, target: pygame.Vector2):
        if self.target_pos != target:
            self.moving = True
            self._last_target = self.target_pos
            self.target_pos = target

            self.rotate()
        self.speed = speed

    def move(self, dt, isTurn = False):
        if not self.moving:
            self.speed = 0
            return False
        
        if self.pos.distance_to(self.target_pos) <= 0:
            self.pos = self.target_pos
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
            self.moving = False

        if not isTurn:
            self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        else:
            self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
            d_x = abs(self.target_pos.x - self.pos.x)
            d_y = abs(self.target_pos.y - self.pos.y)
            self.image = pygame.surface.Surface(
                (d_x + constant.TILE_SIZE, d_y + constant.TILE_SIZE)
            )
            self.image.fill((255, 139, 38))
            if self.target_pos.x > self.pos.x or self.target_pos.y > self.pos.y:
                self.rect = self.image.get_rect(
                    bottomright=(
                        int(
                            self.target_pos.x
                            + constant.TILE_SIZE
                        ),
                        int(
                            self.target_pos.y
                            + constant.TILE_SIZE
                        ),
                    )
                )
            else:
                self.rect = self.image.get_rect(
                    topleft=(
                        int(self.target_pos.x),
                        int(self.target_pos.y),
                    )
                )
        return True
    
    def update(self, snake, type) -> None:
        if self.timeSevered and time() - self.timeSevered > 2:
            if type == "COIN":
                snake.level.coins.add_coin(random.randint(10, 15), self, 1)
            self.kill()

class Snake(pygame.sprite.AbstractGroup):
    from states.LevelTest import LevelTest

    def __init__(self, level: LevelTest, init_len):
        super().__init__()
        self.level = level
        self.max_stamina = 10*constant.TILE_SIZE
        self.stamina = 10*constant.TILE_SIZE
        self.is_speed_boost = False
        self.speed_cool_down = 0
        self.isDeath = False
        self.coins = 0
        self.previous_time = pygame.time.get_ticks()
        self.blocks: list[SnakeBlock] = []
        self.base_speed = 16
        self.gold = 0
        self.keys = 0
        self.direction = Vector2(1, 0)
        self.base_stats = base_stats_value()

        self._block_positions = []
        self._last_direction = Vector2(0, 0)

        self._will_go_out_of_bounds = False
        # thời gian mà đầu con rắn ra khỏi bound
        self._out_of_bounds_time = None
        self._init_snake_blocks(init_len)
    
    def __len__(self):
        return len(self.blocks)
    
    
    def _init_snake_blocks(self, init_len):
        x = 0
        y = 0
        for i in range(init_len):
            x = (constant.SCREEN_WIDTH_TILES // 2 - i) * constant.TILE_SIZE
            y = (constant.SCREEN_HEIGHT_TILES // 2) * constant.TILE_SIZE
            block = SnakeBlock((x, y))
            self.blocks.append(block)

        # self.blocks[0].image = pygame.transform.rotate(constant.HEAD_IMG, -90)
        self.blocks[0].is_head = True

        self._block_positions = [block.pos.copy() for block in self.blocks]

        for block in self.blocks[::-1]:
            self.add(block)
        
    def handle_input(self):
        keys = pygame.key.get_pressed()

        key_map = {
            pygame.K_LEFT: Vector2(-1, 0),
            pygame.K_RIGHT: Vector2(1, 0),
            pygame.K_DOWN: Vector2(0, 1),
            pygame.K_UP: Vector2(0, -1),
            pygame.K_a: Vector2(-1, 0),
            pygame.K_d: Vector2(1, 0),
            pygame.K_s: Vector2(0, 1),
            pygame.K_w: Vector2(0, -1),
        }

        for key, direction in key_map.items():
            if keys[key] and self._last_direction != -direction and self._last_direction != direction:
                self.direction = direction
                break
        
        if keys[pygame.K_SPACE]:
            self.is_speed_boost = True
        else:
            self.is_speed_boost = False

    def handle_movement(self):
        for snake_block in self.blocks:
            if snake_block.moving: return

        head_pos = self._block_positions[0]
        new_head_pos = head_pos + self.direction * constant.TILE_SIZE

        self._block_positions.insert(0, new_head_pos)
        
        if self._is_collide_with_wall() or self._is_collide_with_self() or self._is_collide_with_Obstacle():
            self._block_positions.pop(0)
            if not self._will_go_out_of_bounds:
                print("Snake died after", constant.DEATH_DELAY, "out of bounds!")
                self._out_of_bounds_time = time()
            self._will_go_out_of_bounds = True
            self._last_direction = self.direction
            return
        
        self._will_go_out_of_bounds = False
        
        if len(self._block_positions) > len(self.blocks):
            self._block_positions.pop()
        
        self._last_direction = self.direction
    
    def handle_collision(self):
        self._collide_with_active_trap()
        self._collide_with_bomb()

        if self._is_collide_with_food():
            self.grow_up(2)
            self.level.food.visible = False
            self.level.remove(self.level.food)
            self.level.food_timer = 0

    def handle_go_out_of_bounds(self):
        if self._will_go_out_of_bounds:
            if self._out_of_bounds_time and time() - self._out_of_bounds_time > constant.DEATH_DELAY:
                self.isDeath = True
        else:
            self._out_of_bounds_time = None

    def update(self):
        if (len(self.blocks) <= constant.MIN_LEN):
            self.isDeath = True
            return
        dt = (pygame.time.get_ticks() - self.previous_time) / 100
        self.previous_time = pygame.time.get_ticks()
        self.handle_severed_blocks()
        self.handle_input()
        self.handle_movement()
        self.handle_go_out_of_bounds()
        self.handle_speed_boost()
        self.handle_collision()
        # print(self._block_positions, end=" " * 50 + "\r", flush=True) 
        for i, block in enumerate(self.blocks):
            block.set_target(self.base_speed, self._block_positions[i])
            block.move(dt, i!=0 and block.target_pos - block.pos != self.blocks[i-1].pos - block.target_pos)

    def handle_severed_blocks(self):
        for block in self.sprites():
            if block not in self.blocks:
                block.update(self, "COIN")

    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        t = super().draw(surface)
        return t

    def grow_up(self, length = 1):
        tail = self.blocks[-1]
        for i in range(length):
            newBlock = SnakeBlock(tail.rect.topleft)
            self.blocks.insert(-1, newBlock)
            self._block_positions.append(newBlock.pos.copy())
            for i in self.blocks[0].groups():
                i.add(newBlock) # type: ignore

    def split(self, index):
        for i in range(index, len(self.blocks)):
            if self.blocks[i].timeSevered == None:
                self.blocks[i].timeSevered = time()
        self.blocks = self.blocks[:index]
            
    def handle_speed_boost(self):
        if self.is_speed_boost:
            if self.stamina > 0:
                self.base_speed = 32
                self.stamina -= 1
            else:
                self.base_speed = 16
        else:
            self.base_speed = 16
            if self.stamina < self.max_stamina:
                self.stamina += 1

    def _is_collide_with_Obstacle(self):
        for obstacle in self.level.obstacles:
            obstacle:Obstacle
            if obstacle.rect.colliderect((self._block_positions[0][0], self._block_positions[0][1], constant.TILE_SIZE, constant.TILE_SIZE)): # type: ignore
                return True
        return False
    
    def _is_collide_with_self(self):
        for block in self.blocks[1:]:
            if block.rect.colliderect((self._block_positions[0][0], self._block_positions[0][1], constant.TILE_SIZE, constant.TILE_SIZE)):
                return True
        return False
    
    def _is_collide_with_wall(self):
        for wall in self.level.walls:
            wall: Wall
            if wall.rect and wall.rect.colliderect((self._block_positions[0][0], self._block_positions[0][1], constant.TILE_SIZE, constant.TILE_SIZE)):
                return True
        return False
    
    def _is_collide_with_food(self):
        food = self.level.food
        if food.rect and self.blocks[0].rect.colliderect(food.rect) and food.visible:
            return True
        return False
    
    def _collide_with_active_trap(self):
        pos = None
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            if pygame.sprite.spritecollideany(block, self.level.traps, lambda x, y: x.rect.colliderect(y.rect) and getattr(y, "isActive", False)):
                pos = i
                break
        if pos != None:
            self.split(pos)   

    def _collide_with_bomb(self):
        pos = None
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            if pygame.sprite.spritecollideany(block, self.level.bombs, lambda x, y: x.rect.colliderect(y.rect) and time() - float(getattr(y, "activeTime", time())) > 0.6):
                block.kill()
                pos = i if pos == None else pos
        if pos != None:
            self.split(pos)

class GreenSnake(Snake):
    def __init__(self, level: LevelTest, init_len):
        super().__init__(level, init_len)

    def handle_go_out_of_bounds(self):
        if self._will_go_out_of_bounds:
            if self._out_of_bounds_time and time() - self._out_of_bounds_time > constant.DEATH_DELAY:
                block = self.blocks.pop()
                block.kill()
                self._out_of_bounds_time = None
                self._will_go_out_of_bounds = False
        else:
            self._out_of_bounds_time = None