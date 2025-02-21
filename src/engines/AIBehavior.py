

from abc import ABC, abstractmethod
from .GameObject import GameObject
import pygame

class AIBehavior(ABC):
    @abstractmethod
    def update(self, game_object: GameObject):
        pass

class ChaseBehavior(AIBehavior):
    def __init__(self, target, speed):
        self.target = target  # Đối tượng mục tiêu (ví dụ: người chơi)
        self.speed = speed

    def update(self, game_object: GameObject):
        direction = self.target.position - game_object.position
        direction.normalize_ip()
        game_object.position += direction * self.speed
    
class PatrolBehavior(AIBehavior):
    def __init__(self, points: list[pygame.Vector2], speed: int):
        self.points = points  # Danh sách các điểm tuần tra
        self.speed = speed
        self.current_point = 0

    def update(self, game_object: GameObject):
        target_point = self.points[self.current_point]
        direction = target_point - game_object.position
        if direction.length() < self.speed:
            self.current_point = (self.current_point + 1) % len(self.points)
        else:
            direction.normalize_ip()
            game_object.position += direction * self.speed