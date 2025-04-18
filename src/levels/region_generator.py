import random
import utils.pixil as pixil
import config.constant as constant

trap_possible_regions = [pixil.get_coords_from_pixil("game-assets/region/trap_squareborder.pixil", (180,180,180)),
                        pixil.get_coords_from_pixil("game-assets/region/trap_squareborder_var2.pixil", (180,180,180)),
                        pixil.get_coords_from_pixil("game-assets/region/trap_center_square_var2.pixil", (180,180,180)),
                        pixil.get_coords_from_pixil("game-assets/region/trap_center_square.pixil", (180,180,180)),
                        pixil.get_coords_from_pixil("game-assets/region/trap_center_circleborder.pixil", (180,180,180)),
                        pixil.get_coords_from_pixil("game-assets/region/trap_center_circleborder_var2.pixil", (180,180,180)),
                        pixil.get_coords_from_pixil("game-assets/region/trap_center_circle.pixil", (180,180,180)),
                        pixil.get_coords_from_pixil("game-assets/region/frame_L_border.pixil", None), 
                        pixil.get_coords_from_pixil("game-assets/region/frame_L_border_var2.pixil", None),
                        pixil.get_coords_from_pixil("game-assets/region/4dots.pixil", None),
                        pixil.get_coords_from_pixil("game-assets/region/4dots_var2.pixil", None),
                        pixil.get_coords_from_pixil("game-assets/region/4Ls.pixil", None),
                        pixil.get_coords_from_pixil("game-assets/region/4Ls_var2.pixil", None),
                        pixil.get_coords_from_pixil("game-assets/region/4lines.pixil", None)
                        ]

pot_possible_regions = [pixil.get_coords_from_pixil("game-assets/region/pots_4corner.pixil", (156,90,60)),
                       pixil.get_coords_from_pixil("game-assets/region/pots_random_var2.pixil", (156,90,60)),
                       pixil.get_coords_from_pixil("game-assets/region/pots_random_var3.pixil", (156,90,60)),
                       pixil.get_coords_from_pixil("game-assets/region/pots_random.pixil", (156,90,60)),
                       pixil.get_coords_from_pixil("game-assets/region/THIEN_EASTEREGG.pixil", (156,90,60)),
                       pixil.get_coords_from_pixil("game-assets/region/TUAN_EASTEREGG.pixil", (156,90,60)),
                       pixil.get_coords_from_pixil("game-assets/region/HIEU_EASTEREGG.pixil", (156,90,60)),
                       ]

obstacle_possible_regions = [pixil.get_coords_from_pixil("game-assets/region/frame_L_border.pixil", None),
                            pixil.get_coords_from_pixil("game-assets/region/frame_L_border_var2.pixil", None),
                            pixil.get_coords_from_pixil("game-assets/region/4dots.pixil", None),
                            pixil.get_coords_from_pixil("game-assets/region/4dots_var2.pixil", None),
                            pixil.get_coords_from_pixil("game-assets/region/4Ls.pixil", None),
                            pixil.get_coords_from_pixil("game-assets/region/4Ls_var2.pixil", None),
                            pixil.get_coords_from_pixil("game-assets/region/4lines.pixil", None)
                            ]

chest_possible_regions = [pixil.get_coords_from_pixil("game-assets/region/chest_nearwall.pixil", None),
                          pixil.get_coords_from_pixil("game-assets/region/chest_nearwall_var2.pixil", None),
                          ]

class RegionGenerator:
    def __init__(self, has_trap = None, has_obstacle = None, has_chest = None, has_pot = None) -> None:
        self.grid = [[0 for _ in range(constant.FLOOR_TILE_SIZE)] for _ in range(constant.FLOOR_TILE_SIZE)]

        self.has_trap = has_trap if has_trap != None else random.choice([True,False])
        self.has_obstacle = has_obstacle if has_obstacle != None else random.choice([True,False])
        self.has_chest = has_chest if has_chest != None else random.choice([True,False])
        self.has_pot = has_pot if has_pot != None else random.choice([True,False])

        self.pots_initpos = []
        self.obstacles_initpos = []
        self.traps_initpos = []
        self.chests_initpos = []

        if self.has_trap:
            self.get_trap_region()
        if self.has_obstacle:
            self.get_obstacle_region()
        if self.has_pot:
            self.get_pot_region()
        if self.has_chest:
            self.get_chest_region()
        

    def region_overlaped(self,x,y):
        if (x,y) in self.grid:
            return True
        return False

    # Hàm kiểm tra xem khu vực có trống không
    def is_area_free(self, x, y, size):
        for i in range(size):
            for j in range(size):
                if x + i >= constant.FLOOR_TILE_SIZE or y + j >= constant.FLOOR_TILE_SIZE or self.grid[x + i][y + j] == 1:
                    return False
        return True

    # Hàm đánh dấu ô đã chiếm
    def mark_area(self, x, y, size):
        for i in range(size):
            for j in range(size):
                self.grid[x + i][y + j] = 1

    def get_trap_region(self):
        random.shuffle(trap_possible_regions)
        for region in trap_possible_regions:
            region_placed = False
            for x,y in region:
                if self.is_area_free(x,y,2):
                    self.traps_initpos.append(((x + constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES)*constant.TILE_SIZE, (y + constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES)*constant.TILE_SIZE))
                    self.mark_area(x,y,2)
                    region_placed = True
            if region_placed:
                break
            

    def get_pot_region(self):
        for x,y in random.choices(pot_possible_regions)[0]:
            if self.is_area_free(x,y,1):
                self.pots_initpos.append(((x + constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES)*constant.TILE_SIZE, (y + constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES)*constant.TILE_SIZE))
                self.mark_area(x,y,1)

    def get_obstacle_region(self):
        random.shuffle(obstacle_possible_regions)
        for region in obstacle_possible_regions:
            region_placed = False
            for x,y in region:
                if self.is_area_free(x,y,2):
                    self.obstacles_initpos.append(((x + constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES)*constant.TILE_SIZE, (y + constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES)*constant.TILE_SIZE))
                    self.mark_area(x,y,2)
                    region_placed = True
            if region_placed:
                break

    def get_chest_region(self):
        for x,y in random.choices(chest_possible_regions)[0]:
            if self.is_area_free(x,y,2):
                self.chests_initpos.append(((x + constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES)*constant.TILE_SIZE, (y + constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES)*constant.TILE_SIZE))
                self.mark_area(x,y,2)