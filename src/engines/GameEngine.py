
from __future__ import annotations
import pygame
import typing

from .Scene import Scene


class GameEngine:
    __instance: GameEngine
    def __init__(self, width: int, height:int, menu: Scene) -> None:
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.current_scene: Scene = menu
        self.running = False
        self.scene_overlay = None
        self.__instance = self
    
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.current_scene.handle_events(event)
            self.current_scene.update()
            self.current_scene.render(self.screen)
            pygame.display.flip()
            
            self.clock.tick(60)
        
        pygame.quit()

    
    def swithc_scene(self, scene: Scene):
        self.current_scene = scene

    def set_overlay(self, scene: Scene):
        self.scene_overlay = scene
   
    @classmethod
    def get_instance(cls):
        return cls.__instance