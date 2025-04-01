from __future__ import annotations
import random
from typing import Any, Literal
import inspect
import pygame
from time import time
from pygame.math import Vector2

from entities.items.item_stack import ItemStack
from entities.items.coin import CoinEntity
from entities.items.item_type import ItemCategory
import utils.pixil as pixil
import config.constant as constant
from levels.components.obstacle import Obstacle
from levels.components.wall import Wall
from stats import Stats
from utils.pixil import Pixil
from ui.screens.stats import base_stats_value

class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, layer, pos: tuple[int, int], color: pygame.Color) -> None:
        super().__init__()
        self.image = pygame.Surface((constant.TILE_SIZE, constant.TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.color = color
        self.image.fill(self.color)
        self.target_pos = pygame.Vector2(self.rect.topleft)
        self.pos = pygame.Vector2(self.rect.topleft)
        self._last_target = pygame.Vector2(self.rect.topleft)
        self._layer = layer
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
            # self.image = pygame.transform.rotate(Snake.headImg, -90)
            pass

    def rotate(self, direction, img):
        if not self.is_head or direction == Vector2(0, 0):
            return
        direction = direction.normalize()
        if direction == Vector2(1, 0):
            self.image = pygame.transform.rotate(img, -90)
        elif direction == Vector2(-1, 0):
            self.image = pygame.transform.rotate(img, 90)
        elif direction == Vector2(0, 1):
            self.image = pygame.transform.rotate(img, 180)
        elif direction == Vector2(0, -1):
            self.image = img

    def set_target(self, speed, target: pygame.Vector2):
        if self.target_pos != target:
            self.moving = True
            self._last_target = self.target_pos
            self.target_pos = target
        self.speed = speed

    def move(self, dt, isTurn=False):
        if not self.moving:
            self.speed = 0
            return False

        if self.pos.distance_to(self.target_pos) <= 0:
            self.pos = self.target_pos
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
            self.moving = False

        if not isTurn:
            self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
            if not self.is_head:
                self.image = pygame.surface.Surface(
                    (
                        constant.TILE_SIZE + int(self.target_pos.x != self.pos.x), #NOTE: pos bị lệch khoảng nhỏ nên cần thêm 1
                        constant.TILE_SIZE + int(self.target_pos.y != self.pos.y),
                    )
                )
                self.image.fill(self.color)
            self.rect.topleft = (
                int(self.pos.x),
                int(self.pos.y),
            )
        else:
            self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
            d_x = abs(self.target_pos.x - self.pos.x)
            d_y = abs(self.target_pos.y - self.pos.y)
            self.image = pygame.surface.Surface(
                (
                    d_x + constant.TILE_SIZE + int(self.target_pos.x != self.pos.x),
                    d_y + constant.TILE_SIZE + int(self.target_pos.y != self.pos.y),
                )
            )
            self.image.fill(self.color)
            if self.target_pos.x > self.pos.x or self.target_pos.y > self.pos.y:
                self.rect = self.image.get_rect(
                    bottomright=(
                        int(self.target_pos.x + constant.TILE_SIZE),
                        int(self.target_pos.y + constant.TILE_SIZE),
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
                # snake.level.coins.add_coin(random.randint(10, 15), self, 1)
                for _ in range(random.randint(10, 15)):
                    snake.level.item_group.add(CoinEntity(snake.level, self.rect, 2))
            self.kill()


class Snake(pygame.sprite.AbstractGroup):
    # from states import LevelTest
    
    def __init__(self, level, init_len):
        # Initialize base components
        self.run_time_overriding = {}
        super().__init__()

        # Visual appearance
        self.color = getattr(self, "color", pygame.Color(255, 139, 38))
        self.headImg = getattr(self, "headImg", Pixil.load(constant.Texture.snake_head, 1).frames[0])
        
        # Item and skill management
        self.skill_slot: list[ItemStack | None] = [None, None, None]
        self.item_slot: list [ItemStack | None] = [None, None]
        self.level = level

        # Movement and stamina attributes
        self.max_stamina = 10 * constant.TILE_SIZE
        self.stamina = 10 * constant.TILE_SIZE
        self.is_speed_boost = False
        self.speed_cool_down = 0
        self.base_speed = 16
        self.previous_time = pygame.time.get_ticks()
        
        # Snake state
        self.is_death = False
        self.blocks: list[SnakeBlock] = []
        self.base_speed = constant.BASE_SPEED * (1 + Stats.getValue("SPEED")/100)
        self.gold = 0
        self.keys = 0
        self.direction = Vector2(1, 0)
        self._last_direction = Vector2(0, 0)
        self.is_curling = False

        # Movement control modes
        self.auto_state = True
        self.manual_state = False

        # Out-of-bounds handling
        self._will_go_out_of_bounds = False
        self._out_of_bounds_time = None

        # Player resources
        self.coins = 0
        self.gold = 0
        self.keys = 0
        self.base_stats = base_stats_value()

        # Initialize the snake blocks
        self._init_snake_blocks(init_len)


    # NOTE: Intercept method calls to apply runtime overrides
    def __getattribute__(self, name: str) -> Any:
        try:
            # Use object.__getattribute__ to avoid infinite recursion
            value = object.__getattribute__(self, name)

            # Only intercept methods and functions
            if not (inspect.isfunction(value) or inspect.ismethod(value)):
                return value

            items_overrides = self.run_time_overriding.get(name)
            if items_overrides is None:
                return value

            def wrapper(*args, **kwargs):

                for ret_ in items_overrides["return"]:
                    ret = ret_(self, *args, **kwargs)
                    return ret

                # Apply 'before' interceptors
                for before in items_overrides["before"]:
                    args, kwargs = before(self, *args, **kwargs)

                # Call original method
                ret = value(*args, **kwargs)

                # Apply 'after' interceptors
                for after in items_overrides["after"]:
                    ret = after(self, *args, **kwargs)

                return ret

            return wrapper
        except AttributeError:
            # Handle case where attribute doesn't exist
            raise
    
    def add_item(self, item: ItemStack):

        arr = self.item_slot
        if item.item_type.category == ItemCategory.EQUIPMENT:
            arr = self.skill_slot

        for index, value in enumerate(arr):
            if value is None: continue
            if value.can_stack_with(item):
                arr[index].quantity += 1 # type: ignore
                return 

        for index, value in enumerate(arr):
            if value is None: 
                arr[index] = item
                break
                
            
    def remove_item(self, item: ItemStack):

        arr = self.item_slot
        if item.item_type.category == ItemCategory.EQUIPMENT:
            arr = self.skill_slot

        for index, value in enumerate(arr):
            if value is None: continue
            if value.item_type.id == item.item_type.id: # type: ignore
                arr[index] = None

    def __len__(self):
        return len(self.blocks)

    def _init_snake_blocks(self, init_len):
        x = 0
        y = 0
        for i in range(init_len):
            x = (constant.SCREEN_WIDTH_TILES // 2 - i) * constant.TILE_SIZE
            y = (constant.SCREEN_HEIGHT_TILES // 2) * constant.TILE_SIZE
            block = SnakeBlock(int(i==0) ,(x, y), self.color)
            self.blocks.append(block)

        self.blocks[0].is_head = True

        self._block_positions = [block.pos.copy() for block in self.blocks]

        for block in self.blocks[::-1]:
            self.add(block)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        just_keys = pygame.key.get_just_pressed()

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
            if (
                keys[key]
                and self._last_direction != -direction
                and (((self.auto_state and self._last_direction != direction or self.is_curling)) or not self.auto_state)
                and (
                    self._block_positions[1] - self._block_positions[0] == Vector2(0, 0)
                    or (self._block_positions[1] - self._block_positions[0]).normalize()
                    != direction
                )
            ):  
                self.direction = direction
                self._last_direction = self.direction
                self.is_curling = False
                if self.manual_state:
                    self.handle_movement()
                break
        if keys[pygame.K_SPACE]:
            self.is_speed_boost = True
        else:
            self.is_speed_boost = False
        
        item_map = [
            pygame.K_1, 
            pygame.K_2, 
        ]

        skill_map = [
            pygame.K_3,
            pygame.K_4, 
            pygame.K_5,
        ]

        for index, key in enumerate(item_map):
            if just_keys[key] and self.item_slot[index]:
                self.item_slot[index].use(self) # type: ignore
        
        for index, key in enumerate(skill_map):
            if just_keys[key] and self.skill_slot[index]:
                self.skill_slot[index].use(self) # type: ignore
        

    def handle_movement(self):
        for snake_block in self.blocks:
            if snake_block.moving:
                return

        if self.is_death: return
        head_pos = self._block_positions[0]
        new_head_pos = head_pos + self.direction * constant.TILE_SIZE

        self._block_positions.insert(0, new_head_pos)

        if (
            self._is_collide_with_wall(self._block_positions[0])
            or self._is_collide_with_self(self._block_positions[0])
            or self._is_collide_with_Obstacle(self._block_positions[0])
        ):
            self._block_positions.pop(0)
            if not self._will_go_out_of_bounds:
                print("Snake died after", constant.DEATH_DELAY, "out of bounds!")
                self._out_of_bounds_time = 0
            self._will_go_out_of_bounds = True
            return

        self._will_go_out_of_bounds = False

        if len(self._block_positions) > len(self.blocks):
            self._block_positions.pop()

        

    def handle_collision(self):

        self._collide_with_active_trap()
        self._collide_with_bomb()

        # NOTE: Bây giời cái này ở food rồi 
        # if self.__is_collide_with_food():
        #     self.grow_up(1)

    def handle_go_out_of_bounds(self, dt):
        if self._will_go_out_of_bounds:
            if self._out_of_bounds_time != None:
                if self._out_of_bounds_time / 1000 > constant.DEATH_DELAY:
                    self.isDeath = True
                else:
                    self._out_of_bounds_time += dt
        else:
            self._out_of_bounds_time = None

    def update(self):
        if len(self.blocks) <= constant.MIN_LEN:
            self.is_death = True
            return
        dt = min(pygame.time.get_ticks() - self.previous_time, 20)
        self.previous_time = pygame.time.get_ticks()
        self.handle_severed_blocks()
        self.handle_input()
        if self.auto_state:
            self.handle_movement()
        self.handle_go_out_of_bounds(dt)
        self.handle_speed_boost()
        self.handle_collision()
        self.handle_skills(dt)
        # print(self._block_positions, end=" " * 50 + "\r", flush=True)
        for i, block in enumerate(self.blocks):
            block.set_target(
                self.base_speed, self._block_positions[i]  # NOTE: test stats (speed)
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

    def handle_severed_blocks(self):
        for block in self.sprites():
            if block not in self.blocks:
                block.update(self, "COIN")

    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        t = super().draw(surface)
        return t

    def grow_up(self, length=1):
        tail = self.blocks[-1]
        for i in range(length):
            newBlock = SnakeBlock(0, tail.rect.topleft, self.color)
            self.blocks.insert(-1, newBlock)
            self._block_positions.append(newBlock.pos.copy())
            for i in self.blocks[0].groups():
                i.add(newBlock)  # type: ignore

    def split(self, index):
        for block in self.blocks[index:]:
            if block.timeSevered == None:
                block.timeSevered = time()
        self.blocks = self.blocks[:index]
        self._block_positions = self._block_positions[:index]
        if len(self.blocks) <= constant.MIN_LEN:
            self.is_death = True

    def handle_speed_boost(self):
        if self.is_speed_boost:
            if self.stamina > 0:
                self.base_speed = (constant.BASE_SPEED * (1 + Stats.getValue("SPEED")/100)) * 2
                self.stamina -= constant.STAMINA_DECREASE
            else:
                self.base_speed = constant.BASE_SPEED * (1 + Stats.getValue("SPEED")/100)
        else:
            self.base_speed = constant.BASE_SPEED * (1 + Stats.getValue("SPEED")/100)
            if self.stamina < self.max_stamina * (1 + Stats.getValue("ENERGY CAPACITY")/100):
                self.stamina = min(self.max_stamina, self.stamina + constant.STAMINA_RECOVERY * (1 + Stats.getValue("ENERGY REGEN")/100))

    def _is_collide_with_Obstacle(self, position):
        for obstacle in self.level.obstacle_group:
            obstacle: Obstacle
            if obstacle.rect.colliderect((position[0], position[1], constant.TILE_SIZE, constant.TILE_SIZE)):  # type: ignore
                return True
        return False

    def _is_collide_with_self(self, position):
        if self.is_curling: return False
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

    def _collide_with_active_trap(self):
        pos = None
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            if pygame.sprite.spritecollideany(
                block,
                self.level.trap_group,
                lambda x, y: x.rect.colliderect(y.rect)
                and getattr(y, "isActive", False),
            ):
                pos = i
                break
        if pos != None:
            self.split(pos)

    def _collide_with_bomb(self):
        # pos = None
        # for i in range(len(self.blocks)):
        #     block = self.blocks[i]
        #     if pygame.sprite.spritecollideany(
        #         block,
        #         self.level.,
        #         lambda x, y: x.rect.colliderect(y.rect)
        #         and time() - float(getattr(y, "activeTime", "inf") or "inf") > 0.6,
        #     ):
        #         block.kill()
        #         pos = i if pos == None else pos
        # if pos != None:
        #     self.split(pos)
        pass
        # TODO: xiu nghĩ: để bomb trong nhóm nào là hợp lý hay tạo một nhóm mới luân

    def handle_skills(self, dt):
        pass

    def curl_snake(self):
        if not self.is_curling:
            self.is_curling = True
            self.direction = Vector2(0, 0)
        


class GreenSnake(Snake):

    from levels import level
    def __init__(self, level: "level.Level", init_len):
        self.color = pygame.Color("#0abf2b")
        self.headImg = Pixil.load("game-assets/graphics/pixil/SNAKE_HEAD.pixil", 1).frames[1]
        super().__init__(level, init_len)

    def handle_go_out_of_bounds(self, dt):
        if self._will_go_out_of_bounds:
            if self._out_of_bounds_time != None:
                if self._out_of_bounds_time / 1000 > constant.DEATH_DELAY/1.2 * (1 + Stats.getValue("ARMOUR")/100):
                    block = self.blocks.pop()
                    block.kill()
                    self._out_of_bounds_time = None
                    self._will_go_out_of_bounds = False
                else:
                    self._out_of_bounds_time += dt
        else:
            self._out_of_bounds_time = None

class OrangeSnake(Snake):
    from levels import level

    def __init__(self, level: "level.Level", init_len):
        Stats.setValue("ENERGY REGEN", 50)
        Stats.setValue("ARMOUR", 20)
        Stats.setValue("SPEED", 20)
        self.color = pygame.Color(255, 139, 38)
        self.headImg = Pixil.load(constant.Texture.snake_head, 1).frames[0]
        super().__init__(level, init_len)

class GraySnake(Snake):
    from levels import level
    def __init__(self, level: "level.Level", init_len):
        self.color = pygame.Color("#d3d3d3")
        self.headImg = Pixil.load(constant.Texture.snake_head, 1).frames[2]
        super().__init__(level, init_len)

    def handle_skills(self, dt):
        self.skillCooldown = getattr(self, "skillCooldown", 5000)
        self.skillCooldown += dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and self.skillCooldown > 5000:
            self.skillCooldown = 0
            self.split(-1)

    def handle_severed_blocks(self):
        for block in self.sprites():
            if block not in self.blocks:
                block: SnakeBlock
                if block.rect.colliderect(
                    self.blocks[0].rect
                ):
                    block.kill()
                    self.grow_up(1)
                block.update(self, "COIN")
