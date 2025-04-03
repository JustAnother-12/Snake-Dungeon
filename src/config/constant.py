import pygame

TILE_SIZE = 16
SCREEN_WIDTH_TILES = 58
SCREEN_HEIGHT_TILES = 50
STAMINA_DECREASE = 1
STAMINA_RECOVERY = 1 
BOOST_MULTIPLIER = 2
BASE_SPEED = 16
DEATH_DELAY = 1
LEFT_RIGHT_BORDER_TILES = 9
TOP_BOTTOM_BORDER_TILES = 5
WALL_TILES = 4
COIN_VALUE = 10
MIN_LEN = 3
FLOOR_TILE_SIZE = 32

MAP_WIDTH = (
    SCREEN_WIDTH_TILES -
    LEFT_RIGHT_BORDER_TILES * 2 - WALL_TILES * 2
) * TILE_SIZE
MAP_HEIGHT = (
    SCREEN_HEIGHT_TILES -
    TOP_BOTTOM_BORDER_TILES * 2 - WALL_TILES * 2
) * TILE_SIZE
MAP_LEFT = (LEFT_RIGHT_BORDER_TILES +
            WALL_TILES) * TILE_SIZE
MAP_RIGHT = MAP_LEFT + MAP_WIDTH
MAP_TOP = (TOP_BOTTOM_BORDER_TILES +
           WALL_TILES) * TILE_SIZE
MAP_BOTTOM = MAP_TOP + MAP_HEIGHT

PIXEL_FONT = "game-assets/font/default-pixilart-text.ttf"


# TODO: Add more textures
# and use them in the game
class Texture:
    button = "game-assets/graphics/pixil/BTN_SPRITE_SHEET.pixil"
    snake_head= "game-assets/graphics/pixil/SNAKE_HEAD.pixil"
    pasue_menu_bg = "game-assets/graphics/pixil/PAUSED_MENU_BG.pixil"
    apple = "game-assets/graphics/pixil/apple.pixil"


    

