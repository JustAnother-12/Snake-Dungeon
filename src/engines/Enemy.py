

from engines.Sprite import Sprite

class Enemy(Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        self.speed = 2

    def update(self):
        pass
        # # Ví dụ: di chuyển ngẫu nhiên
        # self.position.x += self.speed
        # if self.position.x > 600 or self.position.x < 0:
        #     self.speed = -self.speed
        # super().update()