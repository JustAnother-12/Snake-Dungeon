# tương lại
from __future__ import annotations

import pygame
from typing import Optional
from abc import ABC, abstractmethod


class GameObject(ABC):
    def __init__(self, x, y, width, height):
        from .AIBehavior import AIBehavior
        self.position = pygame.Vector2(x, y)
        self.size = (width, height)
        self.visible = True
        self.collidable = False
        self.collision_rect = pygame.Rect(x, y, width, height)
        self.ai_behavior: Optional[AIBehavior]= None
        self.interactable = False
        self.velocity = pygame.Vector2(0, 0)

    def update(self):
        if self.ai_behavior:
            self.ai_behavior.update(self)

    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass

    def on_collision(self, other: GameObject):
        pass

    def interact(self):
        pass