import random
from constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import constant
import pixil
from time import time
import pygame




class Trap(pygame.sprite.Sprite):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level
        self.random_pos()
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1
        ).frames[0]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.isActive = False
        self.collisionTime = None

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

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self):
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1
        ).frames[0]
        self.isActive = False
        self.collisionTime = None

    def on_collision(self):
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
    def __init__(self, level, quantity) -> None:
        super().__init__()
        for _ in range(quantity):
            self.add(Trap(level))

    def update(self) -> None:
        for trap in self.sprites():
            trap.update()


class Coin(pygame.sprite.Sprite):
    def __init__(self,  level, area: pygame.Rect | None = None) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/GOLD_LEVEL.pixil", 1
        ).frames[0]
        self.random_pos(area)
        self.rect = self.image.get_rect(center=self.pos)

    def random_pos(self, area: pygame.Rect | None):
        if not area:
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
        else:
            x = random.randint(
                area.centerx - constant.TILE_SIZE * 3,
                area.centerx + constant.TILE_SIZE * 3,
            )
            if (
                x < area.centerx - constant.TILE_SIZE
                or x > area.centerx + constant.TILE_SIZE
            ):
                y = random.randint(
                    area.centery - constant.TILE_SIZE * 3,
                    area.centery + constant.TILE_SIZE * 3,
                )
            else:
                y = random.choice(
                    [
                        random.randint(
                            area.centery - constant.TILE_SIZE * 3,
                            area.centery - constant.TILE_SIZE,
                        ),
                        random.randint(
                            area.centery + constant.TILE_SIZE,
                            area.centery + constant.TILE_SIZE * 3,
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
        self.level.gold += 10
        self.level.hud.set_gold(self.level.gold)


class Coins(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity: int = 0) -> None:
        super().__init__()
        self.level = level
        for _ in range(quantity):
            self.add(Coin(self.level))

    def add_coin(self, quantity):
        for _ in range(quantity):
            self.add(Coin(self.level, self.level.chest.rect))
        self.level.add(self.sprites())

    def update(self):
        for coin in self.sprites():
            coin.update()


class Chest(pygame.sprite.Sprite):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/CHEST_SHEET.pixil", 1, constant.TILE_SIZE
        ).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(center=self.pos)
        self.isOpened = False

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
        if self.__is_collision_with_snake():
            self.on_collision()
        if self.isOpened:
            self.image = pixil.Pixil.load(
                "game-assets/graphics/pixil/CHEST_SHEET.pixil", 1, constant.TILE_SIZE
            ).frames[2]

    def __is_collision_with_snake(self):
        return pygame.sprite.spritecollideany(self, self.level.snake.blocks)

    def on_collision(self):
        if not self.isOpened:
            self.isOpened = True
            print("Open chest")
            self.level.coins.add_coin(random.randint(7, 15))


class Key(pygame.sprite.Sprite):
    """
    Key to open the looked chest
    """

    def __init__(self, *group: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*group)
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/KEY_SPRITE(1).pixil", 2
        ).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(center=self.pos)

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(0 + TILE_SIZE // 2, SCREEN_WIDTH_TILES - TILE_SIZE // 2),
            random.randint(0 + TILE_SIZE // 2, SCREEN_HEIGHT_TILES - TILE_SIZE // 2),
        )


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
        elif time() - self.timeAppear > 3:
            self.activeTime = time()

    def on_collision(self):
        if not self.activeTime:
            self.activeTime = time()

class Bombs(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity = 0) -> None:
        super().__init__()
        self.level = level
        for _ in range(quantity):
            self.add(Bomb(self.level))
        
    def update(self):
        for bomb in self.sprites():
            bomb.update()

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
            