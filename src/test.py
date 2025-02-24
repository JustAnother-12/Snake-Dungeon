from pygame import Surface
import pygame
from engines.CollisionManager import CollisionManager
from engines.GameEngine import GameEngine
from engines.GameObject import GameObject
from engines.Scene import Scene

class Snake(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.collidable = True
        self.cells = [(x, y), (x+width, y)]
        # block / tick
        self.speed = 1
        self.tick = 0

    def render(self, surface: Surface):
        self.collision_rect = pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])
        pygame.draw.rect(surface, pygame.color.Color(255, 0, 0), self.collision_rect)
        for i in self.cells[1:]:
            rect = pygame.Rect(i[0], i[1], self.size[0], self.size[1])
            pygame.draw.rect(surface, pygame.color.Color(255, 0, 0), rect)
            self.collision_rect.union_ip(rect)
        
        return super().render(surface)
    
    def update(self):
        super().update()
        self.tick += 1
        if self.tick * self.speed >= 1:
            self.tick = 0
        self.position += self.velocity
        # self.collision_rect.move(self.velocity.x, self.velocity.y)
        self.collision_rect = pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])
    
    def on_collision(self, other: GameObject):
        if isinstance(other, Wall):
            dx = self.collision_rect.centerx - other.collision_rect.centerx
            dy = self.collision_rect.centery - other.collision_rect.centery

            min_dx = (self.size[0] + other.size[0]) // 2
            min_dy = (self.size[1] + other.size[1]) // 2
            
            if abs(dx) > abs(dy):
                self.position.x += (-1 if dx < 0 else 1) * (min_dx - abs(dx))
        
            else:
                self.position.y += (-1 if dy < 0 else 1) * (min_dy - abs(dy))

class Wall(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.collidable = True
        self.interactable = True
    
    def render(self, surface: Surface):
        pygame.draw.rect(surface, pygame.color.Color(0, 255, 0), self.collision_rect)
        return super().render(surface)

class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = Snake(50, 50 , 20, 20)
        self.walls: list[GameObject] = [
            Wall(100, 100, 50, 50),
            Wall(200, 200, 50, 50),
            Wall(300, 300, 50, 50),
            Wall(400, 400, 50, 50),
            Wall(500, 500, 50, 50),
            Wall(600, 600, 50, 50),
            Wall(700, 700, 50, 50),
            Wall(900, 900, 50, 50),
            Wall(800, 800, 50, 50),
            Wall(1000, 1000, 50, 50),
        ]
        self.game_objects = [self.player ] + self.walls


    def update(self):
        for i in self.game_objects:
            i.update()
        
        self.collision_manager.check_collisions(self.game_objects)

    
    def render(self, surface: Surface):
        surface.fill((0,0,0))
        for i in self.game_objects:
            i.render(surface)

        
    def handle_events(self, event: pygame.Event):
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_LEFT:
                self.player.velocity.x = -1
            elif event.key == pygame.K_RIGHT:
                self.player.velocity.x = 1
            elif event.key == pygame.K_UP:
                self.player.velocity.y = -1
            elif event.key == pygame.K_DOWN:
                self.player.velocity.y = 1
        
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.player.velocity.x = 0
            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                self.player.velocity.y = 0
            

game = GameEngine(1000, 1000, MenuScene())
game.run()
