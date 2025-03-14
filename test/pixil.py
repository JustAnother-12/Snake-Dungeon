import json, pygame, base64
from io import BytesIO

class Pixil:
    def __init__(self, frames: list[pygame.Surface], frames_delay_ms: list[int], original_size: tuple[int, int], size: tuple[int, int]) -> None:
        self.frames = frames
        self.frames_delay_ms = frames_delay_ms
        self.original_size = original_size
        self.size = size

    @classmethod
    def load(cls, path: str, scale: int):
        with open(path) as file:
            # pixil_file = PixilType.from_dict(json.loads(file.read()))
            pixil_file = json.loads(file.read())
            frames_raw = list(filter(lambda x: x['active'] == True, pixil_file['frames']))
            frames: list[pygame.Surface] = [] * len(frames_raw)
            frames_delay: list[int] = [] * len(frames_raw)
            for frame in frames_raw:
                surface = pygame.Surface((int(pixil_file['width']) * scale, int(pixil_file['height']) * scale), pygame.SRCALPHA)
                surface.set_colorkey((0, 0, 0))
                layers = []
                for layer in frame['layers']:
                    if (not layer['active']) : continue
                    buff = BytesIO(base64.b64decode(layer['src'].split(",")[1]))
                    image = pygame.image.load(buff).convert_alpha()
                    image = pygame.transform.scale(image, (int(pixil_file['width']) * scale, int(pixil_file['height']) * scale)).convert_alpha()
                    layers.append((image, (0, 0)))
                surface.blits(layers)
                surface.convert_alpha()

                frames.append(surface)
                frames_delay.append(frame['speed'])
            
            return cls(frames, frames_delay, (pixil_file['width'], pixil_file['height']), (pixil_file['width'] * scale, pixil_file['height'] * scale))
        
# if __name__ == '__main__':
#     pixil = Pixil.load('game-assets/graphics/pixil/apple.pixil', 2)
#     print(pixil.size)
#     print(pixil.original_size)  