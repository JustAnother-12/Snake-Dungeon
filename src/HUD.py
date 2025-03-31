import pygame
from Player import GraySnake, GreenSnake, OrangeSnake, Snake
from gui_element.Sprite_image import ImageElement;
from gui_element.text_class import TextElement;
from pixil import Pixil
import constant


class HUD(pygame.sprite.Group):
    from Player import Snake, GreenSnake, OrangeSnake, GraySnake
    def __init__(self, snake) -> None:
        super().__init__()
        if isinstance(snake, OrangeSnake):
            self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON.pixil", 1).frames[0]
        elif isinstance(snake, GreenSnake):
            self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON.pixil", 1).frames[1]
        elif isinstance(snake, GraySnake):
            self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON.pixil", 1).frames[2]
        self.Player_Icon_rect = ImageElement(4*constant.TILE_SIZE, 3.5*constant.TILE_SIZE, self.Player_Icon)

        self.Gold_Icon = Pixil.load("game-assets/graphics/pixil/HUD_GOLD_ICON.pixil", 2).frames[0]
        self.Gold_Icon_rect = ImageElement(2*constant.TILE_SIZE, 9*constant.TILE_SIZE, self.Gold_Icon)
        self.Gold_text = TextElement(str(snake.coins), "white", 15, 4*constant.TILE_SIZE, int(9.5*constant.TILE_SIZE), "midleft")

        self.Length_Icon = Pixil.load("game-assets/graphics/pixil/HUD_LENGTH_ICON.pixil", 2).frames[0]
        self.Length_Icon_rect = ImageElement(2*constant.TILE_SIZE, 13*constant.TILE_SIZE, self.Length_Icon)
        self.length_text = TextElement(str(len(snake)), "white", 15, 4*constant.TILE_SIZE, int(13.8*constant.TILE_SIZE), "midleft")

        self.Key_Icon = Pixil.load("game-assets/graphics/pixil/KEY_SPRITE.pixil", 4).frames[0]
        self.Key_Icon_rect = ImageElement(2*constant.TILE_SIZE, 18*constant.TILE_SIZE, self.Key_Icon)
        self.Key_text = TextElement(str(snake.keys), "white", 15, 4*constant.TILE_SIZE, int(18.8*constant.TILE_SIZE), "midleft")

        self.stamina_bar = pygame.sprite.Sprite()
        self.draw_stamina(snake.stamina, snake.max_stamina)
        self.add(self.stamina_bar, self.Player_Icon_rect, self.Gold_Icon_rect, self.Length_Icon_rect, self.Gold_text, self.length_text, self.Key_Icon_rect, self.Key_text)

    def set_gold(self, num):
        for grp in self.Gold_text.groups():
            grp.remove(self.Gold_text) # type: ignore
        self.Gold_text = TextElement(str(num), "white", 15, 4*constant.TILE_SIZE, int(9.5*constant.TILE_SIZE), "midleft")
        for grp in self.Gold_Icon_rect.groups():
            grp.add(self.Gold_text) # type: ignore

    def set_length(self, len):
        for grp in self.length_text.groups():
            grp.remove(self.length_text) # type: ignore
        self.length_text = TextElement(str(len), "white", 15, 4*constant.TILE_SIZE, int(13.8*constant.TILE_SIZE), "midleft")
        for grp in self.Length_Icon_rect.groups():
            grp.add(self.length_text) # type: ignore

    def set_key(self, keys):
        for grp in self.Key_text.groups():
            grp.remove(self.Key_text) # type: ignore
        self.Key_text = TextElement(str(keys), "white", 15, 4*constant.TILE_SIZE, int(18.8*constant.TILE_SIZE), "midleft")
        for grp in self.Key_Icon_rect.groups():
            grp.add(self.Key_text) #type: ignore

    def draw_stamina(self, stamina, max_stamina):
        self.stamina_bar.image = pygame.Surface((132, 32))
        if stamina > 0:
            color = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 191), (0, 255, 255)]
            rate = stamina / max_stamina
            index = int(rate / 0.3)
            r = color[index][0] + (color[index + 1][0] - color[index][0]) * (stamina - index * 0.3 * max_stamina) // (min(max_stamina, (index + 1)*0.3 * max_stamina) - index * 0.3 * max_stamina)
            g = color[index][1] + (color[index + 1][1] - color[index][1]) * (stamina - index * 0.3 * max_stamina) // (min(max_stamina, (index + 1)*0.3 * max_stamina) - index * 0.3 * max_stamina)
            b = color[index][2] + (color[index + 1][2] - color[index][2]) * (stamina - index * 0.3 * max_stamina) // (min(max_stamina, (index + 1)*0.3 * max_stamina) - index * 0.3 * max_stamina)

            pygame.draw.rect(
                self.stamina_bar.image, (r, g, b), (0, 4, stamina * 128 // max_stamina, 24)
            )
            
            white_line = pygame.Surface((stamina * 128 // max_stamina, 4), pygame.SRCALPHA)
            white_line.fill((255, 255, 255, 200))
            self.stamina_bar.image.blit(white_line, (0, 4))

        pygame.draw.rect(
            self.stamina_bar.image, (133, 133, 133), (0, 0, 132, 32), 4, 0, 0, 10, 0, 10
        )
        self.stamina_bar.rect = self.stamina_bar.image.get_rect(topleft=(6.5*constant.TILE_SIZE, 2.5*constant.TILE_SIZE))

    def update(self, snake):
        self.set_gold(snake.coins)
        self.set_length(len(snake))
        self.set_key(snake.keys)
        self.draw_stamina(snake.stamina, snake.max_stamina)
