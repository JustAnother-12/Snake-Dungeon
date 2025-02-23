
import pygame
from .GameObject import GameObject
from .CollisionManager import CollisionManager

class Scene:
    def __init__(self):
        self.game_objects: list[GameObject] = []
        self.collision_manager: CollisionManager = CollisionManager()
    
    def update(self):
        pass

    def handle_events(self, event: pygame.Event):
        pass

    def render(self, surface: pygame.Surface):
        pass