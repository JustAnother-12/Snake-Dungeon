import pygame
from ui.elements.image import ImageElement
from ui.elements.item_slot import ItemSlot
from ui.elements.text import TextElement
from utils.pixil import Pixil
import config.constant as constant

class HUD(pygame.sprite.Group):
    from levels import level
    def __init__(self, level_: "level.Level") -> None:
        super().__init__()
        self.level_ = level_
        snake = self.level_.snake
        coin,length, keys = self.level_.snake.gold, len(self.level_.snake), self.level_.snake.keys
        from entities.Player import Snake
        self.Player_Icon = Pixil.load("game-assets/graphics/pixil/HUD_PLAYER_ICON_ALT.pixil", 1).frames[0]
        self.Player_Icon_rect = ImageElement(4*constant.TILE_SIZE, 3.5*constant.TILE_SIZE, self.Player_Icon)

        self.Gold_Icon = Pixil.load("game-assets/graphics/pixil/HUD_GOLD_ICON.pixil", 2).frames[0]
        self.Gold_Icon_rect = ImageElement(2*constant.TILE_SIZE, 9*constant.TILE_SIZE, self.Gold_Icon)
        self.Gold_text = TextElement(str(snake.gold), "white", 15, 4*constant.TILE_SIZE, int(9.5*constant.TILE_SIZE), "midleft")

        self.Length_Icon = Pixil.load("game-assets/graphics/pixil/HUD_LENGTH_ICON.pixil", 2).frames[0]
        self.Length_Icon_rect = ImageElement(2*constant.TILE_SIZE, 13*constant.TILE_SIZE, self.Length_Icon)
        self.length_text = TextElement(str(len(snake)), "white", 15, 4*constant.TILE_SIZE, int(13.8*constant.TILE_SIZE), "midleft")

        self.Key_Icon = Pixil.load("game-assets/graphics/pixil/KEY_SPRITE.pixil", 2).frames[0]
        self.Key_Icon_rect = ImageElement(2*constant.TILE_SIZE, 18*constant.TILE_SIZE, self.Key_Icon)
        self.Key_text = TextElement(str(keys), "white", 15, 4*constant.TILE_SIZE, int(18.8*constant.TILE_SIZE), "midleft")

        i = constant.TILE_SIZE * ( constant.SCREEN_HEIGHT_TILES) + 85
        gap = 4 # 4 pixel gap between slots
        self.item_slot_index = [
            TextElement("1",'white', 15, i-50, 128 + 64 + 20, 'midleft'),
            TextElement("2",'white', 15, i-50, 128 + 64 * 2 + 20+gap, 'midleft'),

            TextElement("3",'white', 15, i-50, 128 + 64 * 3 + 40+gap*2, 'midleft'),
            TextElement("4",'white', 15, i-50, 128 + 64 * 4 + 40+gap*3, 'midleft'),
            TextElement("5",'white', 15, i-50, 128 + 64 * 5 + 40+gap*4, 'midleft'),
        ]
        
        self.item_slot = [

            ItemSlot(i, 128 + 64 + 20),
            ItemSlot(i, 128 + 64 * 2 + 20+gap),

            ItemSlot(i, 128 + 64 * 3 + 40+gap*2),
            ItemSlot(i, 128 + 64 * 4 + 40+gap*3),
            ItemSlot(i, 128 + 64 * 5 + 40+gap*4),

            ItemSlot(i-(85-50-5), 80, scale=2),
        ]

        self.level_.snake.inventory.slots
        
        self.Key_text = TextElement(str(snake.keys), "white", 15, 4*constant.TILE_SIZE, int(18.8*constant.TILE_SIZE), "midleft")
        self.stamina_bar = pygame.sprite.Sprite()

        self.add(self.Player_Icon_rect, self.Gold_Icon_rect, self.Length_Icon_rect, self.Gold_text, self.length_text, self.Key_Icon_rect, self.Key_text)
        self.draw_stamina(snake.stamina, snake.base_stats.energy_cap)
        self.add(self.stamina_bar)
        self.add(*self.item_slot)
        self.add(*self.item_slot_index)

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
        self.stamina_bar.image = pygame.Surface((max_stamina + 4, 32))
        if stamina > 0:
            color = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 191), (0, 255, 255)]
            rate = stamina / max_stamina
            index = int(rate / 0.3)
            r = color[index][0] + (color[index + 1][0] - color[index][0]) * (stamina - index * 0.3 * max_stamina) // (min(max_stamina, (index + 1)*0.3 * max_stamina) - index * 0.3 * max_stamina)
            g = color[index][1] + (color[index + 1][1] - color[index][1]) * (stamina - index * 0.3 * max_stamina) // (min(max_stamina, (index + 1)*0.3 * max_stamina) - index * 0.3 * max_stamina)
            b = color[index][2] + (color[index + 1][2] - color[index][2]) * (stamina - index * 0.3 * max_stamina) // (min(max_stamina, (index + 1)*0.3 * max_stamina) - index * 0.3 * max_stamina)

            pygame.draw.rect(
                self.stamina_bar.image, (r, g, b), (0, 4, stamina, 24)
            )
            
            white_line = pygame.Surface((stamina, 4), pygame.SRCALPHA)
            white_line.fill((255, 255, 255, 200))
            self.stamina_bar.image.blit(white_line, (0, 4))

        pygame.draw.rect(
            self.stamina_bar.image, (133, 133, 133), (0, 0, max_stamina + 4, 32), 4, 0, 0, 10, 0, 10
        )
        self.stamina_bar.rect = self.stamina_bar.image.get_rect(topleft=(6.5*constant.TILE_SIZE, 2.5*constant.TILE_SIZE))

    def update(self):
        self.draw_stamina(self.level_.snake.stamina, self.level_.snake.base_stats.energy_cap)
        coin,length, keys = self.level_.snake.gold, len(self.level_.snake), self.level_.snake.keys
        self.set_gold(coin)
        self.set_length(length)
        self.set_key(keys)

        for index, value in enumerate(self.level_.snake.inventory.slots):
            self.item_slot[index].item_stack = value # type: ignore

        super().update(self)
