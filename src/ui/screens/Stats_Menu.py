import pygame
from stats import Stats
from ui.elements.image import ImageElement
from ui.elements.state_description import StateDecription
from ui.elements.text import TextElement
from ui.screens.state import State
from utils.pixil import Pixil

class base_stats_value:
    def __init__(self) -> None:
        self.speed = 0.0
        self.resistance = 0.0
        self.energy_cap = 0.0
        self.energy_regen = 0.0
        self.food_potency = 0

class Stats_menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.Stats_text = TextElement("STATS", "white", 45, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 18)*game.TILE_SIZE, "center")
        self.Background_texture = Pixil.load("game-assets/graphics/pixil/STATS_MENU_BG_BTN.pixil", 8).frames[0]
        self.Background_rect = ImageElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE, self.Background_texture)
        self.add(self.Background_rect, self.Stats_text)
        self.stats_icons = Pixil.load("game-assets/graphics/pixil/STATS_ICON_SHEET.pixil", 3).frames
        self.addIcons()

    def addIcons(self):
        # add icons
        count =0
        v_gap = 8.2
        h_gap = 19
        for i in range(4):
            for j in range(2):
                icon_rect = ImageElement((self.game.SCREEN_WIDTH_TILES/2 - h_gap)*self.game.TILE_SIZE, 
                                         (self.game.SCREEN_HEIGHT_TILES/2 - v_gap)*self.game.TILE_SIZE, 
                                         self.stats_icons[count]
                                         )
                self.add(icon_rect)
                count+=1
                h_gap -= 22
            h_gap=19
            v_gap-=7.5

        # add name text
        count = 0
        v_gap = 10.5
        h_gap = 16
        for key, value in Stats.stats.items():
            name = TextElement(key.value, 
                               "white", 
                               10, 
                               (self.game.SCREEN_WIDTH_TILES/2 - h_gap)*self.game.TILE_SIZE, 
                               (self.game.SCREEN_HEIGHT_TILES/2 - v_gap)*self.game.TILE_SIZE, 
                               "midleft"
                               )
            self.add(name)
            value = TextElement(str(Stats.getValue(key)), 
                                "yellow", 
                                13, 
                                (self.game.SCREEN_WIDTH_TILES/2 - h_gap + 14.5)*self.game.TILE_SIZE, 
                                (self.game.SCREEN_HEIGHT_TILES/2 - v_gap)*self.game.TILE_SIZE, 
                                "midright"
                                )
            self.add(value)
            h_gap -= 22
            if count % 2 != 0:
                h_gap = 16
                v_gap -= 7.5
            count += 1

        # add decription text
        count = 0
        v_gap = 8
        h_gap = 16
        for key, value in Stats.stats.items():
            text = StateDecription(value["description"].upper(), 
                               "grey", 
                               8, 
                               (self.game.SCREEN_WIDTH_TILES/2 - h_gap)*self.game.TILE_SIZE, 
                               (self.game.SCREEN_HEIGHT_TILES/2 - v_gap)*self.game.TILE_SIZE + 8, 
                               200,
                               56,
                               (57,62,77),
                               5,
                               4,
                               2,
                               "midleft",
                               1,
                               (108,115,135)
                               )
            self.add(text)
            h_gap -= 22
            if count % 2 != 0:
                h_gap = 16
                v_gap -= 7.5
            count += 1

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_state()
                     