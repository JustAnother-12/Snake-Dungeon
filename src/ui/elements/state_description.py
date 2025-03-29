from typing import Literal
import pygame
import config.constant as constant

class StateDecription(pygame.sprite.Sprite):
    def __init__(self, 
                 text: str, 
                 text_color: pygame.typing.ColorLike, 
                 text_size: int, 
                 x_pos: int, 
                 y_pos: int, 
                 width: int,
                 height: int,
                 bg_color: pygame.typing.ColorLike,
                 padding: int,
                 radius: int,
                 radius_scale = 2,
                 choice: Literal["midleft", "center", "midright"] = "midleft",
                 border_width = 0,
                 border_color: pygame.typing.ColorLike = (0,0,0,0),
            ) -> None:
        super().__init__()
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.bg_color = bg_color
        self.radius = radius
        self.padding = padding
        self.radius_scale =radius_scale
        self.border_width = border_width
        self.border_color = border_color
        self.__render_text(choice, width, height)

    def __render_text(self, choice, width, height):
        self.font = pygame.font.Font(constant.PIXEL_FONT, self.text_size)

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
        
        # Calculate dimensions with padding
        padding = self.padding
        border_width = self.border_width
        border_color = self.border_color
        surface_width = width + padding * 2 + border_width * 2
        surface_height = height + border_width * 2

        # Create small surface to scale
        scale_factor = self.radius_scale
        small_width = surface_width // scale_factor
        small_height = surface_height // scale_factor
        small_surface = pygame.Surface((small_width, small_height), pygame.SRCALPHA).convert_alpha()
       
        # Draw small surface background with rounded edge
        background_color = self.bg_color
        corner_radius = self.radius
        pygame.draw.rect(small_surface, background_color, 
                        (0, 0, small_width, small_height), 
                        border_radius=corner_radius)
        # Draw border for the surface
        if border_width != 0:
            pygame.draw.rect(small_surface, border_color, 
                            (0, 0, small_width, small_height), 
                            border_width,
                            corner_radius)
            
        # Scale small surface up for a pixelated effect
        self.image = pygame.transform.scale(small_surface, (surface_width, surface_height))
        
        # Set rectangle position
        if choice == "midleft":
            self.rect = self.image.get_rect(midleft=(self.x_pos, self.y_pos))
        elif choice == "center":
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.image.get_rect(midright=(self.x_pos, self.y_pos))
        
        # Render text with padding
        for i, word in enumerate(words):
            text_surface = self.font.render(word, True, self.text_color)
            if choice == "midleft":
                position = (padding+4, padding + i * self.font.size(word)[1])
            elif choice == "center":
                position = (padding + (width - self.font.size(word)[0])//2, 
                        padding + i * self.font.size(word)[1])
            else:
                position = (padding-4 + width - self.font.size(word)[0], 
                        padding + i * self.font.size(word)[1])
            self.image.blit(text_surface, position)