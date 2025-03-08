from hmac import new
from operator import truediv
import random
import pygame
import sys
from pygame.math import Vector2

TILE_SIZE = 32
WINDOW_SIZE = 640

def check_collision(food, snake_blocks) -> bool:
    all_snake_parts = pygame.sprite.Group()
    for block_group in snake_blocks:
        all_snake_parts.add(block_group.sprite)
    
    collision = pygame.sprite.spritecollideany(food, all_snake_parts)
    return collision is not None

class Food(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.random_pos()
        self.image: pygame.Surface = pygame.image.load('game-assets/graphics/png/apple.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        self.visible = True

        
    
    def random_pos(self):
        self.pos = Vector2(random.randint(0, WINDOW_SIZE//TILE_SIZE - 1) * TILE_SIZE, random.randint(0, WINDOW_SIZE//TILE_SIZE - 1) * TILE_SIZE)

    def draw(self, surface):
        if self.visible:
            self.rect = self.image.get_rect(topleft=self.pos)
            surface.blit(self.image, self.rect)

class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image:pygame.Surface = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.image.fill((255,139,38))
        # self.image.fill((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
        self.direction = Vector2()
        self.target_pos = Vector2(self.rect.center)
        self.pos = Vector2(self.rect.center)
        self.moving = False
        self.speed = 32
        self.tail_movement = False

    def set_target(self, target_pos):
        self.target_pos = Vector2(target_pos)
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
                    self.image = pygame.surface.Surface((d_x + (2 if d_x > 0 else 0) + TILE_SIZE, d_y + (2 if d_y > 0 else 0) + TILE_SIZE))
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
            self.direction = direction
            self.set_target(self.pos + direction * TILE_SIZE)
            return True
        return False


class Snake:
    def __init__(self, init_len):
        self.blocks: list[pygame.sprite.GroupSingle[SnakeBlock]] = []  # type: ignore
        # bao gồm head và body tail và tail giả
        # một cái có animation, cái còn lại không
        x = 0
        y = 0
        for i in range(init_len):
            x = (init_len-i)*TILE_SIZE
            y = 10*TILE_SIZE
            block_group = pygame.sprite.GroupSingle()
            SnakeBlock((x, y), block_group)
            self.blocks.append(block_group)
        
        self.blocks[0].sprite.image = pygame.transform.rotate(pygame.image.load('game-assets/graphics/png/snake_head.png'), -90)
        self.blocks[-1].sprite.tail_movement = True
        # self.blocks[-1].sprite.image.fill("Red")
        
        # Set initial direction for head
        self.blocks[0].sprite.direction = Vector2(1, 0)
        self.last_positions = [block.sprite.pos.copy() for block in self.blocks]

    def update(self, dt):
        
        # Handle input for head
        head = self.blocks[0].sprite
        tail = self.blocks[-1].sprite
        head_moved = False
        
        if not head.moving:
            self.last_positions = [block.sprite.pos.copy() for block in self.blocks]
            head_moved = head.get_input()

        # Store last positions before movement
        animating = head.move(dt)
        # Update head
        if animating or head_moved:
            if head.direction == Vector2(1,0):
                head.image = pygame.transform.rotate(pygame.image.load('game-assets/graphics/png/snake_head.png'), -90)
            elif head.direction == Vector2(-1,0):
                head.image = pygame.transform.rotate(pygame.image.load('game-assets/graphics/png/snake_head.png'), 90)
            elif head.direction == Vector2(0,1):
                head.image = pygame.transform.rotate(pygame.image.load('game-assets/graphics/png/snake_head.png'), 180)
            elif head.direction == Vector2(0,-1):
                head.image = pygame.image.load('game-assets/graphics/png/snake_head.png')
            # Update body segments to follow
            for i in range(1, len(self.blocks)-1):
                curr_block = self.blocks[i].sprite
                curr_block.set_target(self.last_positions[i-1])
                curr_block.move(dt, False)

            # Update tail
            tail.set_target(self.last_positions[-2])
            tail.move(dt, tail_movement=True)
    
    def grow_up(self):
        tail = self.blocks[-1].sprite
        new_tail = pygame.sprite.GroupSingle()
        SnakeBlock((int(tail.pos.x), int(tail.pos.y)), new_tail)
        self.blocks.insert(-1, new_tail)

    def draw(self, surface):
        for block in reversed(self.blocks):
            block.draw(surface)


class World:
    def __init__(self):
        self.snake = Snake(5)
        self.food = Food()
        self.food_timer = 0
        self.food_spawn_time = 5000  # 5 seconds in milliseconds

    def update(self, dt, actual_dt):
        self.snake.update(dt)
        
        # Update food spawn timer
        if not self.food.visible:
            self.food_timer += actual_dt
            if self.food_timer >= self.food_spawn_time:
                self.food.visible = True
                self.food.random_pos()
                self.food_timer = 0
                print("New food appeared!")
    def draw(self, surface):
        self.snake.draw(surface)
        self.food.draw(surface)


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode([WINDOW_SIZE, WINDOW_SIZE], pygame.SCALED)
        pygame.display.set_caption("Snake Dungeon Game")
        self.clock = pygame.time.Clock()
        self.world = World()
        self.running = True
        self.show_grid = True

    @staticmethod
    def draw_grid():
        rows = int(WINDOW_SIZE / TILE_SIZE)
        display = pygame.display.get_surface()
        gap = WINDOW_SIZE // rows
        if display:
            for i in range(rows):
                pygame.draw.line(display, "grey", (0, i * gap), (WINDOW_SIZE, i * gap))
                for j in range(rows):
                    pygame.draw.line(display, "grey", (j * gap, 0), (j * gap, WINDOW_SIZE))

    def update(self, dt, actual_dt):
        self.window.fill("white")
        if self.show_grid:
            self.draw_grid()
        self.world.update(dt, actual_dt)
        self.world.draw(self.window)

        # Check for collision with all foods
        if self.world.food.visible:
            self.check_collisions()

        

    def check_collisions(self):
        # Check each food for collisions
        if check_collision(self.world.food, self.world.snake.blocks[0:1]):
            self.world.food.visible = False
            self.world.food_timer = 0
            print("food collied")
            self.world.snake.grow_up()
            print(list(x.sprite.image for x in self.world.snake.blocks))
            return True
        return False
    def run(self):
        while self.running:
            actual_dt = self.clock.tick(60)  # This gives us milliseconds since last frame
            dt = actual_dt / 100.0  # Your scaled dt for movement
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.show_grid = not self.show_grid

            self.update(dt, actual_dt)
            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()