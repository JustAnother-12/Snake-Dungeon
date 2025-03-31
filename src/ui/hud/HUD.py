import pygame
from entities.items.TestItem import ShieldStack
from ui.elements.image import ImageElement
from ui.elements.item_slot import ItemSlot
from ui.elements.text import TextElement
from utils.pixil import Pixil
import config.constant as constant


class HUD(pygame.sprite.Group):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level
        snake = self.level.snake
        coin,length, keys = self.level.snake.gold, len(self.level.snake), self.level.snake.keys
        from entities.Player import Snake, GreenSnake, OrangeSnake, GraySnake
        self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON_ALT.pixil", 1).frames[0]
        if isinstance(snake, OrangeSnake):
            self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON.pixil", 1).frames[0]
        elif isinstance(snake, GreenSnake):
            self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON.pixil", 1).frames[1]
        elif isinstance(snake, GraySnake):
            self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON.pixil", 1).frames[2]
        self.Player_Icon_rect = ImageElement(4*constant.TILE_SIZE, 3.5*constant.TILE_SIZE, self.Player_Icon)

        self.Gold_Icon = Pixil.load("game-assets/graphics/pixil/HUD_GOLD_ICON.pixil", 2).frames[0]
        self.Gold_Icon_rect = ImageElement(2*constant.TILE_SIZE, 9*constant.TILE_SIZE, self.Gold_Icon)
        self.Gold_text = TextElement(str(coin), "white", 15, 4*constant.TILE_SIZE, int(9.5*constant.TILE_SIZE), "midleft")

        self.Length_Icon = Pixil.load("game-assets/graphics/pixil/HUD_LENGTH_ICON.pixil", 2).frames[0]
        self.Length_Icon_rect = ImageElement(2*constant.TILE_SIZE, 13*constant.TILE_SIZE, self.Length_Icon)
        self.length_text = TextElement(str(len(snake)), "white", 15, 4*constant.TILE_SIZE, int(13.8*constant.TILE_SIZE), "midleft")

        self.Key_Icon = Pixil.load("game-assets/graphics/pixil/KEY_SPRITE.pixil", 4).frames[0]
        self.Key_Icon_rect = ImageElement(2*constant.TILE_SIZE, 18*constant.TILE_SIZE, self.Key_Icon)
        self.Key_text = TextElement(str(keys), "white", 15, 4*constant.TILE_SIZE, int(18.8*constant.TILE_SIZE), "midleft")

        i = constant.TILE_SIZE * ( constant.SCREEN_HEIGHT_TILES) + 50
        self.item_slot = [
            ItemSlot(i, 70),
            ItemSlot(i, 70 + 64),
            ItemSlot(i, 70 + 64 * 2),

        ]

        self.skill_slot = [
            ItemSlot(i, 70 + 64 * 3 + 20),
            ItemSlot(i, 70 + 64 * 4 + 20),
        ]

        self.add(self.Player_Icon_rect, self.Gold_Icon_rect, self.Length_Icon_rect, self.Gold_text, self.length_text, self.Key_Icon_rect, self.Key_text)
        self.add(*self.item_slot)
        self.add(*self.skill_slot)

    def set_gold(self, num):
        for grp in self.Gold_text.groups():
            grp.remove(self.Gold_text) # type: ignore
        self.Gold_text = TextElement(str(num), "white", 15, 4*constant.TILE_SIZE, int(9.5*constant.TILE_SIZE), "midleft")
        for grp in self.Gold_Icon_rect.groups():
            grp.add(self.Gold_text) # type: ignore

    def set_length(self, len):
        for grp in self.length_text.groups():
            grp.remove(self.length_text) # type: ignore
        self.length_text = TextElement(str(len), "white", 15, 4*constant.TILE_SIZE, int(13.8*constant.TILE_SIZE), "midleft")
        for grp in self.Length_Icon_rect.groups():
            grp.add(self.length_text) # type: ignore

    def set_key(self, keys):
        for grp in self.Key_text.groups():
            grp.remove(self.Key_text) # type: ignore
        self.Key_text = TextElement(str(keys), "white", 15, 4*constant.TILE_SIZE, int(18.8*constant.TILE_SIZE), "midleft")
        for grp in self.Key_Icon_rect.groups():
            grp.add(self.Key_text) #type: ignore

    def update(self):
        coin,length, keys = self.level.snake.gold, len(self.level.snake), self.level.snake.keys
        self.set_gold(coin)
        self.set_length(length)
        self.set_key(keys)

        # self.level.snake 
        for index, value in enumerate(self.level.snake.item_slot):
            self.item_slot[index].item_stake = value
        
        for index, value in enumerate(self.level.snake.skill_slot):
            self.skill_slot[index].item_stake = value
        super().update(self)
