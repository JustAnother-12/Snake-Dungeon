import pygame


class State(pygame.sprite.Group):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.prev_state = None
        self.visible = True

    def get_event(self, event: pygame.event.Event):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()