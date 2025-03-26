import pygame

TILE_SIZE = 16
SCREEN_WIDTH_TILES = 58
SCREEN_HEIGHT_TILES = 50
STAMINA_DECREASE_RATE = 0.1
STAMINA_RECOVERY_RATE = 0.1 
STAMINA_DECREASE_RATE_WHILE_RUNNING = 0.2
BOOST_MULTIPLIER = 2
HEAD_IMG = pygame.transform.scale(pygame.image.load("game-assets/graphics/png/snake_head.png"), (TILE_SIZE, TILE_SIZE))
DEATH_DELAY = 1
LEFT_RIGHT_BORDER_TILES = 9
TOP_BOTTOM_BORDER_TILES = 5
WALL_TILES = 4
COIN_VALUE = 10
MIN_LEN = 3
FLOOR_TILE_SIZE = 32

PIXEL_FONT = "game-assets/font/default-pixilart-text.ttf"


# TODO: Add more textures
# and use them in the game
class Texture:
    button = "game-assets/graphics/pixil/PAUSE_MENU_BTN_BG_SHEET.pixil"
    snake_head= "game-assets/graphics/png/snake_head.png"
    pasue_menu_bg = "game-assets/graphics/pixil/PAUSED_MENU_BG.pixil"
    apple = "game-assets/graphics/pixil/apple.pixil"


    

