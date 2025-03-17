
import pygame


class TextElement(pygame.sprite.Sprite):
    def __init__(self, text, color, size, x_pos, y_pos, choice = "midright", width = -1) -> None:
        super().__init__()
        self.text = text
        self.color = color
        self.size = size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.__render_text(choice, width)
    
    def __render_text(self, choice, width):
        self.font = pygame.font.Font("game-assets/font/default-pixilart-text.ttf", self.size)
        if width == -1:
            width = self.font.size(self.text)[0]
        words = []
        tw = []

        if self.text.count(" ") == 0:
            words.append(self.text)
        else: 
            for word in self.text.split(" "):
                if self.font.size(" ".join(tw + [word]))[0] > width:
                    words.append(" ".join(tw))
                    tw = []
        
                tw.append(word)
        if tw:
            words.append(" ".join(tw))
        
        self.image = pygame.Surface((width, len(words) * self.font.get_height())).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        if choice == "midleft":
            self.rect = self.image.get_rect(midleft=(self.x_pos, self.y_pos))
        elif choice == "center":
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.image.get_rect(midright=(self.x_pos, self.y_pos))
        
        # print(self.text, words)

        for i, word in enumerate(words):
            if choice == "midleft":
                img = self.font.render(word, True, self.color), (0, i * self.font.size(word)[1])
            elif choice == "center":
                img = self.font.render(word, True, self.color), (width//2 - self.font.size(word)[0]//2, i * self.font.size(word)[1])
            else:
                img = self.font.render(word, True, self.color), (width - self.font.size(word)[0], i * self.font.size(word)[1])
            # print(self.font.size(word))
            self.image.blit(*img)