from states.state import State
from states.Pause_menu import Pause_menu
import pygame
import constant
from region_generator import RegionGenerator
from level_components.Trap import Traps
from level_components.Chest import Chests
from level_components.Coin import Coins
from level_components.Key import Keys
from level_components.Pot import Pot_group
from level_components.Wall import Walls
from level_components.Bomb import Bomb_group
from level_components.Obstacle import Obstacle_group
from level_components.Food import Food_Group

class Level(pygame.sprite.Group):
    def __init__(self, world) -> None:
        super().__init__()
        self.world = world
        self.init()
    
    def init(self):
        self.remove(self.sprites())
        self.region_generator = RegionGenerator()
        self.traps = Traps(self.world,self.region_generator.traps_initpos)
        self.chests = Chests(self.world, self.region_generator.chests_initpos)
        self.pots = Pot_group(self.world, self.region_generator.pots_initpos)
        self.obstacles = Obstacle_group(self.world, self.region_generator.obstacles_initpos)

        self.foods = Food_Group(self.world)
        self.keys = Keys(self.world, 2)
        self.coins = Coins(self.world)
        self.bombs = Bomb_group(self.world, 5) 
        
        self.walls = Walls()
        self.add(self.traps, self.chests, self.pots, self.obstacles, self.foods, self.keys, self.coins, self.bombs, self.walls)
    
    def reset(self):
        self.init()

    def update(self):
        self.traps.update()
        self.keys.update()
        self.chests.update()
        self.pots.update()
        self.bombs.update()
        self.coins.update()
        self.foods.update()

    def draw_grid(self, surface: pygame.Surface):
        surface.fill("black")
        pygame.draw.rect(
            surface,
            (51, 54, 71),
            (
                constant.MAP_LEFT,
                constant.MAP_TOP,
                constant.MAP_WIDTH,
                constant.MAP_HEIGHT,
            ),
        )
        for x in range(constant.MAP_LEFT, constant.MAP_RIGHT + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100),
                             (x, constant.MAP_TOP), (x, constant.MAP_BOTTOM))
        for y in range(constant.MAP_TOP, constant.MAP_BOTTOM + 1, constant.TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100),
                             (constant.MAP_LEFT, y), (constant.MAP_RIGHT, y))
            
    # def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
    #     self.draw_grid(surface)

    #     return super().draw(surface)
