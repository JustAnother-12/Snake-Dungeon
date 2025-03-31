from __future__ import annotations
from math import floor
import pygame
from Stats import Stats
from level_components.Trap import Traps
from level_components.Chest import Chests
from level_components.Coin import Coins
from level_components.Key import Keys
from level_components.Pot import Pot_group
from level_components.Wall import Walls
from level_components.Bomb import Bomb_group
from level_components.Obstacle import Obstacle_group
from level_components.floor_tile import Floor, Floor_Tile
from states import RoomCleared
from states.GameOver_menu import GameOver_menu
from states.state import State
from states.Pause_menu import Pause_menu
from states.RoomCleared import RoomCleared
from gui_element.text_class import TextElement
import constant
from HUD import HUD
from region_generator import RegionGenerator
from level_components.Food import Food_Group
from time import time

class LevelTest(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.init()

    def init(self):
        from Player import Snake, GreenSnake, OrangeSnake, GraySnake
        self.remove(self.sprites())
        self.snake = GreenSnake(self, 5)

        self.foods = Food_Group(self)

        self.region_generator = RegionGenerator()
        self.traps = Traps(self,self.region_generator.traps_initpos)
        self.chests = Chests(self, self.region_generator.chests_initpos)
        self.pots = Pot_group(self, self.region_generator.pots_initpos)
        self.obstacles = Obstacle_group(self, self.region_generator.obstacles_initpos)

        self.keys = Keys(self, 2)
        self.coins = Coins(self)
        self.bombs = Bomb_group(self, 5) 
        self.walls = Walls()
        
        self.currentRoom = 1
        self.hud = HUD(self.snake)
        self.roomText = TextElement("ROOM "+str(self.currentRoom),"white", 15, (int(constant.SCREEN_WIDTH_TILES/2))*constant.TILE_SIZE, constant.TILE_SIZE, 'center')

        self.is_paused = False
        self.is_finished = False
        self.timer = time()
        self.floor = Floor()
        self.add(self.floor, self.hud, self.walls, self.traps, self.obstacles,
                 self.foods, self.chests, self.pots, self.coins, self.bombs, self.keys, self.snake)
        
    def reset_room(self):
        self.snake.auto_state, self.snake.manual_state = True, False
        self.timer = time()
        self.is_finished = False
        self.remove(self.foods, self.traps, self.chests, self.pots, self.obstacles, self.keys, self.coins, self.bombs, self.walls, self.snake, self.roomText)
        self.foods = Food_Group(self)

        self.region_generator = RegionGenerator()
        self.traps = Traps(self,self.region_generator.traps_initpos)
        self.chests = Chests(self, self.region_generator.chests_initpos)
        self.pots = Pot_group(self, self.region_generator.pots_initpos)
        self.obstacles = Obstacle_group(self, self.region_generator.obstacles_initpos)

        self.keys = Keys(self, 2)
        self.coins = Coins(self)
        self.bombs = Bomb_group(self, 5) 
        self.walls = Walls()

        self.currentRoom +=1
        self.roomText = TextElement("ROOM "+str(self.currentRoom),"white", 15, (int(constant.SCREEN_WIDTH_TILES/2))*constant.TILE_SIZE, constant.TILE_SIZE, 'center')
        self.add(self.roomText,self.foods, self.traps, self.chests, self.pots, self.obstacles, self.keys, self.coins, self.bombs, self.walls, self.snake)

    def reset(self):
        self.init()

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_r]:
            self.game.state_stack.append(RoomCleared(self.game))
            self.is_finished = True
            
        if self.is_finished:
            self.snake.auto_state, self.snake.manual_state = False, True
            # self.reset_room()
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(Pause_menu(self.game))

        if self.is_paused or self.snake.isDeath:
            return
        self.snake.update()
        self.traps.update()
        self.keys.update()
        self.chests.update()
        self.pots.update()
        self.bombs.update()
        self.coins.update()
        self.foods.update()
        self.hud.update(self.snake)
        
        Stats.setValue("LENGTH", len(self.snake.blocks))

        if self.snake.isDeath:
            self.game.state_stack[-1].visible = False
            self.game.state_stack.append(GameOver_menu(self.game))        

    def drawRoomCleared(self):
        pass

def main():
    pass

if __name__ == "__main__":
    main()
