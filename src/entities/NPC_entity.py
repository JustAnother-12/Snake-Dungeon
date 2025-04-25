from systems.interaction_manager import InteractionObject
from utils.help import Share
from utils.pixil import Pixil


class NPC(InteractionObject):
    def __init__(self, level, pos):
        self.reStockPrice = 20
        super().__init__(level, f'restock Equipments and Skills ({self.reStockPrice} Gold)', 45)
        self.pos = pos
        self.frame_index = 0
        self.frame_duration = 1
        self.time_animation = 0
        self.frames = Pixil.load(
            "game-assets/graphics/pixil/OWL_NPC_SPRITE.pixil", 2).frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def update(self):

        dt = Share.clock.get_time()/1000
        self.time_animation += dt

        if self.time_animation >= self.frame_duration:
            self.time_animation = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        if self.__is_collision_with_snake():
            self.image.set_alpha(100)  # type: ignore
        else:
            self.image.set_alpha(255)  # type: ignore

        super().update()

    def __is_collision_with_snake(self):
        return self.rect and not self.level.snake.is_dead and self.rect.colliderect(self.level.snake.blocks[0].rect)

    def on_interact(self):
        if self.level.snake.gold >= self.reStockPrice:
            Share.audio.play_sound("sell-reroll")
            self.level.shop.reStock()
            self.level.snake.gold-=self.reStockPrice
            self.reStockPrice+=20
            self.text = f'restock ({self.reStockPrice} Gold)'
        else:
            Share.audio.play_sound("error")
