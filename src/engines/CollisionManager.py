from .GameObject import GameObject

class CollisionManager:
    def check_collisions(self, game_objects: list[GameObject]):
        # Lọc ra các đối tượng có thể va chạm
        collidable_objects = [obj for obj in game_objects if obj.collidable]
        
        # Kiểm tra va chạm giữa từng cặp đối tượng
        for i in range(len(collidable_objects)):
            for j in range(i + 1, len(collidable_objects)):
                obj1 = collidable_objects[i]
                obj2 = collidable_objects[j]
                if obj1.collision_rect.colliderect(obj2.collision_rect):
                    # Khi va chạm xảy ra, gọi phương thức on_collision
                    obj1.on_collision(obj2)
                    obj2.on_collision(obj1)