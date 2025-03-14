import pygame

TILE_SIZE = 25
SCREEN_WIDTH_TILES = 25
SCREEN_HEIGHT_TILES = 25
STAMINA_DECREASE_RATE = 0.1
STAMINA_RECOVERY_RATE = 0.1 
STAMINA_DECREASE_RATE_WHILE_RUNNING = 0.2
BOOST_MULTIPLIER = 2
HEAD_IMG = pygame.transform.scale(pygame.image.load("game-assets/graphics/png/snake_head.png"), (TILE_SIZE, TILE_SIZE))
DEATH_DELAY = 2

# TODO: Add more textures
# and use them in the game
class Texture:
    button = "game-assets/graphics/pixil/PAUSE_MENU_BTN_BG_SHEET.pixil"
    snake_head= "game-assets/graphics/png/snake_head.png"

