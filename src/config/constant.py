TILE_SIZE = 16
SCREEN_WIDTH_TILES = 58
SCREEN_HEIGHT_TILES = 50
STAMINA_DECREASE = 1
STAMINA_RECOVERY = 0.5 
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
    bomb = 'game-assets/graphics/pixil/item-sprite/BOMB_ITEM.pixil'
    ouroboros = "game-assets/graphics/pixil/item-sprite/THE_OUROBOROS.pixil"
    earth_essence = "game-assets/graphics/pixil/item-sprite/EARTH_ESSENCE.pixil"
    gale_essence = "game-assets/graphics/pixil/item-sprite/GALE_ESSENCE.pixil"
    gluttony_essence = "game-assets/graphics/pixil/item-sprite/GLUTTONY_ESSENCE.pixil"
    gold_essence = "game-assets/graphics/pixil/item-sprite/GOLD_ESSENCE.pixil"
    lightning_essence = "game-assets/graphics/pixil/item-sprite/LIGHTNING_ESSENCE.pixil"
    luck_essence = "game-assets/graphics/pixil/item-sprite/LUCK_ESSENCE.pixil"
    water_essence = "game-assets/graphics/pixil/item-sprite/WATER_ESSENCE.pixil"
    dungeon_essence = "game-assets/graphics/pixil/item-sprite/DUNGEON_ESSENCE.pixil"
    green_jade = "game-assets/graphics/pixil/item-sprite/GREEN_JADE_PELLET.pixil"
    time_efficiency = "game-assets/graphics/pixil/item-sprite/TIME_EFFICIENCY.pixil"
    credit_card = "game-assets/graphics/pixil/item-sprite/CREDIT_CARD.pixil"
    aerolite_plate = "game-assets/graphics/pixil/item-sprite/AEROLITE_PLATE.pixil"
    adrenaline_syringe = "game-assets/graphics/pixil/item-sprite/ADRENALINE_SYRINGE.pixil"
    appetite_stimulant = "game-assets/graphics/pixil/item-sprite/APPETITE_STIMULANT.pixil"
    celestine_fragment = "game-assets/graphics/pixil/item-sprite/CELESTINE_FRAGMENT.pixil"
    energy_drink = "game-assets/graphics/pixil/item-sprite/ENERGY_DRINK.pixil"
    energized_crystal = "game-assets/graphics/pixil/item-sprite/ENERGIZED_CRYSTAL.pixil"
    fire_bomb = "game-assets/graphics/pixil/item-sprite/FIRE_BOMB.pixil"
    ghost_like_body = "game-assets/graphics/pixil/item-sprite/GHOST_LIKE_BODY.pixil"
    molotov = "game-assets/graphics/pixil/item-sprite/MOLOTOV.pixil"
    resistance_potion = "game-assets/graphics/pixil/item-sprite/RESISTANCE_POTION.pixil"
    ritual_dagger = "game-assets/graphics/pixil/item-sprite/RITUAL_DAGGER.pixil"
    speed_potion = "game-assets/graphics/pixil/item-sprite/SPEED_POTION.pixil"
    reverse = "game-assets/graphics/pixil/item-sprite/REVERSE.pixil"