
import random
from re import S
import pygame
from states.state import State
from pixil import Pixil
from pygame.sprite import AbstractGroup
import constant
from pygame.math import Vector2

class Food(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = Pixil.load("game-assets/graphics/pixil/apple.pixil", 1).frames[0]
        self.rect = self.image.get_rect(topleft=(0,0))
        self.visible = True

    def random_pos(self):
        # TODO: Implement this function
        # self.pos = pygame.Vector2(
        #     random.randint(0, )
        # )
        pass
    
    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)

class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((constant.TILE_SIZE, constant.TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.image.fill((255, 139, 38))
        self.direction = pygame.Vector2(0, 0)
        self.target_pos = pygame.Vector2(self.rect.center)
        self.pos = pygame.Vector2(self.rect.center)

        self.moving = False
        self.speed = 32
        self.tail_movement = False
    
    def set_target(self, target: pygame.Vector2):
        self.target = target
        self.direction = (target - self.pos).normalize()
        self.moving = True

    def move(self, dt, animation = True, tail_movement = False):
        self.tail_movement = tail_movement
        if self.moving:
            if self.pos.distance_to(self.target_pos) > 1:
                if animation and not self.tail_movement:
                    self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
                    self.rect.center = (int(self.pos.x), int(self.pos.y))
                elif self.tail_movement:
                    self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
                    d_x = abs(self.target_pos.x - self.pos.x)
                    d_y = abs(self.target_pos.y - self.pos.y)
                    self.image = pygame.surface.Surface((d_x + (1 if d_x > 0.05 else 0) + constant.TILE_SIZE, d_y + (1 if d_y > 0.05 else 0) + constant.TILE_SIZE))
                    self.image.fill((255,139,38))
                    self.rect = self.image.get_rect(center = (self.pos.x + (self.target_pos.x - self.pos.x) / 2, self.pos.y + (self.target_pos.y - self.pos.y) / 2))
                else:
                    self.pos = self.target_pos
                    self.rect.center = (int(self.pos.x), int(self.pos.y))
                    self.moving = False
            else:
                self.pos = self.target_pos
                self.rect.center = (int(self.pos.x), int(self.pos.y))
                self.moving = False
            return True
        return False

    def get_input(self):
        keys = pygame.key.get_pressed()
        direction = Vector2()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = Vector2(0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = Vector2(0, 1)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = Vector2(-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = Vector2(1, 0)

        if direction.length() > 0:
            if self.direction == Vector2(1, 0) and direction == Vector2(-1, 0):
                return False
            if self.direction == Vector2(-1, 0) and direction == Vector2(1, 0):
                return False
            if self.direction == Vector2(0, 1) and direction == Vector2(0, -1):
                return False
            if self.direction == Vector2(0, -1) and direction == Vector2(0, 1):
                return False
            self.direction = direction
            self.set_target(self.pos + direction * constant.TILE_SIZE)
            return True
        return False

class Snake(pygame.sprite.AbstractGroup):
    def __init__(self) -> None:
        AbstractGroup.__init__(self)

        self.stamina = 100
        
        x = 0
        y = 0
        init_length = 3
        for i in range(init_length):
            x = (init_length - i) * constant.TILE_SIZE
            SnakeBlock((x, y), self)
        
        print(self.sprites()[0])

class LevelTest(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.snake = Snake()
        self.food = Food()
        self.food.random_pos()
        self.food_timer = 0
        self.food_spawn_time = 5000 # 5 seconds

        self.add(self.snake, self.food)
    
    def update(self):
        self.snake.update()
        if not self.food.visible:
            self.food_timer += self.game.clock.get_time()
            if self.food_timer > self.food_spawn_time:
                self.food.visible = True
                self.food.random_pos()
                self.food_timer = 0
                print("Food spawned")
    

def main():
    pass



if __name__ == "__main__":
    main()