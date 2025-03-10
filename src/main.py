from __future__ import annotations
import enum
import pygame
from pygame.sprite import Sprite
import json, base64
from io import BytesIO
import time
import random

from pixil_classdata import PixilType

TILE_SIZE = 16
SCREEN_WIDTH_TILES = 56
SCREEN_HEIGHT_TILES = 48

class Pixil:
    def __init__(self, frames: list[pygame.Surface], frames_delay_ms: list[int], original_size: tuple[int, int], zoom: int) -> None:
        self.frames = frames
        self.frames_delay_ms = frames_delay_ms
        self.current_frame = 0
        self.stat_time = time.time()
    
    def update(self) -> None:
        if time.time() - self.stat_time >= self.frames_delay_ms[self.current_frame] / 1000:
            self.current_frame += 1
            self.current_frame %= len(self.frames)
            self.stat_time = time.time()
    
    def get_current_frame(self) -> pygame.Surface:
        surf = self.frames[self.current_frame] 
        return surf

    @classmethod
    def load(cls, path: str, scale: int):

        with open(path) as file:
            pixil_file = PixilType.from_dict(json.loads(file.read()))
            frames_raw = list(filter(lambda x: x.active == True, pixil_file.frames))
            frames: list[pygame.Surface] = [] * len(frames_raw)
            frames_delay: list[int] = [] * len(frames_raw)
            for i, frame in enumerate(frames_raw):
                surface = pygame.Surface((pixil_file.width * scale, pixil_file.height * scale))
                surface.fill((255, 255, 255, 0))
                for layer in frame.layers:
                    buff = BytesIO(base64.b64decode(layer.src.split(",")[1]))
                    image = pygame.image.load(buff)
                    image.set_alpha(layer.opacity * 255)
                    surface.blit(pygame.transform.scale(image, (pixil_file.width * scale, pixil_file.height * scale)), (0, 0))
                frames.append(surface)
                frames_delay.append(frame.speed)
            
            return cls(frames, frames_delay, (pixil_file.width, pixil_file.height), scale)

class SnakeBlockType(enum.Enum):
    HEAD = 0
    BODY = 1
    FAKE_TAIL = 2
    TAIL = 3

class Food(Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.random_pos()
        self.image: pygame.Surface = pygame.image.load('game-assets/graphics/png/apple.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        self.visible = True

    def random_pos(self) -> None:
        self.pos = pygame.Vector2(pygame.Vector2(random.randint(0, SCREEN_WIDTH_TILES - 1) * TILE_SIZE, random.randint(0, SCREEN_HEIGHT_TILES - 1) * TILE_SIZE))
    
    def draw(self, surface: pygame.Surface) -> None:
        if self.visible:
            self.rect = self.image.get_rect(topleft=self.pos)
            surface.blit(self.image, self.rect)

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
        self.direction = pygame.math.Vector2(0,0)

        self.get_texture()
   
    @property 
    def grid_pos(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.topleft) // TILE_SIZE
    
    @grid_pos.setter
    def grid_pos(self, pos: pygame.Vector2) -> None:
        self.rect.topleft = pos * TILE_SIZE

    def get_texture(self) -> pygame.surface.Surface:
        self.image.fill((255, 139, 38)) 

        return self.image
    
    def set_target(self, target_pos: tuple[int, int]) -> None:
        self.direction = (pygame.math.Vector2(target_pos) - self.pos)
        self.target_pos = pygame.math.Vector2(target_pos)
        self.moving = True
    
    def move(self):
        if not self.moving:
            return False
        
        if self.pos.distance_to(self.target_pos) <= 1 or self.type == SnakeBlockType.BODY:
            self.pos = self.target_pos
            self.rect.center = (int(self.pos.x), int(self.pos.y))
            self.moving = False
            self.get_texture()
            return False
        
        if self.type == SnakeBlockType.TAIL:
            self.pos = self.pos.move_towards(self.target_pos, self.speed)
            self.image = pygame.surface.Surface((abs(self.target_pos.x - self.pos.x) + TILE_SIZE, abs(self.target_pos.y - self.pos.y) + TILE_SIZE))
            self.rect = self.image.get_rect(center = (self.pos.x + (self.target_pos.x - self.pos.x) / 2, self.pos.y + (self.target_pos.y - self.pos.y) / 2))
            self.get_texture()
            return

        self.pos = self.pos.move_towards(self.target_pos, self.speed)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.get_texture()
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
        center_grid = (self.get_width() // TILE_SIZE // 2, self.get_height() // TILE_SIZE // 2)
        self.snake = Snake(center_grid, 3)
    
    def update(self) -> None:
        if not self.snake.is_moving():
            self.snake.get_input()
        
        self.fill("white")
        self.draw_grid()
        self.draw_border()
        self.snake.move()
        self.snake.draw(self)

    def draw_border(self) -> None:
        border_rect = pygame.Rect(0,0, SCREEN_WIDTH_TILES*TILE_SIZE, SCREEN_HEIGHT_TILES*TILE_SIZE)
        pygame.draw.rect(self, "black", border_rect,5*TILE_SIZE)
        left_rect = pygame.Rect(5*TILE_SIZE, 5*TILE_SIZE, 4*TILE_SIZE, SCREEN_HEIGHT_TILES*TILE_SIZE - 5*2*TILE_SIZE)
        pygame.draw.rect(self, "black", left_rect)
        right_rect = pygame.Rect((SCREEN_WIDTH_TILES-9)*TILE_SIZE, 5*TILE_SIZE, 4*TILE_SIZE, SCREEN_HEIGHT_TILES*TILE_SIZE - 5*2*TILE_SIZE)
        pygame.draw.rect(self, "black", right_rect)
        

    def draw_grid(self) -> None:

        gap = TILE_SIZE
        for i in range(0, self.get_width(), gap):
            pygame.draw.line(self, "grey", (i, 0), (i, self.height))
            for j in range(0, self.get_height(), gap):
                pygame.draw.line(self, "grey", (0, j), (self.width, j))

class Game:
    def __init__(self) -> None:
        pygame.init()
        # self.screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((TILE_SIZE*SCREEN_WIDTH_TILES, TILE_SIZE*SCREEN_HEIGHT_TILES))
        self.clock = pygame.time.Clock()
        # self.world = World((self.screen_info.current_w, self.screen_info.current_h))
        self.world = World((self.screen.get_width(),self.screen.get_height()))
    
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
            
    def update(self) -> None:
        self.screen.fill("white")
        self.world.update()
        # self.keep_player_center_screen()
        # window_pos = self.get_window_pos()
        player_pos = pygame.Vector2(self.world.snake.head.rect.center)
        player_pos.x -= self.screen.get_width() // 2
        player_pos.y -= self.screen.get_height() // 2

        # self.move_window(int(player_pos.x), int(player_pos.y))

        self.screen.blit(self.world, (0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))
        
if __name__ == "__main__":
    game = Game()
    game.run()
    
    