import random
from constant import LEFT_RIGHT_BORDER_TILES, SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE, COIN_VALUE, TOP_BOTTOM_BORDER_TILES
from gui_element.text_class import TextElement;
import constant
import pixil
from time import time
import pygame


# Hàm kiểm tra xem khu vực có trống không
def is_area_free(x, y, size, grid):
    for i in range(size):
        for j in range(size):
            if x + i >= constant.FLOOR_TILE_SIZE or y + j >= constant.FLOOR_TILE_SIZE or grid[x + i][y + j] == 1:
                return False
    return True

# Hàm đánh dấu ô đã chiếm
def mark_area(x, y, size, grid):
    for i in range(size):
        for j in range(size):
            grid[x + i][y + j] = 1

regions = [pixil.get_coords_from_pixil("game-assets/region/trap_squareborder.pixil", (180,180,180)), 
           pixil.get_coords_from_pixil("game-assets/region/frame_L_border.pixil", (180,180,180)), 
           pixil.get_coords_from_pixil("game-assets/region/4dots.pixil", (180,180,180))
           ]


# print(traps_pos)

class Trap(pygame.sprite.Sprite):
    def __init__(self, level, pos) -> None:
        super().__init__()
        self.level = level
        self.pos = pos
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1
        ).frames[0]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.isActive = False
        self.collisionTime = None

    # def random_pos(self):
    #     self.pos = pygame.Vector2(
    #         random.randint(
    #             constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
    #             (
    #                 SCREEN_WIDTH_TILES
    #                 - constant.LEFT_RIGHT_BORDER_TILES
    #                 - 2
    #                 - constant.WALL_TILES
    #             ),
    #         )
    #         * TILE_SIZE,
    #         random.randint(
    #             constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
    #             (
    #                 SCREEN_HEIGHT_TILES
    #                 - constant.TOP_BOTTOM_BORDER_TILES
    #                 - 2
    #                 - constant.WALL_TILES
    #             ),
    #         )
    #         * TILE_SIZE,
    #     )

    def reset(self):
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1
        ).frames[0]
        self.isActive = False
        self.collisionTime = None

    def on_collision(self):
        if self.collisionTime == None:
            self.collisionTime = time()

    def active(self):
        self.isActive = True
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1
        ).frames[1]
    
    def update(self):
        if self.__is_collision_with_snake() and not self.isActive:
            self.on_collision()
            
        if not self.collisionTime == None:
            if time() - self.collisionTime > 1.5:
                self.reset()
            elif time() - self.collisionTime > 1:
                self.active()
    
    def __is_collision_with_snake(self):
        return pygame.sprite.spritecollideany(self, self.level.snake.blocks) # type: ignore

    # def on_collision(self, src):
    #     if not self.collisionTime:
    #         self.collision()
    #     if self.isActive:
    #         print("Sập bẫy rồi con giun.")


class Traps(pygame.sprite.AbstractGroup):
    def __init__(self, level) -> None:
        super().__init__()
        self.traps_pos = []
        self.get_region(level)
        
        # if len(self.traps_pos) == 0:
        for x,y in self.traps_pos:
            self.add(Trap(level, (x,y)))

    def get_region(self,level):
        placed = set()
        for x,y in random.choices(regions)[0]:
            if (x,y) not in placed and is_area_free(x,y,2,level.grid):
                self.traps_pos.append((x*constant.TILE_SIZE+LEFT_RIGHT_BORDER_TILES*TILE_SIZE+64,y*constant.TILE_SIZE+TOP_BOTTOM_BORDER_TILES*TILE_SIZE+64))
                mark_area(x,y,2,level.grid)
                placed.add((x,y))

    def update(self) -> None:
        for trap in self.sprites():
            trap.update()


class Coin(pygame.sprite.Sprite):
    def __init__(self,  level, area: pygame.Rect | None = None, r = 2) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/GOLD_LEVEL.pixil", 1
        ).frames[0]
        self.random_pos(area, r)
        self.rect = self.image.get_rect(center=self.pos)

    def random_pos(self, area: pygame.Rect | None, r = 2):
        if not area:
            self.pos = pygame.Vector2(
                random.randint(
                    constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                    (
                        SCREEN_WIDTH_TILES
                        - constant.LEFT_RIGHT_BORDER_TILES
                        - constant.WALL_TILES
                    ),
                )
                * TILE_SIZE,
                random.randint(
                    constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                    (
                        SCREEN_HEIGHT_TILES
                        - constant.TOP_BOTTOM_BORDER_TILES
                        - constant.WALL_TILES
                    ),
                )
                * TILE_SIZE,
            )
        else:
            R = int(r * constant.TILE_SIZE)
            x = random.randint(
                area.centerx - R - area.width // 2,
                area.centerx + R + area.width // 2,
            )
            if (
                x < area.centerx - area.width // 2
                or x > area.centerx + area.width // 2
            ):
                y = random.randint(
                    area.centery - R - area.height // 2,
                    area.centery + R + area.height // 2,
                )
            else:
                y = random.choice(
                    [
                        random.randint(
                            area.centery - R - area.height // 2,
                            area.centery - area.height // 2,
                        ),
                        random.randint(
                            area.centery + area.height // 2,
                            area.centery + R + area.height // 2,
                        ),
                    ]
                )
            self.pos = pygame.Vector2(x, y)
            if (
                x < (constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES) * TILE_SIZE + 4
                or x > (SCREEN_WIDTH_TILES - constant.LEFT_RIGHT_BORDER_TILES - constant.WALL_TILES) * TILE_SIZE - 4
                or y < (constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES) * TILE_SIZE + 4
                or y > (SCREEN_HEIGHT_TILES - constant.TOP_BOTTOM_BORDER_TILES - constant.WALL_TILES) * TILE_SIZE - 4
            ):
                self.random_pos(area)

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()

    def __is_collision_with_snake(self):
        return pygame.sprite.spritecollideany(self, self.level.snake.blocks)
    
    def on_collision(self):
        self.kill()
        self.level.snake.gold += COIN_VALUE


class Coins(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity: int = 0) -> None:
        super().__init__()
        self.level = level
        for _ in range(quantity):
            self.add(Coin(self.level))

    def add_coin(self, quantity, source, r = 2):
        for _ in range(quantity):
            self.add(Coin(self.level, source.rect, r))
        self.level.add(self.sprites())

    def update(self):
        for coin in self.sprites():
            coin.update()


class Chest(pygame.sprite.Sprite):
    def __init__(self, level, isLocked = None) -> None:
        super().__init__()
        self.level = level
        self.isLocked = isLocked if isLocked != None else random.choice([True, False])
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/CHEST_SHEET.pixil", 1, constant.TILE_SIZE
        ).frames[int(self.isLocked)]
        self.random_pos()
        self.rect = self.image.get_rect(center=self.pos)
        self.isClosed = True
        self.collision_time = None
        self.alpha = 255
        self.LockedText = TextElement("LOCKED!", "White", 8, int(self.pos[0]) - TILE_SIZE - 8, int(self.pos[1]) - 2*TILE_SIZE, "midleft")
        self.TextTime = None

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(
                constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES + 1,
                (
                    SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 3
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
            random.randint(
                constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES + 1,
                (
                    SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 3
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
        )

    def update(self) -> None:
        if self.TextTime != None:
            if time() - self.TextTime > 2:
                self.LockedText.kill()
        if self.__is_collision_with_snake():
            self.on_collision()
        if not self.isClosed:
            self.image = pixil.Pixil.load(
                "game-assets/graphics/pixil/CHEST_SHEET.pixil", 1, constant.TILE_SIZE
            ).frames[2]
        if not self.collision_time == None:
            if(time() - self.collision_time > 2):
                if not self.image == None:
                    self.alpha = max(0,self.alpha-5)
                    self.image = self.image.copy()
                    self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
                    if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
                        self.kill()
                    # self.FadeOut(self.image)

    # def FadeOut(self, sprite:pygame.Surface):
    #     self.alpha = max(0,self.alpha-5)
    #     sprite = sprite.copy()
    #     sprite.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
    #     if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
    #         self.kill()


    def __is_collision_with_snake(self):
        return self.rect and self.rect.colliderect(self.level.snake.blocks[0].rect)
    
    def OpenChest(self):
        self.isClosed = False
        print("Open chest")
        self.level.coins.add_coin(random.randint(7, 15), self)
        self.collision_time = time()

    def on_collision(self):
        if self.isClosed:
            if not self.isLocked:
                self.OpenChest()
            else:
                if self.level.snake.keys > 0:
                    self.level.snake.keys -= 1
                    self.OpenChest()
                else:
                    self.level.add(self.LockedText)
                    self.TextTime = time()

class Chests(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity) -> None:
        super().__init__()
        for _ in range(quantity):
            self.add(Chest(level))

    def update(self) -> None:
        for chest in self.sprites():
            chest.update()

class Key(pygame.sprite.Sprite):
    """
    Key to open the locked chest
    """

    def __init__(self,  level) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/KEY_SPRITE.pixil", 2
        ).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(center=self.pos)

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(
                constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES + 1,
                (
                    SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 3
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
            random.randint(
                constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES + 1,
                (
                    SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 3
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
        )

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()

    def __is_collision_with_snake(self):
        return pygame.sprite.spritecollideany(self, self.level.snake.blocks)
    
    def on_collision(self):
        self.kill()
        self.level.snake.keys += 1

class Keys(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity) -> None:
        super().__init__()
        for _ in range(quantity):
            self.add(Key(level))

    def update(self) -> None:
        for key in self.sprites():
            key.update()


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, type, angle=0) -> None:
        super().__init__()
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/WALL_SHEETS.pixil", 1
        ).frames[type]
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(topleft=pos)


class Walls(pygame.sprite.AbstractGroup):
    def __init__(self) -> None:
        super().__init__()
        top = constant.TOP_BOTTOM_BORDER_TILES * TILE_SIZE
        left = constant.LEFT_RIGHT_BORDER_TILES * TILE_SIZE
        bottom = (
            SCREEN_HEIGHT_TILES - constant.TOP_BOTTOM_BORDER_TILES - constant.WALL_TILES
        ) * TILE_SIZE
        right = (
            SCREEN_WIDTH_TILES - constant.LEFT_RIGHT_BORDER_TILES - constant.WALL_TILES
        ) * TILE_SIZE
        for y in range(
            top + constant.WALL_TILES * TILE_SIZE,
            bottom,
            constant.WALL_TILES * TILE_SIZE,
        ):
            self.add(Wall((left, y), random.randint(0, 3), 90))
            self.add(Wall((right, y), random.randint(0, 3), 270))

        for x in range(
            left + constant.WALL_TILES * TILE_SIZE,
            right,
            constant.WALL_TILES * TILE_SIZE,
        ):
            self.add(Wall((x, top), random.randint(0, 3)))
            self.add(Wall((x, bottom), random.randint(0, 3), 180))

        self.add(Wall((left, top), 4))
        self.add(Wall((left, bottom), 4, 90))
        self.add(Wall((right, bottom), 4, 180))
        self.add(Wall((right, top), 4, 270))

class Bomb(pygame.sprite.Sprite):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/BOMB_SHEET.pixil", 1
        ).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(topleft=self.pos)
        self.activeTime = None
        self.timeAppear = time()

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(
                constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                (
                    SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 1
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
            random.randint(
                constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                (
                    SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 1
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
        )

    def __is_collision_with_snake(self):
        return pygame.sprite.spritecollideany(self, self.level.snake.blocks)

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()
        if self.activeTime != None:
            if time() - self.activeTime < 1:
                self.image = pixil.Pixil.load(
                    "game-assets/graphics/pixil/EXPLOSION_ANIMATION.pixil", 1
                ).frames[int((time() - self.activeTime) * 7)]
                self.rect = self.image.get_rect(topleft=self.pos- pygame.Vector2(TILE_SIZE, TILE_SIZE))
            else:
                self.kill()
        # elif time() - self.timeAppear > 3:
        #     self.activeTime = time()

    def on_collision(self):
        if not self.activeTime:
            self.activeTime = time()

class Bomb_group(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity = 0) -> None:
        super().__init__()
        self.level = level
        for _ in range(quantity):
            self.add(Bomb(self.level))
        
    def update(self):
        for bomb in self.sprites():
            bomb.update()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/OBSTACLE_TILE.pixil", 2).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(topleft=self.pos)

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(
                constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                (
                    SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 2
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
            random.randint(
                constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                (
                    SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 2
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
        )

    # def update(self):
    #     if self.__is_collision_with_snake():
    #         self.on_collision()
    
    # def __is_collision_with_snake(self):
    #     return pygame.sprite.spritecollideany(self, self.level.snake.blocks)
    
    # def on_collision(self):
    #     return True

class Obstacle_group(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity) -> None:
        super().__init__()
        self.level = level
        for _ in range(quantity):
            self.add(Obstacle(self.level))

    # def update(self):
    #     for obstacle in self.sprites():
    #         obstacle.update()

class Pot(pygame.sprite.Sprite):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/POTS_SPRITE_SHEET.pixil", 1).frames[random.randint(0,3)]

        self.random_pos()
        self.rect = self.image.get_rect(topleft = self.pos)
        self.collision_time = None
        self.alpha = 255
        self.isClosed = True


    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(
                constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES + 1,
                (
                    SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 3
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
            random.randint(
                constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES + 1,
                (
                    SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 3
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
        )

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()
        if not self.isClosed:
            self.image = pixil.Pixil.load("game-assets/graphics/pixil/POTS_SPRITE_SHEET.pixil", 1).frames[4]
        if not self.collision_time == None:
            if(time() - self.collision_time > 2):
                if not self.image == None:
                    self.alpha = max(0,self.alpha-5)
                    self.image = self.image.copy()
                    self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
                    if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
                        self.kill()

    def __is_collision_with_snake(self):
        return self.rect and self.rect.colliderect(self.level.snake.blocks[0].rect)
    
    def open(self):
        self.isClosed = False
        print("Break pot!")
        self.level.coins.add_coin(random.randint(1, 3), self, 1)
        if self.collision_time == None:
            self.collision_time = time()

    def on_collision(self):
        if self.isClosed:
            self.open()

class Pot_group(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity) -> None:
        super().__init__()
        self.level = level
        for _ in range(quantity):
            self.add(Pot(self.level))

    def update(self):
        for pot in self.sprites():
            pot.update()


# class CollisionManager:
#     def __init__(self, game) -> None:
#         self.game = game
# class CollisionManager:
#     def __init__(self, game) -> None:
#         from states import LevelTest
#         self.level: LevelTest.LevelTest = game

#     def update(self):
#         self.check_collision_trap()
#         self.check_collision_food()

#     def check_collision_trap(self):
#         for trap in self.lever.traps.sprites():
#             if check_collision(trap, self.lever.snake.blocks):
#                 trap.on_collision(self.lever.snake)
    
#     def check_collision_food(self):
#         if not self.lever.food.visible: return
#         if check_collision(self.lever.food, self.lever.snake.blocks[0:1]):
#             self.lever.food.visible = False
#             self.lever.remove(self.lever.food)
#             self.lever.food_timer = 0
#             self.lever.snake.grow_up()
    
#     def check_collisions_snake(self):
#         pass
#         # if check_collision(self.lever.snake.blocks[0], self.lever.snake.blocks[2:]):
#         #     pass
    
#     def check_collision_wall(self):
#         pass
#         # if check_collision(self.lever.snake.blocks[0], self.lever.walls):
#         #     pass
            