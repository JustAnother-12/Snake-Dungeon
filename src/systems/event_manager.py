

import pygame


class EventManager:
    __event: list[pygame.Event]
    
    @staticmethod
    def update():
        EventManager.__event = pygame.event.get()
    
    @staticmethod
    def get_events():
        return EventManager.__event;