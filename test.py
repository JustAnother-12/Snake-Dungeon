import pygame
import sys

TILE_SIZE = 32
WINDOW_SIZE = 640
epsilon = 1e-10

class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.image.fill("blue")
        self.direction = pygame.math.Vector2()
        self.target_pos = pygame.math.Vector2(self.rect.center)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.moving = False
        self.speed = 32
        self.tail_moment = False

    def set_target(self, target_pos):
        self.target_pos = pygame.math.Vector2(target_pos)
        self.moving = True

    def move(self, dt, animation = True):
        if self.moving:
            if self.pos.distance_to(self.target_pos) > 1:
                if animation and not self.tail_moment:
                    self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
                    self.rect.center = (int(self.pos.x), int(self.pos.y))
                elif self.tail_moment:
                    self.pos = self.pos.move_towards(self.target_pos, self.speed * dt)
                    self.image = pygame.surface.Surface((abs(self.target_pos.x - self.pos.x) + TILE_SIZE, abs(self.target_pos.y - self.pos.y) + TILE_SIZE))
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
            self.set_target(self.pos + direction * TILE_SIZE)
            return True
        return False


class Snake:
    def __init__(self, init_len):
        self.blocks: list[pygame.sprite.GroupSingle[SnakeBlock]] = []
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
        
        self.blocks[-1].sprite.tail_moment = True
        self.blocks[-1].sprite.image.fill("red")
        
        # Set initial direction for head
        self.blocks[0].sprite.direction = pygame.math.Vector2(1, 0)
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
            # Update body segments to follow
            for i in range(1, len(self.blocks)-1):
                curr_block = self.blocks[i].sprite
                curr_block.set_target(self.last_positions[i-1])
                curr_block.move(dt, False)

            # Update tail
            tail.set_target(self.last_positions[-2])
            tail.move(dt)
        

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)


class World:
    def __init__(self):
        self.snake = Snake(3)

    def update(self, dt):
        self.snake.update(dt)

    def draw(self, surface):
        self.snake.draw(surface)


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode([WINDOW_SIZE, WINDOW_SIZE], pygame.SCALED)
        pygame.display.set_caption("Smooth Snake Movement in Pygame")
        self.clock = pygame.time.Clock()
        self.world = World()
        self.running = True
        self.show_grid = True

    @staticmethod
    def draw_grid():
        rows = int(WINDOW_SIZE / TILE_SIZE)
        display = pygame.display.get_surface()
        gap = WINDOW_SIZE // rows
        for i in range(rows):
            pygame.draw.line(display, "grey", (0, i * gap), (WINDOW_SIZE, i * gap))
            for j in range(rows):
                pygame.draw.line(display, "grey", (j * gap, 0), (j * gap, WINDOW_SIZE))

    def update(self, dt):
        self.window.fill("white")
        self.world.update(dt)
        self.world.draw(self.window)
        if self.show_grid:
            self.draw_grid()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 100.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.show_grid = not self.show_grid

            self.update(dt)
            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
                