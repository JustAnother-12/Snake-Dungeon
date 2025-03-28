import random
from constant import LEFT_RIGHT_BORDER_TILES, TILE_SIZE, TOP_BOTTOM_BORDER_TILES
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
           pixil.get_coords_from_pixil("game-assets/region/trap_frame_L_border.pixil", (180,180,180)), 
           pixil.get_coords_from_pixil("game-assets/region/trap_4dots.pixil", (180,180,180))
           ]

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