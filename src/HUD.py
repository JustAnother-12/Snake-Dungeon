import pygame
from gui_element.Sprite_image import ImageElement;
from gui_element.text_class import TextElement;
from pixil import Pixil
import constant


class HUD(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON_ALT.pixil", 1).frames[0]
        self.Player_Icon_rect = ImageElement(4*constant.TILE_SIZE, 3.5*constant.TILE_SIZE, self.Player_Icon)

        self.Gold_Icon = Pixil.load("game-assets/graphics/pixil/HUD_GOLD_ICON.pixil", 2).frames[0]
        self.Gold_Icon_rect = ImageElement(4*constant.TILE_SIZE, 9*constant.TILE_SIZE, self.Gold_Icon)
        self.Gold_text = TextElement("0", "white", 15, 6*constant.TILE_SIZE, 9.5*constant.TILE_SIZE, "midleft")

        self.Length_Icon = Pixil.load("game-assets/graphics/pixil/HUD_LENGTH_ICON.pixil", 2).frames[0]
        self.Length_Icon_rect = ImageElement(4*constant.TILE_SIZE, 13*constant.TILE_SIZE, self.Length_Icon)
        self.length_text = TextElement("5", "white", 15, 6*constant.TILE_SIZE, 13.8*constant.TILE_SIZE, "midleft")

        self.add(self.Player_Icon_rect, self.Gold_Icon_rect, self.Length_Icon_rect, self.Gold_text, self.length_text)

    def set_gold(self, num):
        for grp in self.Gold_text.groups():
            grp.remove(self.Gold_text) # type: ignore
        self.Gold_text = TextElement(str(num), "white", 15, 6*constant.TILE_SIZE, 9.5*constant.TILE_SIZE, "midleft")
        for grp in self.Gold_Icon_rect.groups():
            grp.add(self.Gold_text) # type: ignore

    def set_lenght(self, len):
        for grp in self.length_text.groups():
            grp.remove(self.length_text) # type: ignore
        self.length_text = TextElement(str(len), "white", 15, 6*constant.TILE_SIZE, 13.8*constant.TILE_SIZE, "midleft")
        for grp in self.Length_Icon_rect.groups():
            grp.add(self.length_text) # type: ignore
