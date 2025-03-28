
from typing import Literal
from constant import FLOOR_TILE_SIZE

def Generate_rectangle_region(width, height, top_left_x , top_left_y):
    coords = []

    for x in range(top_left_x, top_left_x+width):
        for y in range(top_left_y, top_left_y+height):
            coords.append((x,y))
        
    return coords

# def Generate_circle_region():
#     coords = []
#     outer_radius = random.randint(4,8)
#     circle_width = 2
#     inner_radius = outer_radius - circle_width
#     center_x, center_y = FLOOR_TILE_SIZE//2, FLOOR_TILE_SIZE//2

#     for x in range(FLOOR_TILE_SIZE):
#         for y in range(FLOOR_TILE_SIZE):
#             distance = math.sqrt((x-center_x)**2 + (y-center_y)**2) # distance between random pos and the center of the circle
#             if inner_radius <= distance <= outer_radius:
#                 coords.append((x,y))
#     return coords

# def Generate_solid_circle_region():
#     coords = []
#     radius = random.randint(4,8)
#     center_x, center_y = FLOOR_TILE_SIZE//2, FLOOR_TILE_SIZE//2

#     for x in range(FLOOR_TILE_SIZE):
#         for y in range(FLOOR_TILE_SIZE):
#             if math.sqrt((x-center_x)**2 + (y-center_y)**2) <= radius:
#                 coords.append((x,y))
#     return coords

def generate_L_shaped_region(width, height, corner_x, corner_y, corner_pos: Literal["topleft", "topright", "bottomleft", "bottomright"]):
    coords = []
    leg1_length = width  # Chân ngang
    leg2_length = height  # Chân dọc

    match corner_pos:
        case "topleft":
            for x in range(corner_x, corner_x + leg1_length):
                if x < FLOOR_TILE_SIZE and x >= 0:
                    coords.append((x, corner_y))
            for y in range(corner_y, corner_y + leg2_length):
                if y < FLOOR_TILE_SIZE and y>=0:
                    coords.append((corner_x, y))
        case "topright":    
            for x in range(corner_x - leg1_length, corner_x):
                if x < FLOOR_TILE_SIZE and x>=0:
                    coords.append((x, corner_y))
            for y in range(corner_y, corner_y + leg2_length):
                if y < FLOOR_TILE_SIZE and y>=0:
                    coords.append((corner_x, y))
        case "bottomleft":
            for x in range(corner_x, corner_x + leg1_length):
                if x < FLOOR_TILE_SIZE and x>=0:
                    coords.append((x, corner_y))
            for y in range(corner_y - leg2_length, corner_y):
                if y < FLOOR_TILE_SIZE and y>=0:
                    coords.append((corner_x, y))
        case "bottomright":
            for x in range(corner_x - leg1_length, corner_x):
                if x < FLOOR_TILE_SIZE and x>=0:
                    coords.append((x, corner_y))
            for y in range(corner_y - leg2_length, corner_y):
                if y < FLOOR_TILE_SIZE and y >=0:
                    coords.append((corner_x, y))
    
    return list(set(coords))

def generate_frame_L_region(width, leg_length):
    coords = []

    side_length = width
    # Tâm của level
    center_x, center_y = FLOOR_TILE_SIZE // 2, FLOOR_TILE_SIZE // 2

    # Tính tọa độ 4 góc của hình vuông (đảm bảo hình vuông nằm giữa level)
    half_side = side_length // 2
    top_left = (center_x - half_side, center_y - half_side)  # Góc trên trái
    top_right = (center_x + half_side, center_y - half_side)  # Góc trên phải
    bottom_left = (center_x - half_side, center_y + half_side)  # Góc dưới trái
    bottom_right = (center_x + half_side, center_y + half_side)  # Góc dưới phải

    # Chữ L trên-trái (góc vuông hướng xuống-phải)
    for x in range(top_left[0], top_left[0] + leg_length):  # Chân ngang
        if 0 <= x < FLOOR_TILE_SIZE:
            coords.append((x, top_left[1]))
    for y in range(top_left[1], top_left[1] + leg_length):  # Chân dọc
        if 0 <= y < FLOOR_TILE_SIZE:
            coords.append((top_left[0], y))

    # Chữ L trên-phải (góc vuông hướng xuống-trái)
    for x in range(top_right[0] - leg_length + 1, top_right[0] + 1):  # Chân ngang
        if 0 <= x < FLOOR_TILE_SIZE:
            coords.append((x, top_right[1]))
    for y in range(top_right[1], top_right[1] + leg_length):  # Chân dọc
        if 0 <= y < FLOOR_TILE_SIZE:
            coords.append((top_right[0], y))

    # Chữ L dưới-trái (góc vuông hướng lên-phải)
    for x in range(bottom_left[0], bottom_left[0] + leg_length):  # Chân ngang
        if 0 <= x < FLOOR_TILE_SIZE:
            coords.append((x, bottom_left[1]))
    for y in range(bottom_left[1] - leg_length + 1, bottom_left[1] + 1):  # Chân dọc
        if 0 <= y < FLOOR_TILE_SIZE:
            coords.append((bottom_left[0], y))

    # Chữ L dưới-phải (góc vuông hướng lên-trái)
    for x in range(bottom_right[0] - leg_length + 1, bottom_right[0] + 1):  # Chân ngang
        if 0 <= x < FLOOR_TILE_SIZE:
            coords.append((x, bottom_right[1]))
    for y in range(bottom_right[1] - leg_length + 1, bottom_right[1] + 1):  # Chân dọc
        if 0 <= y < FLOOR_TILE_SIZE:
            coords.append((bottom_right[0], y))

    return coords

def generate_square_border_region(top_left_x, top_left_y, width, thickness):
    coords = []
    side_length = width

    # Tọa độ 4 cạnh của viền hình vuông
    top_left = (top_left_x+4, top_left_y+4)
    bottom_right = (top_left[0] + side_length, top_left[1] + side_length)

    # Cạnh trên
    for x in range(top_left[0], bottom_right[0]):
        for y in range(top_left[1], top_left[1] + thickness):
            coords.append((x, y))
    # Cạnh dưới
    for x in range(top_left[0], bottom_right[0]):
        for y in range(bottom_right[1] - thickness, bottom_right[1]):
            coords.append((x, y))
    # Cạnh trái
    for x in range(top_left[0], top_left[0] + thickness):
        for y in range(top_left[1], bottom_right[1]):
            coords.append((x, y))
    # Cạnh phải
    for x in range(bottom_right[0] - thickness, bottom_right[0]):
        for y in range(top_left[1], bottom_right[1]):
            coords.append((x, y))

    return list(set(coords))  # Loại bỏ tọa độ trùng lặp ở các góc




    
