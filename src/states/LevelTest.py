from typing import Any
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
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__()
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
    def __init__(self, init_len):
        super().__init__()
        self.stamina = 100
        self.blocks: list[SnakeBlock] = []  # type: ignore
        # bao gồm head và body tail và tail giả
        # một cái có animation, cái còn lại không
        x = 0
        y = 0
        for i in range(init_len):
            x = (init_len - i) * constant.TILE_SIZE
            y = 10 * constant.TILE_SIZE
            block = SnakeBlock((x, y))
            self.blocks.append(block)

        self.blocks[0].image = pygame.transform.rotate(
            pygame.image.load("game-assets/graphics/png/snake_head.png"), -90
        )
        self.blocks[-1].tail_movement = True

        # Set initial direction for head
        self.blocks[0].direction = Vector2(1, 0)
        self.last_positions = [block.pos.copy() for block in self.blocks]

        # Add stamina attribute
        self.stamina = 100
        self.is_boosting = False

        self.previous_time = pygame.time.get_ticks()

        for block in self.blocks:
            self.add(block)


    def boost(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for block in self.blocks:
                block.speed *= 2
            print("Boost on")

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            for block in self.blocks:
                block.speed //= 2
            print("Boost off")
    
    def update(self):
        dt = (pygame.time.get_ticks() - self.previous_time) / 100
        self.previous_time = pygame.time.get_ticks()

        # Handle input for head
        head = self.blocks[0]
        tail = self.blocks[-1]
        head_moved = False

        if not head.moving:
            self.last_positions = [block.pos.copy() for block in self.blocks]
            head_moved = head.get_input()

        # Handle stamina and boosting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.stamina > 0:
            self.is_boosting = True
            self.stamina -= constant.STAMINA_DECREASE_RATE
        else:
            self.is_boosting = False
            self.stamina = min(100, self.stamina + constant.STAMINA_RECOVERY_RATE)

        # Adjust speed based on boosting
        speed_multiplier = constant.BOOST_MULTIPLIER if self.is_boosting else 1

        # Store last positions before movement
        animating = head.move(dt * speed_multiplier)
        # Update head
        if animating or head_moved:
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
            
            head.image = pygame.transform.scale(head.image, (constant.TILE_SIZE, constant.TILE_SIZE)) # type: ignore
            # Update body segments to follow
            for i in range(1, len(self.blocks) - 1):
                curr_block = self.blocks[i]
                curr_block.set_target(self.last_positions[i - 1])
                curr_block.move(dt * speed_multiplier, False)

            # Update tail
            tail.set_target(self.last_positions[-2])
            tail.move(dt * speed_multiplier, tail_movement=True)

    def grow_up(self):
        tail = self.blocks[-1]
        new_tail = SnakeBlock((int(tail.pos.x), int(tail.pos.y)))
        self.blocks.insert(-1, new_tail)
        self.add(new_tail)

    def outOfWindow(self):
        head = self.blocks[0]
        if head.rect.right > (constant.SCREEN_HEIGHT_TILES * constant.TILE_SIZE ) or head.rect.bottom > (constant.SCREEN_WIDTH_TILES * constant.TILE_SIZE ) or head.rect.left < 0 or head.rect.top < 0:
            return True
        return False


class LevelTest(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()
    
    def init(self):
        self.snake = Snake(5)
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