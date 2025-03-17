import random
from constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import constant
import pixil
from time import time
from logic.Collision import check_collision
import pygame

class Trap(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.random_pos()
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[0]
        self.rect = self.image.get_rect(topleft = self.pos)
        self.isActive = False
        self.collisionTime = None

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES, (SCREEN_WIDTH_TILES - constant.LEFT_RIGHT_BORDER_TILES - 2 - constant.WALL_TILES)) * TILE_SIZE,
            random.randint(constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES, (SCREEN_HEIGHT_TILES - constant.TOP_BOTTOM_BORDER_TILES - 2 - constant.WALL_TILES)) * TILE_SIZE
        )
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self):
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[0]
        self.isActive = False
        self.collisionTime = None

    def collision(self):
        self.collisionTime = time()
    
    def active(self):
        self.isActive = True
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[1]

    def update(self):
        if not self.collisionTime == None:
            if time() - self.collisionTime > 1.5:
                self.reset()
            elif time() - self.collisionTime > 1:
                self.active()


    def on_collision(self, src):
        if not self.collisionTime:
            self.collision()
        if self.isActive:
            print("Sập bẫy rồi con giun.")

class Traps(pygame.sprite.AbstractGroup):
    def __init__(self, quantity) -> None:
        super().__init__()
        for _ in range(quantity):
            self.add(Trap())

    def update(self) -> None:
        for trap in self.sprites():
            trap.update()

class Coin(pygame.sprite.Sprite):
    def __init__(self, *group: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*group)
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/GOLD_LEVEL.pixil", 1).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(center = self.pos)

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES, (SCREEN_WIDTH_TILES - constant.LEFT_RIGHT_BORDER_TILES - 2 - constant.WALL_TILES)) * TILE_SIZE,
            random.randint(constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES, (SCREEN_HEIGHT_TILES - constant.TOP_BOTTOM_BORDER_TILES - 2 - constant.WALL_TILES)) * TILE_SIZE
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Key(pygame.sprite.Sprite):
    '''
    Key to open looked chest
    '''

    def __init__(self, *group: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*group)
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/KEY_SPRITE(1).pixil", 2).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(center = self.pos)

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(0 + TILE_SIZE//2, SCREEN_WIDTH_TILES - TILE_SIZE//2),
            random.randint(0 + TILE_SIZE//2, SCREEN_HEIGHT_TILES - TILE_SIZE//2)
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, type, angle = 0) -> None:
        super().__init__()
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/WALL_SHEETS.pixil", 1).frames[type]
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(topleft = pos)

class Walls(pygame.sprite.AbstractGroup):
    def __init__(self) -> None:
        super().__init__()
        top = constant.TOP_BOTTOM_BORDER_TILES * TILE_SIZE
        left = constant.LEFT_RIGHT_BORDER_TILES * TILE_SIZE
        bottom = (SCREEN_HEIGHT_TILES - constant.TOP_BOTTOM_BORDER_TILES - constant.WALL_TILES) * TILE_SIZE
        right = (SCREEN_WIDTH_TILES - constant.LEFT_RIGHT_BORDER_TILES - constant.WALL_TILES) * TILE_SIZE
        for y in range(top + constant.WALL_TILES*TILE_SIZE, bottom, constant.WALL_TILES*TILE_SIZE):
            self.add(Wall((left, y), random.randint(0, 3), 90))
            self.add(Wall((right, y), random.randint(0, 3), 270))

        for x in range(left + constant.WALL_TILES*TILE_SIZE, right, constant.WALL_TILES*TILE_SIZE):
            self.add(Wall((x, top), random.randint(0, 3)))
            self.add(Wall((x, bottom), random.randint(0, 3), 180))
            
        self.add(Wall((left, top), 4))
        self.add(Wall((left, bottom), 4, 90))
        self.add(Wall((right, bottom), 4, 180))
        self.add(Wall((right, top), 4, 270))

class CollisionManager:
    def __init__(self, game) -> None:
        self.game = game

    def update(self):
        self.check_collision_trap()

    def check_collision_trap(self):
        for trap in self.game.traps.sprites():
            if check_collision(trap, self.game.snake.blocks):
                trap.on_collision(self.game.snake)

                # self.game.snake.on_collision(trap)