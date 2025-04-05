import random
from config.constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE, COIN_VALUE
import config.constant as constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity
import utils.pixil as pixil
import pygame



COIN_TYPE = ItemType(
    'coin', 
    'Coin', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        "game-assets/graphics/pixil/GOLD_LEVEL.pixil",
    ),
    "",
    1,
    activation_type=ActivationType.ON_COLLISION,
)

class CoinEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, COIN_TYPE, area, r, quantity)
    
    def apply_instant_effect(self):
        self.level.snake.gold += self.item_type.value * self.quantity
    