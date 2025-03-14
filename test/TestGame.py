from hmac import new
from operator import truediv
from time import sleep, time
import pygame
import sys
from pygame.math import Vector2
from CollectableSprite import Food, Key, Coin
from const import TILE_SIZE, WINDOW_SIZE, check_collision, HEAD_IMG, DEATH_DELAY, STAMINA_DECREASE_RATE, STAMINA_RECOVERY_RATE, BOOST_MULTIPLIER
from TrapSprite import Trap

class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image: pygame.Surface = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.image.fill((255, 139, 38))
        # self.image.fill((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
        self.direction = Vector2(1, 0)
        self.target_pos = Vector2(self.rect.center)
        self.pos = Vector2(self.rect.center)
        self.moving = False
        self.speed = 32
        self.tail_movement = False
        self.isOutside = False

    def set_target(self, target_pos):
        self.target_pos = Vector2(target_pos)
        self.moving = True

    def move(self, dt, animation=True, tail_movement=False):
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
                    self.image = pygame.surface.Surface((d_x + TILE_SIZE, d_y + TILE_SIZE))
                    self.image.fill((255,139,38))
                    if self.target_pos.x > self.pos.x or self.target_pos.y > self.pos.y:
                         self.rect = self.image.get_rect(bottomright = (int(self.target_pos.x + TILE_SIZE//2), int(self.target_pos.y + TILE_SIZE//2)))
                    else:
                         self.rect = self.image.get_rect(topleft = (int(self.target_pos.x - TILE_SIZE//2), int(self.target_pos.y - TILE_SIZE//2)))
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
            if direction == Vector2(1, 0) and self.pos.x > WINDOW_SIZE - TILE_SIZE:
                self.isOutside = True
                self.image = pygame.transform.rotate(
                    HEAD_IMG, -90
                )
                return False
            if direction == Vector2(0, 1) and self.pos.y > WINDOW_SIZE - TILE_SIZE:
                self.isOutside = True
                self.image = pygame.transform.rotate(
                    HEAD_IMG, 180
                )
                return False
            if direction == Vector2(-1, 0) and self.pos.x < TILE_SIZE:
                self.isOutside = True
                self.image = pygame.transform.rotate(
                    HEAD_IMG, 90
                )
                return False
            if direction == Vector2(0, -1) and self.pos.y < TILE_SIZE:
                self.isOutside = True
                self.image = HEAD_IMG
                return False
            
            self.direction = direction
            self.set_target(self.pos + direction * TILE_SIZE)
            self.isOutside = False
            return True
        return False

class Snake:
    def __init__(self, init_len):
        self.stamina = 100
        self.coins = 0
        self.blocks: list[pygame.sprite.GroupSingle[SnakeBlock]] = []  # type: ignore
        # bao gồm head và body tail và tail giả
        # một cái có animation, cái còn lại không
        x = 0
        y = 0
        for i in range(init_len):
            x = (init_len - i) * TILE_SIZE
            y = WINDOW_SIZE // 2 - TILE_SIZE
            block_group = pygame.sprite.GroupSingle()
            SnakeBlock((x, y), block_group)
            self.blocks.append(block_group)

        self.blocks[0].sprite.image = pygame.transform.rotate(
            HEAD_IMG, -90
        )
        self.blocks[-1].sprite.tail_movement = True
        # self.blocks[-1].sprite.image.fill("Red")

        # Set initial direction for head
        self.blocks[0].sprite.direction = Vector2(1, 0)
        self.last_positions = [block.sprite.pos.copy() for block in self.blocks]

        # Add stamina attribute
        self.stamina = 100
        self.is_boosting = False
        self.out_of_bounds_time = None
        self.is_out_of_bounds = False


    def boost(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for block in self.blocks:
                block.sprite.speed *= 2
            print("Boost on")

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            for block in self.blocks:
                block.sprite.speed //= 2
            print("Boost off")
                

    def update(self, dt):

        # Handle input for head
        head = self.blocks[0].sprite
        tail = self.blocks[-1].sprite
        head_moved = False

        if not head.moving:
            self.last_positions = [block.sprite.pos.copy() for block in self.blocks]
            head_moved = head.get_input()

        if head.isOutside:
            if not self.is_out_of_bounds:
                self.is_out_of_bounds = True
                self.out_of_bounds_time = time()
            elif self.out_of_bounds_time and time() - self.out_of_bounds_time > DEATH_DELAY:
                print("Snake died after 2 seconds out of bounds!")
                sys.exit()
        else:
            self.is_out_of_bounds = False
            self.out_of_bounds_time = None

        # Handle stamina and boosting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.stamina > 0:
            self.is_boosting = True
            self.stamina -= STAMINA_DECREASE_RATE
        else:
            self.is_boosting = False
            self.stamina = min(100, self.stamina + STAMINA_RECOVERY_RATE)

        # Adjust speed based on boosting
        speed_multiplier = BOOST_MULTIPLIER if self.is_boosting else 1

        # Store last positions before movement
        animating = head.move(dt * speed_multiplier)
        # Update head
        if animating or head_moved:
            if head.direction == Vector2(1, 0):
                head.image = pygame.transform.rotate(
                    HEAD_IMG, -90
                )
            elif head.direction == Vector2(-1, 0):
                head.image = pygame.transform.rotate(
                    HEAD_IMG, 90
                )
            elif head.direction == Vector2(0, 1):
                head.image = pygame.transform.rotate(
                    HEAD_IMG, 180
                )
            elif head.direction == Vector2(0, -1):
                head.image = HEAD_IMG
            # Update body segments to follow
            for i in range(1, len(self.blocks) - 1):
                curr_block = self.blocks[i].sprite
                curr_block.set_target(self.last_positions[i - 1])
                curr_block.move(dt * speed_multiplier, False)

            # Update tail
            tail.set_target(self.last_positions[-2])
            tail.move(dt * speed_multiplier, tail_movement=True)

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
        self.keys = pygame.sprite.Group()
        self.keys.add(Key())
        self.coins = pygame.sprite.Group()
        for _ in range(30):
            self.coins.add(Coin())
        self.traps = pygame.sprite.Group()
        for _ in range(10):
            self.traps.add(Trap())
        self.food.random_pos(self.snake.blocks)
        self.food_timer = 0
        self.food_spawn_time = 5000  # 5 seconds in milliseconds

    def update(self, dt, actual_dt):
        self.snake.update(dt)

        # Update food spawn timer
        if not self.food.visible:
            self.food_timer += actual_dt
            if self.food_timer >= self.food_spawn_time:
                self.food.visible = True
                self.food.random_pos(self.snake.blocks)
                self.food_timer = 0
                print("New food appeared!")

    def draw(self, surface):
        self.traps.draw(surface)
        self.coins.draw(surface)
        self.food.draw(surface)
        self.keys.draw(surface)
        self.snake.draw(surface)


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
                pygame.draw.line(display, "white", (0, i * gap), (WINDOW_SIZE, i * gap))
                for j in range(rows):
                    pygame.draw.line(
                        display, "white", (j * gap, 0), (j * gap, WINDOW_SIZE)
                    )

    def draw_stamina(self, stamina):
        if stamina <= 0: return
        image = pygame.surface.Surface((128*stamina//100, 16))
        rect = image.get_rect(topleft = (0, 16))
        image.fill((0, 255, 255))
        self.window.blit(image, rect)

    def update(self, dt, actual_dt):
        self.window.fill("gray")
        if self.show_grid:
            self.draw_grid()
        self.draw_stamina(self.world.snake.stamina)
        self.world.update(dt, actual_dt)
        self.world.draw(self.window)

        # Check for collision with all foods
        if self.world.food.visible:
            self.check_collisions_food()
        
        if self.check_collisions_snake():
            sleep(1)
            self.running = False
        
        self.check_collision_key()
        self.check_collision_coin()
        self.check_collision_trap()
        for trap in self.world.traps:
            trap.update()

    def check_collisions_food(self):
        # Check each food for collisions
        if check_collision(self.world.food, self.world.snake.blocks[0:1]):
            self.world.food.visible = False
            self.world.food_timer = 0
            print("food collied")
            self.world.snake.grow_up()
            return True
        return False
    
    def check_collisions_snake(self):
        if check_collision(self.world.snake.blocks[0].sprite, self.world.snake.blocks[2:]):
            return True
        return False
    
    def check_collision_key(self):
        for key in self.world.keys:
            if check_collision(key, self.world.snake.blocks[0:1]):
                key.kill()

    def check_collision_coin(self):
        for coin in self.world.coins:
            if check_collision(coin, self.world.snake.blocks[0:1]):
                self.world.snake.coins += 10
                print(f"Coin: {self.world.snake.coins}")
                coin.kill()

    def check_collision_trap(self):
        for trap in self.world.traps:
            if check_collision(trap, self.world.snake.blocks[0:1]):
                if not trap.collisionTime:
                    trap.collision()
                if trap.isActive:
                    print("Sập bẫy rồi con giun.")

    def run(self):
        while self.running:
            actual_dt = self.clock.tick(
                60
            )  # This gives us milliseconds since last frame
            dt = actual_dt / 100.0  # Your scaled dt for movement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # self.world.snake.boost(event)
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
