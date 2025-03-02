import pygame
import sys
import random
import time

from pygame.math import Vector2

class FOOD:
    def __init__(self):
        self.random_pos()
        
    def draw_food(self):
        food_rect = pygame.Rect(self.pos.x * tile_size, self.pos.y * tile_size, tile_size, tile_size)
        # pygame.draw.rect(screen, (126, 166, 114) , food_rect)
        screen.blit(apple, food_rect)

    def random_pos (self):
        self.x = random.randint(0,tile_number-1)
        self.y = random.randint(0,tile_number-1)
        self.pos = Vector2(self.x,self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10), Vector2(2,10)]
        self.direction = 'RIGHT'
        self.add_block = False

        
        self.head_up = pygame.image.load('game-assets/graphics/png/snake_head.png').convert_alpha()
        self.head_right = pygame.transform.rotate(self.head_up, -90)
        self.head_down = pygame.transform.rotate(self.head_up, -180)
        self.head_left = pygame.transform.rotate(self.head_up, 90)

        self.tail_up = pygame.image.load('game-assets/graphics/png/snake_tail.png').convert_alpha()
        self.tail_right = pygame.transform.rotate(self.tail_up, -90)
        self.tail_down = pygame.transform.rotate(self.tail_up, -180)
        self.tail_left = pygame.transform.rotate(self.tail_up, 90)

        self.body_up = pygame.image.load('game-assets/graphics/png/snake_body.png').convert_alpha()
        self.body_side = pygame.transform.rotate(self.body_up, -90)

        self.corner_up_right = pygame.image.load('game-assets/graphics/png/snake_corner_up_right.png').convert_alpha()
        self.corner_right_down = pygame.transform.rotate(self.corner_up_right, -90)
        self.corner_down_left = pygame.transform.rotate(self.corner_up_right, -180)
        self.corner_left_up = pygame.transform.rotate(self.corner_up_right, 90)

    def draw_snake(self):
        for index,block in enumerate(self.body):
            snake_rect = pygame.Rect(block.x*tile_size, block.y*tile_size, tile_size, tile_size)
            self.update_graphics(snake_rect, 'HEAD')
            self.update_graphics(snake_rect, 'TAIL')

            if index == 0:
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rect)
            else:
                prev_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                if prev_block.x == next_block.x:
                    screen.blit(self.body_up, snake_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_side, snake_rect)
                else: 
                    if(prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1):
                        screen.blit(self.corner_up_right, snake_rect)
                    if(prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1):
                        screen.blit(self.corner_right_down, snake_rect)
                    if(prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1):
                        screen.blit(self.corner_down_left, snake_rect)
                    if(prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1):
                        screen.blit(self.corner_left_up, snake_rect)


    def update_graphics(self, snake_rect, part):
        if(part == 'HEAD'):
            head_relation = self.body[0] - self.body[1]
            if(head_relation == Vector2(1,0)): self.head = self.head_right #head is to the right
            elif(head_relation == Vector2(-1,0)): self.head = self.head_left #head is to the left
            elif(head_relation == Vector2(0,1)): self.head = self.head_down #head is below
            elif(head_relation == Vector2(0,-1)): self.head = self.head_up #head is above
        if(part == 'TAIL'):
            tail_relation = self.body[-2] - self.body[-1]
            if(tail_relation == Vector2(1,0)): self.tail = self.tail_right #tail is to the right
            elif(tail_relation == Vector2(-1,0)): self.tail = self.tail_left #tail is to the left
            elif(tail_relation == Vector2(0,1)): self.tail= self.tail_down #tail is below
            elif(tail_relation == Vector2(0,-1)): self.tail = self.tail_up #tail is above
        


    def move_snake(self):
        next_direction = Vector2(1,0) #Right
        if self.direction == 'RIGHT':
            next_direction = Vector2(1,0)
        if self.direction == 'LEFT':
            next_direction = Vector2(-1,0)
        if self.direction == 'UP':
            next_direction = Vector2(0,-1)
        if self.direction == 'DOWN':
            next_direction = Vector2(0,1)
        
        if(self.add_block == True):
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + next_direction)
            self.body = body_copy[:]
            self.add_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + next_direction)
            self.body = body_copy[:]

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()
        self.blip_SFX = pygame.mixer.Sound('game-assets/audio/blipSelect.wav')
        self.dead_SFX = pygame.mixer.Sound('game-assets/audio/hitHurt.wav')

    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw_element(self):
        self.draw_background()
        self.food.draw_food()
        self.snake.draw_snake()

    def check_collision(self):
        if(self.food.pos == self.snake.body[0]):
            self.play_SFX('EAT')
            self.food.random_pos()
            self.snake.add_block = True

            for block in self.snake.body:
                if(block == self.food.pos):
                    self.food.random_pos()

        if(not 0 <= self.snake.body[0].x < tile_number or not 0 <= self.snake.body[0].y < tile_number):
            self.game_over()

        for block in self.snake.body[1:]:
            if(self.snake.body[0] == block):
                self.game_over()

    def play_SFX(self, type):
        if type == 'EAT':
            self.blip_SFX.play()
        elif type == 'DEAD':
            self.blip_SFX.play()

    def game_over(self):
        self.play_SFX('DEAD')
        
        time.sleep(1)
        pygame.quit()
        sys.exit()

    def draw_background(self):
        bg_color = (52,57,77)
        for row in range (tile_number):
            if(row%2 == 0):
                for col in range(tile_number):
                    if(col%2==0):
                        bg_rect = pygame.Rect(col*tile_size,row*tile_size,tile_size,tile_size)
                        pygame.draw.rect(screen,bg_color,bg_rect)
            else:
                for col in range(tile_number):
                    if(col%2!=0):
                        bg_rect = pygame.Rect(col*tile_size,row*tile_size,tile_size,tile_size)
                        pygame.draw.rect(screen,bg_color,bg_rect)


pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

# set screen width-height
tile_number = 20
tile_size = 32

screen = pygame.display.set_mode((tile_size*tile_number,tile_size*tile_number))

# create clock obj
clock = pygame.time.Clock()
apple = pygame.image.load('game-assets/graphics/png/apple.png').convert_alpha()


main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150) 

# game loop
while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and (main.snake.direction != 'DOWN'):
                main.snake.direction = 'UP' # moving up
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (main.snake.direction != 'UP'):
                main.snake.direction = 'DOWN' # moving down
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (main.snake.direction != 'RIGHT'):
                main.snake.direction = 'LEFT' # moving left
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (main.snake.direction != 'LEFT'):
                main.snake.direction = 'RIGHT' # moving right

    screen.fill((47,51,69))
    main.draw_element()
    pygame.display.update()
    clock.tick(60) # game max fps