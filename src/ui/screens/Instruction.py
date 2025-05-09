import pygame
from ui.screens.count_down import Count_down
from ui.screens.state import State
from config.constant import SCREEN_HEIGHT_TILES, SCREEN_WIDTH_TILES, TILE_SIZE
from ui.elements.text import TextElement

class Instruction(State):
    def __init__(self, game, level) -> None:
        super().__init__(game)
        self.module = True

        self.level = level
        self.bg_sprite = pygame.sprite.Sprite()
        self.bg_sprite.image = pygame.Surface((SCREEN_WIDTH_TILES*TILE_SIZE, SCREEN_HEIGHT_TILES*TILE_SIZE))
        self.bg_sprite.rect = self.bg_sprite.image.get_rect(topleft=(0,0))

        self.header_text = TextElement("HOW TO PLAY", 'yellow', 30, (SCREEN_WIDTH_TILES//2)*TILE_SIZE, (SCREEN_HEIGHT_TILES//2-20)*TILE_SIZE, 'center')
        
        self.instruction_text1 = TextElement("- W,A,S,D OR ARROW KEYS TO CHANGE DIRECTION",
                                            'white', 
                                            16, 
                                            (SCREEN_WIDTH_TILES//2-24)*TILE_SIZE, 
                                            (SCREEN_HEIGHT_TILES//2-16)*TILE_SIZE, 
                                            'midleft',
                                            )
        self.instruction_text2 = TextElement("- ESC TO PAUSE THE GAME",
                                            'white', 
                                            16, 
                                            (SCREEN_WIDTH_TILES//2-24)*TILE_SIZE, 
                                            (SCREEN_HEIGHT_TILES//2-12)*TILE_SIZE, 
                                            'midleft',
                                            )
        self.instruction_text3 = TextElement("- HOLD SPACE TO GAIN SPEED BOOST",
                                            'white', 
                                            16, 
                                            (SCREEN_WIDTH_TILES//2-24)*TILE_SIZE, 
                                            (SCREEN_HEIGHT_TILES//2-8)*TILE_SIZE, 
                                            'midleft',
                                            )
        self.instruction_text4 = TextElement("- CTRL TO USE SKILL. NUMB1 and NUMB2 TO USE CONSUMABLES",
                                            'white', 
                                            16, 
                                            (SCREEN_WIDTH_TILES//2-24)*TILE_SIZE, 
                                            (SCREEN_HEIGHT_TILES//2-4)*TILE_SIZE, 
                                            'midleft',
                                            )
        self.instruction_text5 = TextElement("- HOLD THE ITEM's SLOT KEY TO DROP",
                                            'white', 
                                            16, 
                                            (SCREEN_WIDTH_TILES//2-24)*TILE_SIZE, 
                                            (SCREEN_HEIGHT_TILES//2)*TILE_SIZE, 
                                            'midleft',
                                            )
        self.instruction_text6 = TextElement("- SPEED BOOST AND SKILL COSTS ENERGY",
                                            'white', 
                                            16, 
                                            (SCREEN_WIDTH_TILES//2-24)*TILE_SIZE, 
                                            (SCREEN_HEIGHT_TILES//2+4)*TILE_SIZE, 
                                            'midleft',
                                            )
        self.instruction_text7 = TextElement("- DEFEAT THE ENEMIES TO PROGRESS THE GAME",
                                            'white', 
                                            16, 
                                            (SCREEN_WIDTH_TILES//2-24)*TILE_SIZE, 
                                            (SCREEN_HEIGHT_TILES//2+8)*TILE_SIZE, 
                                            'midleft',
                                            )
        self.instruction_text8 = TextElement("- REACH THE END OF THE DUNGEON AS FAST AS POSSIBLE!",
                                            'white', 
                                            16, 
                                            (SCREEN_WIDTH_TILES//2-24)*TILE_SIZE, 
                                            (SCREEN_HEIGHT_TILES//2+12)*TILE_SIZE, 
                                            'midleft',
                                            )
        self.escape_instruction = TextElement("PRESS SPACE TO CONTINUE", 'cyan', 16, (SCREEN_WIDTH_TILES//2)*TILE_SIZE, (SCREEN_HEIGHT_TILES//2+18)*TILE_SIZE, 'center')

        self.add(self.bg_sprite, 
                 self.header_text, 
                 self.instruction_text1,
                 self.instruction_text2,
                 self.instruction_text3,
                 self.instruction_text4,
                 self.instruction_text5,
                 self.instruction_text6,
                 self.instruction_text7, 
                 self.instruction_text8,
                 self.escape_instruction
                 )

        

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            self.exit_state()
        return super().update()
