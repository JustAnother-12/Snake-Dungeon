import pygame

def check_collision(sprite: pygame.sprite.Sprite, list_sprite) -> bool:
    '''
    Return true if sprite collision with any sprite in list

    '''
    all_snake_parts = pygame.sprite.Group()
    for block_group in list_sprite:
        all_snake_parts.add(block_group)

    collision = pygame.sprite.spritecollideany(sprite, all_snake_parts)
    return collision is not None