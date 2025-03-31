from typing import Any
from config import constant
import pygame
from time import time

from ui.elements.state_description import StateDecription
from ui.screens.state import State


class RoomCleared(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.RoomCleared_text = StateDecription("ROOM CLEARED!", 
                                                  "white", 
                                                  45, 
                                                  (int(constant.SCREEN_WIDTH_TILES/2))*constant.TILE_SIZE, 
                                                  (int(constant.SCREEN_HEIGHT_TILES/2))*constant.TILE_SIZE, 
                                                  constant.SCREEN_WIDTH_TILES*constant.TILE_SIZE, 
                                                  9*constant.TILE_SIZE, 
                                                  (47,53,84), 
                                                  constant.TILE_SIZE,
                                                  0, 
                                                  choice='center'
                                                  )
        self.timer = time()
        self.add(self.RoomCleared_text)

    def update(self) -> None:
        if time() - self.timer > 1:
            self.game.state_stack.pop()
        return super().update()