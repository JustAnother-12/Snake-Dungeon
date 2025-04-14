import pygame
from levels.components.bomb import Bomb, BombState
from levels.components.fire_tile import Fire_Tile

class FireBomb(pygame.sprite.Sprite):
    def __init__(self, level, pos=None, burn_time=4.0, fire_size=5, damage=1):
        super().__init__()
        self.level = level
        self.burn_time = burn_time  # Thời gian cháy của ngọn lửa (giây)
        self.fire_size = fire_size  # Kích thước của ngọn lửa (đơn vị ô)
        self.damage = damage
        
        # Tạo bomb thường
        self.bomb = Bomb(level, pos, BombState.ACTIVE)
        self.level.bomb_group.add(self.bomb)
        # Sử dụng các thuộc tính của bomb
        self.image = self.bomb.image
        self.rect = self.bomb.rect
        self.pos = pos
        
        # Theo dõi trạng thái
        self.fire_created = False
        
    def update(self):
        # Đồng bộ hóa hình ảnh và vị trí
        self.image = self.bomb.image
        self.rect = self.bomb.rect
        
        # Kiểm tra nếu bomb đang ở trạng thái nổ
        if self.bomb.state == BombState.EXPLOSION and not self.fire_created:
            # Tạo lửa tại chính xác vị trí bomb đang nổ
            self.create_fire()
            self.fire_created = True
            
        # Nếu bomb đã hoàn thành animation và biến mất
        if not self.bomb.alive():
            self.kill()
    
    def create_fire(self):
        """Tạo ngọn lửa ngay tại vị trí bomb nổ"""        
        # Tạo Fire_Tile tại vị trí bomb
        fire = Fire_Tile(
            self.level,
            self.pos,
            self.fire_size,
            self.fire_size,
            self.burn_time,
            self.damage
        )
        
        self.level.fire_group.add(fire)
    
    def kill(self):
        """Ghi đè phương thức kill để đảm bảo cả bomb và sprite đều bị xóa"""
        if self.bomb.alive():
            self.bomb.kill()
        super().kill()

