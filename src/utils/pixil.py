import json, pygame, base64
from io import BytesIO
from PIL import Image
import numpy

class Pixil:
    def __init__(self, frames: list[pygame.Surface], frames_delay_ms: list[int], original_size: tuple[int, int], size: tuple[int, int], padding: int = 0) -> None:
        self.frames = frames
        self.frames_delay_ms = frames_delay_ms
        self.original_size = original_size
        self.size = size
        self.padding = padding

    @classmethod
    def load(cls, path: str, scale: int = 1, padding: int = 0):
        with open(path) as file:
            # pixil_file = PixilType.from_dict(json.loads(file.read()))
            pixil_file = json.loads(file.read())
            frames_raw = list(filter(lambda x: x['active'] == True, pixil_file['frames']))
            frames: list[pygame.Surface] = [] * len(frames_raw)
            frames_delay: list[int] = [] * len(frames_raw)
            for frame in frames_raw:
                surface = pygame.Surface((int(pixil_file['width']) * scale + padding*2, int(pixil_file['height']) * scale + padding*2), pygame.SRCALPHA)
                surface.set_colorkey((0, 0, 0))
                layers = []
                for layer in frame['layers']:
                    if (not layer['active']) : continue
                    buff = BytesIO(base64.b64decode(layer['src'].split(",")[1]))
                    image = pygame.image.load(buff).convert_alpha()
                    image = pygame.transform.scale(image, (int(pixil_file['width']) * scale, int(pixil_file['height']) * scale)).convert_alpha()
                    image.set_alpha(int(float(layer['opacity'])*255))
                    layers.append((image, (padding, padding)))
                surface.blits(layers)
                surface.convert_alpha()

                frames.append(surface)
                frames_delay.append(frame['speed'])
            
            return cls(frames, frames_delay, (pixil_file['width'], pixil_file['height']), (pixil_file['width'] * scale, pixil_file['height'] * scale), padding)


def get_coords_from_pixil(path, target_color):
    with open(path, 'r') as file:
        pixil_data = json.load(file)
    image_data = base64.b64decode(pixil_data['frames'][0]['layers'][0]['src'].split(',')[1])
    image = Image.open(BytesIO(image_data))
    if image.size != (32,32):
        raise ValueError("Loaded image size has to be 32x32 pixel!")
    image = image.convert("RGB")

    image_array = numpy.array(image)

    coords = []
    for x in range(32):
        for y in range(32):
            pixel_color = tuple(int(val) for val in image_array[y, x])
            if target_color != None:
                if pixel_color == target_color:
                    coords.append((x,y))
            else:
                if pixel_color != (0,0,0):
                    coords.append((x,y))
    return coords

    
# if __name__ == '__main__':
#     # pixil = Pixil.load('game-assets/graphics/pixil/apple.pixil', 2)
#     # print(pixil.size)
#     # print(pixil.original_size)
#     coords = get_coords_from_pixil("C:/Users/user/Downloads/test.pixil", (255, 194, 14))
#     print(coords)  