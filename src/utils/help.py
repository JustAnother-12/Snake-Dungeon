import pygame

from systems.audio_manager import AudioManager

class Share:
    clock = pygame.time.Clock()
    audio = AudioManager()
    
def to_dark_color(color, darken_factor=10):
    """
    Darkens a color by subtracting a value from each RGB component.
    Ensures that the resulting color components are within the range [0, 255].
    """
    r = color[0]
    g = color[1]
    b = color[2] 
    return tuple(max(0, min(255, c - darken_factor)) for c in (r, g, b))