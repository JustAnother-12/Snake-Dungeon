from typing import Any, Iterable
import pygame
from pygame.sprite import AbstractGroup



class NestedGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self._sub_group__: list[AbstractGroup] = []
    
    def add(self, *sprites: Any | AbstractGroup | Iterable) -> None:
        for sprite in sprites:
            if isinstance(sprite, AbstractGroup):
                self._sub_group__.append(sprite)
            else:
                super().add(sprite)
    
    def remove(self, *sprites: Any | AbstractGroup | Iterable) -> None:
        for sprite in sprites:
            if isinstance(sprite, AbstractGroup):
                self._sub_group__.remove(sprite)
            else:
                super().remove(sprite)
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        for i in self._sub_group__:
            i.update(*args, **kwargs)

        return super().update(*args, **kwargs)
    
    def draw(self, surface: pygame.Surface) -> list[pygame.FRect | pygame.Rect]:
        for i in self._sub_group__:
            i.draw(surface)
        return super().draw(surface)
    
    def empty(self) -> None:
        self._sub_group__.clear()
        return super().empty() 

class State(NestedGroup):
    def __init__(self, game) -> None:
        super().__init__()
        from Main import Game
        self.game: Game = game
        self.state_pass: list[State] = []
        self.visible = True
        self.is_paused = False
        self.module = False

    def get_event(self, event: pygame.event.Event):
        pass

    def reset(self):
        pass

    def enter_state(self):
        if self.module:
            for state in self.game.state_stack:
                if not state.visible: continue
                self.state_pass.append(state)
                state.visible = False
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()
        for state in self.state_pass:
            state.visible = True
        self.state_pass.clear()
