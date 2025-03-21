from __future__ import annotations
from operator import pos
import os
import pygame
from typing import Any, override
from level_component import Chest, Chests, Coins, Keys, Obstacle, Trap, Traps, Wall, Walls, Bombs, Obstacle_group
from states.GameOver_menu import GameOver_menu
from states.state import State
from states.Pause_menu import Pause_menu
from states.Stats_menu import base_stats_value
from pixil import Pixil
from pygame.sprite import AbstractGroup
import constant
from pygame.math import Vector2
import random
from logic.help import check_collision
from time import time, sleep
from HUD import HUD

MAP_WIDTH = (
    constant.SCREEN_WIDTH_TILES - constant.LEFT_RIGHT_BORDER_TILES * 2 - constant.WALL_TILES * 2
) * constant.TILE_SIZE
MAP_HEIGHT = (
    constant.SCREEN_HEIGHT_TILES - constant.TOP_BOTTOM_BORDER_TILES * 2 - constant.WALL_TILES * 2
) * constant.TILE_SIZE
MAP_LEFT = (constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES)* constant.TILE_SIZE
MAP_RIGHT = MAP_LEFT + MAP_WIDTH
MAP_TOP = (constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES)* constant.TILE_SIZE
MAP_BOTTOM = MAP_TOP + MAP_HEIGHT

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image: pygame.Surface = pygame.transform.scale(
            Pixil.load(constant.Texture.apple, 1).frames[0],
            (constant.TILE_SIZE, constant.TILE_SIZE),
        )
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.visible = True

    def random_pos(self, snake_blocks):
        self.pos = pygame.Vector2(
            (
                random.randint(
                    constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                    constant.SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 2
                    - constant.WALL_TILES,
                )
                * constant.TILE_SIZE
            ),
            (
                random.randint(
                    constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                    constant.SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 2
                    - constant.WALL_TILES,
                )
                * constant.TILE_SIZE
            ),
        )
        self.rect = self.image.get_rect(topleft=self.pos)
        if check_collision(self, snake_blocks):
            self.random_pos(snake_blocks)

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)


class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface((constant.TILE_SIZE, constant.TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.image.fill((255, 139, 38))
        self.target_pos = pygame.Vector2(self.rect.topleft)
        self.pos = pygame.Vector2(self.rect.topleft)
        self.__last_target = pygame.Vector2(self.rect.topleft)

        self.speed = 0
        self.moving = False
        self.isOutside = False
        self.__is_head = False
        self.timeSevered: float | None = None 
    
    @property
    def is_head(self):
        return self.__is_head

    @is_head.setter
    def is_head(self, value):
        self.__is_head = value
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
            self.__last_target = self.target_pos
            self.target_pos = target

            self.rotate()
        self.speed = speed

    def move(self, dt, animation=True, tail_movement=False):
        if not self.moving:
            self.speed = 0
            return False
        
        if self.pos.distance_to(self.target_pos) <= 0:
            self.pos = self.target_pos
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
            self.moving = False

        if animation and not tail_movement:
            self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
            
        elif tail_movement:
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
        else:
            self.pos = self.target_pos
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
            self.moving = False
        
        return True
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

class Snake(pygame.sprite.AbstractGroup):

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

        self.__block_positions = []
        self.__last_direction = Vector2(0, 0)

        self.__will_go_out_of_bounds = False
        # thời gian mà đầu con rắn ra khỏi bound
        self.__out_of_bounds_time = None
        self.__init_snake_blocks(init_len)
    
    def __len__(self):
        return len(self.blocks)
    
    
    def __init_snake_blocks(self, init_len):
        x = 0
        y = 0
        for i in range(init_len):
            x = (constant.SCREEN_WIDTH_TILES // 2 - i) * constant.TILE_SIZE
            y = (constant.SCREEN_HEIGHT_TILES // 2) * constant.TILE_SIZE
            block = SnakeBlock((x, y))
            self.blocks.append(block)

        # self.blocks[0].image = pygame.transform.rotate(constant.HEAD_IMG, -90)
        self.blocks[0].is_head = True

        self.__block_positions = [block.pos.copy() for block in self.blocks]

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
            if keys[key] and self.__last_direction != -direction and self.__last_direction != direction:
                self.direction = direction
                break
        
        if keys[pygame.K_SPACE]:
            self.is_speed_boost = True
        else:
            self.is_speed_boost = False

    def handle_movement(self):
        for snake_block in self.blocks:
            if snake_block.moving: return

        head_pos = self.__block_positions[0]
        new_head_pos = head_pos + self.direction * constant.TILE_SIZE

        self.__block_positions.insert(0, new_head_pos)
        
        if self.__is_collide_with_wall() or self.__is_collide_with_self() or self.__is_collide_with_Obstacle():
            self.__block_positions.pop(0)
            if not self.__will_go_out_of_bounds:
                print("Snake died after", constant.DEATH_DELAY, "out of bounds!")
                self.__out_of_bounds_time = time()
            self.__will_go_out_of_bounds = True
            self.__last_direction = self.direction
            return
        
        self.__will_go_out_of_bounds = False
        
        if len(self.__block_positions) > len(self.blocks):
            self.__block_positions.pop()
        
        self.__last_direction = self.direction
    
    def handle_collision(self):
        self.__collide_with_active_trap()
        self.__collide_with_bomb()

        if self.__is_collide_with_food():
            self.grow_up()
            self.level.food.visible = False
            self.level.remove(self.level.food)
            self.level.food_timer = 0

    def handle_go_out_of_bounds(self):
        if self.__will_go_out_of_bounds:
            if self.__out_of_bounds_time and time() - self.__out_of_bounds_time > constant.DEATH_DELAY:
                self.isDeath = True
        else:
            self.__out_of_bounds_time = None

    def update(self):
        dt = (pygame.time.get_ticks() - self.previous_time) / 100
        self.previous_time = pygame.time.get_ticks()

        self.remove_severed_tail()
        self.handle_input()
        self.handle_movement()
        self.handle_go_out_of_bounds()
        self.handle_speed_boost()
        self.handle_collision()
        # print(self.__block_positions, end=" " * 50 + "\r", flush=True) 
        for i, block in enumerate(self.blocks):
            block.set_target(self.base_speed, self.__block_positions[i])
            block.move(dt, 
                animation=(i == 0),
                tail_movement=(i == len(self.blocks) - 1)
            )

    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        t = super().draw(surface)
        return t

    def remove_severed_tail(self):
        for block in self.sprites():
            if block not in self.blocks:
                if block.timeSevered and time() - block.timeSevered > 2:
                    block.kill()

    def grow_up(self):
        tail = self.blocks[-1]
        newBlock = SnakeBlock(tail.rect.topleft)
        self.blocks.insert(-1, newBlock)
        self.__block_positions.append(newBlock.pos.copy())
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

    def __is_collide_with_Obstacle(self):
        for obstacle in self.level.obstacles:
            obstacle:Obstacle
            if obstacle.rect.colliderect((self.__block_positions[0][0], self.__block_positions[0][1], constant.TILE_SIZE, constant.TILE_SIZE)): # type: ignore
                return True
        return False
    
    def __is_collide_with_self(self):
        for block in self.blocks[1:]:
            if block.rect.colliderect((self.__block_positions[0][0], self.__block_positions[0][1], constant.TILE_SIZE, constant.TILE_SIZE)):
                return True
        return False
    
    def __is_collide_with_wall(self):
        for wall in self.level.walls:
            wall: Wall
            if wall.rect and wall.rect.colliderect((self.__block_positions[0][0], self.__block_positions[0][1], constant.TILE_SIZE, constant.TILE_SIZE)):
                return True
        return False
    
    def __is_collide_with_food(self):
        food = self.level.food
        if food.rect and self.blocks[0].rect.colliderect(food.rect) and food.visible:
            return True
        return False
    
    def __collide_with_active_trap(self):
        pos = None
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            if pygame.sprite.spritecollideany(block, self.level.traps, lambda x, y: x.rect.colliderect(y.rect) and getattr(y, "isActive", False)):
                pos = i
                break
        if pos != None:
            if pos < constant.MIN_LEN:
                self.isDeath = True
            else:   
                self.split(pos)

    def __collide_with_bomb(self):
        pos = None
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            if pygame.sprite.spritecollideany(block, self.level.bombs, lambda x, y: x.rect.colliderect(y.rect) and time() - getattr(y, "activeTime", time()) > 0.6):
                block.kill()
                pos = i if pos == None else pos
        if pos != None:
            if pos < constant.MIN_LEN:
                self.isDeath = True
            else:
                self.split(pos)

        
            

class LevelTest(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()

    def init(self):
        self.remove(self.sprites())
        self.snake = Snake(self, 5)
        self.food = Food()
        self.traps = Traps(self, 10)
        self.keys = Keys(self,2)
        self.coins = Coins(self)
        self.walls = Walls()
        self.obstacles = Obstacle_group(self, 3)
        self.chests = Chests(self, 3)
        self.bombs = Bombs(self, 5)
        self.hud = HUD(self.snake.gold, len(self.snake), self.snake.keys)
        self.food.random_pos(self.snake.blocks)
        self.food_spawn_time = 5000
        self.food_timer = 0
        self.is_paused = False
        self.add(self.hud,self.walls, self.traps,self.obstacles, self.snake, self.food, self.chests, self.coins, self.bombs, self.keys)

    def reset(self):
        # self.remove(self.hud,self.walls, self.traps,self.obstacles, self.snake, self.food, self.chests, self.coins, self.bombs, self.keys)
        self.init()

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(Pause_menu(self.game))

        if self.is_paused:
            return
        self.snake.update()
        self.traps.update()
        self.keys.update()
        self.chests.update()
        self.bombs.update()
        self.coins.update()
        self.hud.update(self.snake.gold, len(self.snake.blocks), self.snake.keys)

        if not self.food.visible:
            self.food_timer += self.game.clock.get_time()
            if self.food_timer > self.food_spawn_time:
                self.food.visible = True
                self.add(self.food)
                self.food.random_pos(self.snake.blocks)
                self.food_timer = 0
                print("Food spawned")
        
        if self.snake.isDeath:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(GameOver_menu(self.game))

    def draw_grid(self, surface: pygame.Surface):
        surface.fill("black")
        pygame.draw.rect(
            surface,
            (51, 54, 71),
            (
                MAP_LEFT,
                MAP_TOP,
                MAP_WIDTH,
                MAP_HEIGHT,
            ),
        )
        for x in range(MAP_LEFT, MAP_RIGHT + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100), (x, MAP_TOP), (x, MAP_BOTTOM))
        for y in range(MAP_TOP, MAP_BOTTOM + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100), (MAP_LEFT, y), (MAP_RIGHT, y))

    def draw_stamina(self, surface: pygame.Surface):
        if self.snake.stamina > 0:
            pygame.draw.rect(
                surface, "cyan", (6.5*constant.TILE_SIZE, 2.5*constant.TILE_SIZE+4, self.snake.stamina * 128 // 100, 24)
            )
            pygame.draw.rect(
                surface, (192,237,250), (6.5*constant.TILE_SIZE, 2.5*constant.TILE_SIZE+4, self.snake.stamina * 128 // 100, 4)
            )
        pygame.draw.rect(
                surface, (133,133,133), (6.5*constant.TILE_SIZE-4, 2.5*constant.TILE_SIZE, self.snake.max_stamina * 128 // 100 + 6, 32), 4, 0, 0, 10, 0, 10
            )

    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        self.draw_grid(surface)
        self.draw_stamina(surface)

        return super().draw(surface)


def main():
    pass


if __name__ == "__main__":
    main()
