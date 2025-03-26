from __future__ import annotations
import pygame
from level_component import Chests, Coins, Keys, Pot_group, Traps, Walls, Bomb_group, Obstacle_group
from states.GameOver_menu import GameOver_menu
from states.state import State
from states.Pause_menu import Pause_menu
from pixil import Pixil
import constant
import random
from logic.help import check_collision
from HUD import HUD

MAP_WIDTH = (
    constant.SCREEN_WIDTH_TILES -
    constant.LEFT_RIGHT_BORDER_TILES * 2 - constant.WALL_TILES * 2
) * constant.TILE_SIZE
MAP_HEIGHT = (
    constant.SCREEN_HEIGHT_TILES -
    constant.TOP_BOTTOM_BORDER_TILES * 2 - constant.WALL_TILES * 2
) * constant.TILE_SIZE
MAP_LEFT = (constant.LEFT_RIGHT_BORDER_TILES +
            constant.WALL_TILES) * constant.TILE_SIZE
MAP_RIGHT = MAP_LEFT + MAP_WIDTH
MAP_TOP = (constant.TOP_BOTTOM_BORDER_TILES +
           constant.WALL_TILES) * constant.TILE_SIZE
MAP_BOTTOM = MAP_TOP + MAP_HEIGHT


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image: pygame.Surface = pygame.transform.scale(
            Pixil.load(constant.Texture.apple, 1).frames[0],
            (constant.TILE_SIZE, constant.TILE_SIZE),
        )
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.visible = True

    def random_pos(self, snake_blocks):
        self.pos = pygame.Vector2(
            (
                random.randint(
                    constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                    constant.SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 2
                    - constant.WALL_TILES,
                )
                * constant.TILE_SIZE
            ),
            (
                random.randint(
                    constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                    constant.SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 2
                    - constant.WALL_TILES,
                )
                * constant.TILE_SIZE
            ),
        )
        self.rect = self.image.get_rect(topleft=self.pos)
        if check_collision(self, snake_blocks):
            self.random_pos(snake_blocks)

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)


class Item:
    def __init__(self, texture: str):
        super().__init__()
        self.image = Pixil.load(texture, 1).frames[0]
        self.active = True
        self.stack = 1
        self.max_stack = 1

    def use(self, snake: Snake):
        pass

    def check_input(self, keys) -> bool:
        return False

    def on_add(self):
        pass

    def on_remove(self):
        pass


class ItemController:
    def __init__(self, level: LevelTest):
        super().__init__()
        self.level = level
        self.items = []

    def update(self):
        keys = pygame.key.get_just_pressed()
        for item in self.items:
            item: Item
            if item.active and item.check_input(keys):
                item.use(self.level.snake)
                item.stack -= 1
                if item.stack == 0:
                    item.active = False
                    item.on_remove()

    def add(self, item: Item):
        self.items.append(item)

    def remove(self, item: Item):
        self.items.remove(item)


class LevelTest(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()

    def init(self):
        from Player import Snake
        self.remove(self.sprites())
        self.snake = Snake(self, 5)
        self.food = Food()
        self.traps = Traps(self, 10)
        self.keys = Keys(self, 2)
        self.coins = Coins(self)
        self.walls = Walls()
        self.obstacles = Obstacle_group(self, 3)
        self.chests = Chests(self, 3)
        self.bombs = Bomb_group(self, 5)
        self.pots = Pot_group(self, 20)
        self.itemController = ItemController(self)
        self.hud = HUD(self.snake.gold, len(self.snake), self.snake.keys)
        self.food.random_pos(self.snake.blocks)
        self.food_spawn_time = 5000
        self.food_timer = 0
        self.is_paused = False
        self.add(self.hud, self.walls, self.traps, self.obstacles,
                 self.food, self.chests, self.pots, self.coins, self.bombs, self.keys, self.snake)

    def reset(self):
        # self.remove(self.hud,self.walls, self.traps,self.obstacles, self.snake, self.food, self.chests, self.coins, self.bombs, self.keys)
        self.init()

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(Pause_menu(self.game))

        if self.is_paused:
            return
        self.snake.update()
        self.traps.update()
        self.keys.update()
        self.chests.update()
        self.pots.update()
        self.bombs.update()
        self.coins.update()
        self.itemController.update()
        self.hud.update(self.snake.gold, len(
            self.snake.blocks), self.snake.keys)

        if not self.food.visible:
            self.food_timer += self.game.clock.get_time()
            if self.food_timer > self.food_spawn_time:
                self.food.visible = True
                self.add(self.food)
                self.food.random_pos(self.snake.blocks)
                self.food_timer = 0
                print("Food spawned")

        if self.snake.isDeath:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(GameOver_menu(self.game))

    def draw_grid(self, surface: pygame.Surface):
        surface.fill("black")
        pygame.draw.rect(
            surface,
            (51, 54, 71),
            (
                MAP_LEFT,
                MAP_TOP,
                MAP_WIDTH,
                MAP_HEIGHT,
            ),
        )
        for x in range(MAP_LEFT, MAP_RIGHT + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100),
                             (x, MAP_TOP), (x, MAP_BOTTOM))
        for y in range(MAP_TOP, MAP_BOTTOM + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100),
                             (MAP_LEFT, y), (MAP_RIGHT, y))

    def draw_stamina(self, surface: pygame.Surface):
        if self.snake.stamina > 0:
            pygame.draw.rect(
                surface, "cyan", (6.5*constant.TILE_SIZE, 2.5 *
                                  constant.TILE_SIZE+4, self.snake.stamina * 128 // 100, 24)
            )
            pygame.draw.rect(
                surface, (192, 237, 250), (6.5*constant.TILE_SIZE, 2.5 *
                                           constant.TILE_SIZE+4, self.snake.stamina * 128 // 100, 4)
            )
        pygame.draw.rect(
            surface, (133, 133, 133), (6.5*constant.TILE_SIZE-4, 2.5*constant.TILE_SIZE,
                                       self.snake.max_stamina * 128 // 100 + 6, 32), 4, 0, 0, 10, 0, 10
        )

    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        self.draw_grid(surface)
        self.draw_stamina(surface)

        return super().draw(surface)


def main():
    pass


if __name__ == "__main__":
    main()
