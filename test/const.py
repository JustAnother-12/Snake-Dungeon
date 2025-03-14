import pygame

TILE_SIZE = 16
WINDOW_SIZE = 640
BOOST_MULTIPLIER = 2
STAMINA_RECOVERY_RATE = 0.2
STAMINA_DECREASE_RATE = 1
DEATH_DELAY = 2
HEAD_IMG = pygame.transform.scale(pygame.image.load("game-assets/graphics/png/snake_head.png"), (TILE_SIZE, TILE_SIZE))
APPLE_IMG = pygame.image.load("game-assets/graphics/png/apple.png")

def check_collision(food, snake_blocks: list[pygame.sprite.GroupSingle]) -> bool:
    all_snake_parts = pygame.sprite.Group()
    for block_group in snake_blocks:
        all_snake_parts.add(block_group.sprite)

    collision = pygame.sprite.spritecollideany(food, all_snake_parts)
    return collision is not None