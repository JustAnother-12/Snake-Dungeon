

import pygame


class InteractionManager:
    def __init__(self, level):
        self.level = level
        self.interactable_items = []
        self.interaction_key = pygame.K_e
        
        