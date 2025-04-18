import random
import inspect
from typing import Any
import pygame
from pygame.math import Vector2

from levels.components.bomb import Bomb, BombState
from levels.components.fire_tile import Fire_Tile
from levels.components.trap import TrapState
from ui.screens.game_over import GameOver_menu
from utils.help import Share, to_dark_color
import config.constant as constant
from levels.components.obstacle import Obstacle
from levels.components.wall import Wall
from stats import StatType, Stats
from utils.pixil import Pixil
from ui.screens.Stats_Menu import base_stats_value


class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, layer, pos: tuple[int, int], color: pygame.Color) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            (constant.TILE_SIZE, constant.TILE_SIZE), pygame.SRCALPHA)
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
        self.time_severed = 0
        self.is_severed = False  # Tracks if this block is severed from the snake's main body
        self.is_edible = False
        self.transform_type = None
        self.can_collide = False
        self.health = 3
        self.is_burning = False
        self.burning_time = 2
        self.take_damage_delay = 0.5
        self.time = 0

    @property
    def is_head(self):
        return self.__is_head

    def take_fire_damage(self, damage):
        if self.time >= self.take_damage_delay:  # NOTE: nhận sát thương khi hết delay
            self.time = 0
            self.is_burning = True
            self.health -= damage

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
                        # NOTE: pos bị lệch khoảng nhỏ nên cần thêm 1
                        constant.TILE_SIZE +
                        int(self.target_pos.x != self.pos.x),
                        constant.TILE_SIZE +
                        int(self.target_pos.y != self.pos.y),
                    ), pygame.SRCALPHA
                )
                self.image.fill(to_dark_color(self.color, 10 * (3 - self.health)))
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
                    d_x + constant.TILE_SIZE +
                    int(self.target_pos.x != self.pos.x),
                    d_y + constant.TILE_SIZE +
                    int(self.target_pos.y != self.pos.y),
                ), pygame.SRCALPHA
            )
            self.image.fill(to_dark_color(self.color, 10 * (3 - self.health)))
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

    def update(self):
        
        self.time += Share.clock.get_time() / 1000
        if self.is_burning:
            if self.time >= self.burning_time:  # NOTE: thời gian để thoát khỏi trạng thái đốt
                self.is_burning = False
                self.time = 0
                
        if self.is_severed:
            self.time_severed -= Share.clock.get_time() / 1000
            if self.time_severed >= 0:
                if self.time_severed <= 0.2:
                    self.image.fill((255, 255, 255))  # type: ignore
                return
            snake = self.groups()[0]
            if self.transform_type == "COIN":
                from entities.items.instant.coin import CoinEntity
                for _ in range(random.randint(6, 8)):
                    snake.level.item_group.add(CoinEntity(snake.level, self.rect, 2))  # type: ignore
            elif self.transform_type == "BOMB":
                snake.level.bomb_group.add(Bomb(snake.level, self.rect.topleft, BombState.ACTIVE)) # type: ignore
            elif self.transform_type == "FIRE":
                snake.level.fire_group.add(Fire_Tile(snake.level, self.rect.center, 2, 2, 5)) # type: ignore
            self.kill()

    def sever(self, type, delay):
        self.is_severed = True
        self.time_severed = delay
        self.transform_type = type


class Snake(pygame.sprite.AbstractGroup):
    def __init__(self, level, init_len):

        # Initialize base components
        self.run_time_overriding = {}
        super().__init__()

        # Visual appearance
        self.color = getattr(self, "color", pygame.Color(255, 139, 38))
        self.headImg = getattr(self, "headImg", Pixil.load(
            constant.Texture.snake_head, 1).frames[0])

        # Item and skill management
        from systems.inventory_manager import InventoryManager
        self.inventory = InventoryManager(self)
        from levels.level import Level
        self.level: Level = level

        # Snake state
        self.is_dead = False
        self.blocks: list[SnakeBlock] = []
        self.direction = Vector2(0, 0)
        self._last_direction = Vector2(0, 0)
        self.is_curling = True
        self.time_die = 0

        # Movement and stamina attributes
        self.base_stats = base_stats_value()
        self.update_stats()
        self.stamina = self.base_stats.energy_cap
        self.is_speed_boost = False
        self.speed_cool_down = 0

        # Movement control modes
        self.auto_state = True

        # Out-of-bounds handling
        self._will_go_out_of_bounds = False
        self._out_of_bounds_time = None

        # Player resources
        self.gold = 0
        self.keys = 0

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

    def __len__(self):
        return len(self.blocks)

    def _init_snake_blocks(self, init_len):
        for i in range(init_len):
            x = (constant.SCREEN_WIDTH_TILES // 2) * constant.TILE_SIZE
            y = constant.MAP_BOTTOM - constant.TILE_SIZE
            block = SnakeBlock(int(i == 0), (x, y), self.color)
            self.blocks.append(block)

        self.blocks[0].is_head = True

        self._block_positions = [block.pos.copy() for block in self.blocks]

        for block in self.blocks[::-1]:
            self.add(block)

    def handle_input(self) -> bool:
        '''
        trả về true nếu có sự kiện nhấn phím
        '''
        keys = pygame.key.get_pressed()
        is_pressed = False

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
            ):
                self.direction = direction
                is_pressed = True

        if keys[pygame.K_SPACE]:
            self.is_speed_boost = True
        else:
            self.is_speed_boost = False

        return is_pressed

    def handle_movement(self):
        for snake_block in self.blocks:
            if snake_block.moving:
                return

        if self.is_dead:
            return
        head_pos = self._block_positions[0]
        new_head_pos = head_pos + self.direction * constant.TILE_SIZE

        self._block_positions.insert(0, new_head_pos)

        if self._is_collide(self._block_positions[0]):
            self._block_positions.pop(0)
            if not self._will_go_out_of_bounds:
                # print("Snake died after", self.base_stats.resistance, "out of bounds!")
                self._out_of_bounds_time = 0
            self._will_go_out_of_bounds = True
            return

        self._last_direction = self.direction
        self._will_go_out_of_bounds = False

        if len(self._block_positions) > len(self.blocks):
            self._block_positions.pop()

    def handle_collision(self):
        self._collide_with_active_trap()
        self._collide_with_bomb()

    def handle_go_out_of_bounds(self, dt):
        if self._will_go_out_of_bounds and self.auto_state:
            if self._out_of_bounds_time != None:
                if self._out_of_bounds_time / 1000 > self.base_stats.resistance:
                    self.is_dead = True
                else:
                    self._out_of_bounds_time += dt
        else:
            self._out_of_bounds_time = None

    def update(self):
        if self.is_dead:
            self.time_die += Share.clock.get_time() / 1000
            for block in self.blocks:
                block: SnakeBlock
                block.image.fill((255, 255, 255))  # type: ignore
            if self.time_die > 0.05:
                self.die()
                self.time_die = 0

        if len(self.blocks) <= constant.MIN_LEN:
            self.is_dead = True
            return

        self.update_stats()
        dt = self.level.game.clock.get_time()
        # self.handle_severed_blocks()
        is_press = self.handle_input()

        # một là đang trong trạng thái tự động, hai là có sự kiện nhấn phím
        if self.auto_state or is_press:
            self.handle_movement()

        self.handle_go_out_of_bounds(dt)
        self.handle_speed_boost()
        self.handle_collision()
        self.handle_skills(dt)
        self.check_blocks_health()
        self.inventory.update()
        # print(self._block_positions, end=" " * 50 + "\r", flush=True)
        for i, block in enumerate(self.blocks):
            block.set_target(
                # NOTE: test stats (speed)
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

        for block in self.sprites():
            block.update()

    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        t = super().draw(surface)
        return t

    def grow_up(self, length=1):
        tail = self.blocks[-1]
        for i in range(length * self.base_stats.food_potency):
            newBlock = SnakeBlock(0, tail.rect.topleft, self.color)
            self.blocks.insert(-1, newBlock)
            self._block_positions.append(newBlock.pos.copy())
            for i in self.blocks[0].groups():
                i.add(newBlock)  # type: ignore

    def check_blocks_health(self):
        # print(len(self.sprites()), list(sprite.health for sprite in self.sprites()))
        for index, block in enumerate(self.sprites()):
            if block.health <= 0:
                self.split(index)

    def split(self, index, transform_type='', delay=2):
        for i, block in enumerate(self.blocks[index:]):
            # block.is_severed = True
            block.sever(transform_type, delay + 0.1 * i)
            # block.image.fill((255, 255, 255)) # type: ignore

        self.blocks = self.blocks[:index]
        self._block_positions = self._block_positions[:index]
        if len(self.blocks) <= constant.MIN_LEN:
            self.is_dead = True

    def handle_speed_boost(self):
        if self.is_speed_boost:
            if self.stamina > 0:
                self.base_stats.speed *= constant.BOOST_MULTIPLIER
                self.stamina -= constant.STAMINA_DECREASE
        else:
            if self.stamina < self.base_stats.energy_cap:
                self.stamina = min(self.base_stats.energy_cap,
                                   self.stamina + self.base_stats.energy_regen)

    def _is_collide(self, position):
        if self._is_collide_with_wall(position) or self._is_collide_with_obstacle(position) or self._is_collide_with_self(position) or self._is_collide_with_orther_snake(position):
            return True
        return False

    def _is_collide_with_obstacle(self, position):
        for obstacle in self.level.obstacle_group:
            obstacle: Obstacle
            
            if obstacle.rect.colliderect((position[0], position[1], constant.TILE_SIZE, constant.TILE_SIZE)):# type: ignore
                return True
        return False

    def _is_collide_with_self(self, position):
        if self.is_curling:
            return False
        for block in self.sprites():
            if block == self.blocks[0]:
                continue
            if block.rect.colliderect(
                (
                    position[0],
                    position[1],
                    constant.TILE_SIZE,
                    constant.TILE_SIZE,
                )
            ):
                if block.is_edible:
                    # code ở đây tệ vl
                    block.kill()
                    self.grow_up(1)
                    continue
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
            trap = pygame.sprite.spritecollideany(block, self.level.trap_group)
            if not trap is None:
                if trap.state == TrapState.ACTIVATED:
                    pos = i
                break
        if pos != None:
            self.split(pos)

    def _collide_with_bomb(self):
        pos = None
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            bom = pygame.sprite.spritecollideany(
                block, self.level.bomb_group)  # type: ignore
            if not bom is None:
                bom: Bomb
                if bom.state == BombState.EXPLOSION:
                    block.kill()
                    pos = i if pos == None else pos
        if pos != None:
            self.split(pos)

    def _is_collide_with_orther_snake(self, position):
        for snake in self.level.snake_group._sub_group__:  # type: ignore
            snake: Snake
            if snake == self:
                continue
            if snake.is_dead:
                continue
            for block in snake.sprites():
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

    def handle_skills(self, dt):
        pass

    def curl_snake(self):
        if not self.is_curling:
            self.is_curling = True
            self.direction = Vector2(0, 0)

    def update_stats(self):
        self.base_stats.speed = constant.BASE_SPEED * \
            (1 + Stats.getValue(StatType.SPEED)/100)
        self.base_stats.resistance = constant.DEATH_DELAY * \
            (1 + Stats.getValue(StatType.RESISTANCE)/100)
        self.base_stats.energy_cap = 10 * constant.TILE_SIZE * \
            (1 + Stats.getValue(StatType.ENERGY_CAPACITY)/100)
        self.base_stats.energy_regen = constant.STAMINA_RECOVERY * \
            (1 + Stats.getValue(StatType.ENERGY_REGEN)/100)
        self.base_stats.food_potency = int(
            1 + Stats.getValue(StatType.FOOD_POTENCY)//25)
        Stats.setValue(StatType.LENGTH, len(self.blocks))

    def die(self):
        if len(self.blocks) == 0:
            self.level.game.state_stack[-1].visible = False
            self.level.game.state_stack.append(GameOver_menu(self.level.game))
            return
        block = self.blocks.pop(0)
        self._block_positions.pop(0)
        block: SnakeBlock
        block.kill()

# class GreenSnake(Snake):
#     from levels import level # type: ignore
#     def __init__(self, level: "level.Level", init_len):
#         self.color = pygame.Color("#0abf2b")
#         self.headImg = Pixil.load("game-assets/graphics/pixil/SNAKE_HEAD.pixil", 1).frames[1]
#         super().__init__(level, init_len)

#     def handle_go_out_of_bounds(self, dt):
#         if self._will_go_out_of_bounds:
#             if self._out_of_bounds_time != None:
#                 if self._out_of_bounds_time / 1000 > constant.DEATH_DELAY/1.2 * (1 + Stats.getValue("RESISTANCE")/100):
#                     block = self.blocks.pop()
#                     block.kill()
#                     self._out_of_bounds_time = None
#                     self._will_go_out_of_bounds = False
#                 else:
#                     self._out_of_bounds_time += dt
#         else:
#             self._out_of_bounds_time = None

# class OrangeSnake(Snake):
#     from levels import level # type: ignore

#     def __init__(self, level: "level.Level", init_len):
#         Stats.setValue("ENERGY REGEN", 50)
#         Stats.setValue("RESISTANCE", 20)
#         Stats.setValue("SPEED", 20)
#         self.color = pygame.Color(255, 139, 38)
#         self.headImg = Pixil.load(constant.Texture.snake_head, 1).frames[0]
#         super().__init__(level, init_len)

# class GraySnake(Snake):
#     from levels import level # type: ignore
#     def __init__(self, level: "level.Level", init_len):
#         self.color = pygame.Color("#d3d3d3")
#         self.headImg = Pixil.load(constant.Texture.snake_head, 1).frames[2]
#         super().__init__(level, init_len)

#     def handle_skills(self, dt):
#         self.skillCooldown = getattr(self, "skillCooldown", 5000)
#         self.skillCooldown += dt
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_e] and self.skillCooldown > 5000:
#             self.skillCooldown = 0
#             self.split(-1)

#     def handle_severed_blocks(self):
#         for block in self.sprites():
#             if block not in self.blocks:
#                 block: SnakeBlock
#                 if block.rect.colliderect(
#                     self.blocks[0].rect
#                 ):
#                     block.kill()
#                     self.grow_up(1)
#                 block.update(self, "COIN")
