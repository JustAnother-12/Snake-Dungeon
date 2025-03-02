from __future__ import annotations
import enum
import pygame
from pygame.sprite import Sprite, AbstractGroup

TILE_SIZE = 32


class SnakeBlockType(enum.Enum):
    HEAD = 0
    BODY = 1
    FAKE_TAIL = 2
    TAIL = 3

class SnakeBlock(Sprite):
    def __init__(self, pos_grid: tuple[int, int], type: SnakeBlockType) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image: pygame.Surface = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=(pos_grid[0] * TILE_SIZE, pos_grid[1] * TILE_SIZE))
        self.target_pos = pygame.math.Vector2(self.rect.center)
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.moving = False
        self.speed = 2
        self.type = type

        self.get_texture()
   
    @property 
    def grid_pos(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.topleft) // TILE_SIZE
    
    @grid_pos.setter
    def grid_pos(self, pos: pygame.Vector2) -> None:
        self.rect.topleft = pos * TILE_SIZE

    def get_texture(self) -> pygame.surface.Surface:
        
        if self.type == SnakeBlockType.HEAD:
            self.image.fill("red")
        elif self.type == SnakeBlockType.BODY:
            self.image.fill("blue")
        elif self.type == SnakeBlockType.TAIL:
            self.image.fill("green")

        return self.image
    
    def set_target(self, target_pos: tuple[int, int]) -> None:
        self.target_pos = pygame.math.Vector2(target_pos)
        self.moving = True
    
    def move(self):
        if not self.moving:
            return False
        
        if self.pos.distance_to(self.target_pos) <= 1 or self.type == SnakeBlockType.BODY:
            self.pos = self.target_pos
            self.rect.center = (int(self.pos.x), int(self.pos.y))
            self.moving = False
            return False
        
        if self.type == SnakeBlockType.TAIL:
            self.pos = self.pos.move_towards(self.target_pos, self.speed)
            self.image = pygame.surface.Surface((abs(self.target_pos.x - self.pos.x) + TILE_SIZE, abs(self.target_pos.y - self.pos.y) + TILE_SIZE))
            self.rect = self.image.get_rect(center = (self.pos.x + (self.target_pos.x - self.pos.x) / 2, self.pos.y + (self.target_pos.y - self.pos.y) / 2))
            self.get_texture()
            return

        self.pos = self.pos.move_towards(self.target_pos, self.speed)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        return True
         

class Snake(pygame.sprite.Group):
    def __init__(self, pos_grid: tuple[int, int], init_len: int) -> None:
        pygame.sprite.Group.__init__(self)
        self.direction = pygame.math.Vector2()
        self.head = SnakeBlock(pos_grid, SnakeBlockType.HEAD)
        self.add(self.head)
        for i in range(init_len - 1):
            self.add(SnakeBlock((pos_grid[0], pos_grid[1] + i), SnakeBlockType.BODY))
        self.add(SnakeBlock((pos_grid[0], pos_grid[1] + init_len - 1), SnakeBlockType.TAIL))
        
    def get_input(self) -> bool:
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = pygame.math.Vector2(0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = pygame.math.Vector2(0, 1)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = pygame.math.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = pygame.math.Vector2(1, 0)
        
        if direction.length() > 0:
            self.direction = direction
            next_ = (self.head.pos + direction * TILE_SIZE)
            self.head.set_target((int(next_.x), int(next_.y)))
            blocks = self.sprites()
            for i in range(1, len(blocks)):
                blocks[i].set_target(blocks[i - 1].pos)
            return True
        return False

    def move(self) -> None:
        blocks : list[SnakeBlock] = self.sprites()
        for block in blocks:
            block.move()
    
    def is_moving(self) -> bool:
        return self.head.moving
    
    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        return super().draw(surface)
    
class World(pygame.Surface):
    def __init__(self, world_size: tuple[int, int]) -> None:
        super().__init__(world_size)
        self.snake = Snake((2, 2), 3)
    
    def update(self) -> None:
        if not self.snake.is_moving():
            self.snake.get_input()
        self.draw_grid()
        self.snake.move()
        self.snake.draw(self)

    def draw_grid(self) -> None:
        rows = int(800 / TILE_SIZE)
        gap = 800 // rows
        for i in range(rows):
            pygame.draw.line(self, "grey", (0, i * gap), (800, i * gap))
            for j in range(rows):
                pygame.draw.line(self, "grey", (j * gap, 0), (j * gap, 800))

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.world = World((self.screen_info.current_w, self.screen_info.current_h))
    
    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
    
    def draw_grid(self) -> None:
        rows = int(800 / TILE_SIZE)
        display = pygame.display.get_surface()
        gap = 800 // rows
        if display is None:
            return
        for i in range(rows):
            pygame.draw.line(display, "grey", (0, i * gap), (800, i * gap))
            for j in range(rows):
                pygame.draw.line(display, "grey", (j * gap, 0), (j * gap, 800))
            
    def update(self) -> None:
        self.screen.fill("white")
        self.world.update()
        self.screen.blit(self.world, (0, 0), (0,0 , 800, 600))
        self.draw_grid()
        
if __name__ == "__main__":
    game = Game()
    game.run()
    
    