import random
import constant
import pixil
from time import time
import pygame


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


class Traps(pygame.sprite.AbstractGroup):
    def __init__(self, level, traps_pos) -> None:
        super().__init__()
        self.traps_pos = traps_pos
        
        # if len(self.traps_pos) == 0:
        for x,y in self.traps_pos:
            self.add(Trap(level, (x,y)))

    def update(self) -> None:
        for trap in self.sprites():
            trap.update()