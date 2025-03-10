
import random
from re import I, S
import pygame
from states import Pause_menu
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
        self.target_pos = target
        # self.direction = (target - self.pos).normalize()
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
        
        self.sprites()[-1].tail_movement = True

        self.sprites()[0].direction = pygame.Vector2(1, 0)
        self.last_positons = [block.pos.copy() for block in self.sprites()]
        self.stamina = 100
        self.is_boosting = False
        self.last_time = pygame.time.get_ticks()

    def boost(self):
        if self.stamina > 0:
            self.is_boosting = True
            self.stamina -= 1
        else:
            self.is_boosting = False
    
    def update(self):
        blocks = self.sprites()
        dt = pygame.time.get_ticks() - self.last_time
        dt = dt / 100.0
        self.last_time = pygame.time.get_ticks()

        head = blocks[0]
        tail = blocks[-1]
        head_move = False

        if not head.moving:
            self.last_positions = [block.pos.copy() for block in blocks]
            head_move = head.get_input()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.stamina > 0:
            self.is_boosting = True
            # TODO: magic number
            self.stamina -= 1
        else:
            self.is_boosting = False
            # TODO: magic number
            self.stamina = min(100, self.stamina + 0.1)

        # Magic number 
        speed_multiplier = 2 if self.is_boosting else 1

        animating = head.move(dt * speed_multiplier)

        if animating or head_move:
            # TODO: làm tạm
            if head.direction == Vector2(1, 0):
                head.image = pygame.transform.rotate(
                    pygame.image.load("game-assets/graphics/png/snake_head.png"), -90
                )
            elif head.direction == Vector2(-1, 0):
                head.image = pygame.transform.rotate(
                    pygame.image.load("game-assets/graphics/png/snake_head.png"), 90
                )
            elif head.direction == Vector2(0, 1):
                head.image = pygame.transform.rotate(
                    pygame.image.load("game-assets/graphics/png/snake_head.png"), 180
                )
            elif head.direction == Vector2(0, -1):
                head.image = pygame.image.load(
                    "game-assets/graphics/png/snake_head.png"
                )
            
            for i in range(1, len(blocks) - 1):
                curr_block = blocks[i]
                curr_block.set_target(self.last_positions[i - 1])
                curr_block.move(dt * speed_multiplier, False)

        tail.set_target(self.last_positions[-2])
        tail.move(dt * speed_multiplier, tail_movement=True)


class LevelTest(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()
    
    def init(self):
        self.snake = Snake()
        self.food = Food()
        self.food_spawn_time = 5000
        self.food_timer = 0
        self.is_paused = False
        self.add(self.snake, self.food)
    
    def reset(self):
        self.remove(self.snake, self.food)
        self.init()

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game.state_stack[-1].visible = False 
            self.game.state_stack.append(Pause_menu.Pause_menu(self.game))

        if self.is_paused: return
        self.snake.update()
        if not self.food.visible:
            self.food_timer += self.game.clock.get_time()
            if self.food_timer > self.food_spawn_time:
                self.food.visible = True
                self.food.random_pos()
                self.food_timer = 0
                print("Food spawned")

    def draw_grid(self, surface: pygame.Surface):
        surface.fill("white")
        for x in range(0, constant.SCREEN_WIDTH_TILES * constant.TILE_SIZE, constant.TILE_SIZE):
            pygame.draw.line(surface, "black", (x, 0), (x, constant.SCREEN_HEIGHT_TILES * constant.TILE_SIZE))
        for y in range(0, constant.SCREEN_HEIGHT_TILES * constant.TILE_SIZE, constant.TILE_SIZE):
            pygame.draw.line(surface, "black", (0, y), (constant.SCREEN_WIDTH_TILES * constant.TILE_SIZE, y))
        
    def draw_stamina(self, surface: pygame.Surface):
        if self.snake.stamina > 0:
            pygame.draw.rect(surface, "green", (0, 16, self.snake.stamina//100 * 128, 10))
    
    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        self.draw_grid(surface)
        self.draw_stamina(surface)
        return super().draw(surface)
    

def main():
    pass



if __name__ == "__main__":
    main()