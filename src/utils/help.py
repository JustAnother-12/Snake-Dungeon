import pygame

def check_collision(sprite: pygame.sprite.Sprite, list_sprite):
    '''
    Return true if sprite collision with any sprite in list

    '''
    for block_group in list_sprite:
        if sprite.rect and sprite.rect.colliderect(block_group.rect):
            return True

class Share:
    clock = pygame.time.Clock()