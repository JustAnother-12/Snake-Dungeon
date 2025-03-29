
import random
import config.constant as constant
import utils.pixil as pixil

grid = [[0 for _ in range(constant.FLOOR_TILE_SIZE)] for _ in range(constant.FLOOR_TILE_SIZE)]
# Hàm kiểm tra xem khu vực có trống không
def is_area_free(x, y, size):
    for i in range(size):
        for j in range(size):
            if x + i >= constant.FLOOR_TILE_SIZE or y + j >= constant.FLOOR_TILE_SIZE or grid[x + i][y + j] == 1:
                return False
    return True

# Hàm đánh dấu ô đã chiếm
def mark_area(x, y, size):
    for i in range(size):
        for j in range(size):
            grid[x + i][y + j] = 1

regions = [pixil.get_coords_from_pixil("game-assets/region/trap_squareborder.pixil", (180,180,180)), 
           pixil.get_coords_from_pixil("game-assets/region/trap_frame_L_border.pixil", (180,180,180)), 
           pixil.get_coords_from_pixil("game-assets/region/trap_4dots.pixil", (180,180,180))
           ]
traps_pos = []
pots_pos = []
obstacles_pos = []

if __name__ == '__main__':
    placed = set()
    for x,y in random.choices(regions)[0]:
        if (x,y) not in placed and is_area_free(x,y,2):
            traps_pos.append((x*constant.TILE_SIZE+64,y*constant.TILE_SIZE+64))
            mark_area(x,y,2)
            placed.add((x,y))

    print(traps_pos)
    

