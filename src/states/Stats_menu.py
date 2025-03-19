import pygame
import json
from states.state import State
from gui_element.Sprite_image import ImageElement
from gui_element.text_class import TextElement
from pixil import Pixil

class base_stats_value:
    def __init__(self) -> None:
        self.speed = 0
        self.armour = 0
        self.energy_cap = 0
        self.energy_regen = 0
        self.treasury = 0
        self.luck = 0
        self.food_potent = 0


class Stats_menu(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.Stats_text = TextElement("STATS", "white", 45, (game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - 18)*game.TILE_SIZE, "center")
        self.Background_texture = Pixil.load("game-assets/graphics/pixil/STATS_MENU_BG_BTN.pixil", 8).frames[0]
        self.Background_rect = ImageElement((game.SCREEN_WIDTH_TILES/2)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2)*game.TILE_SIZE, self.Background_texture)
        self.add(self.Background_rect, self.Stats_text)

        with open("data/stats.json", "r") as fopen:
            self.stats_data = json.load(fopen)

        self.stats_icons = Pixil.load("game-assets/graphics/pixil/STATS_ICON_SHEET.pixil", 3).frames
        self.addIcons(game)

    def addIcons(self, game):
        # add icons
        count =0
        v_gap = 8.2
        h_gap = 19
        for i in range(4):
            for j in range(2):
                icon_rect = ImageElement((game.SCREEN_WIDTH_TILES/2 - h_gap)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - v_gap)*game.TILE_SIZE, self.stats_icons[count])
                self.add(icon_rect)
                count+=1
                h_gap -= 22
            h_gap=19
            v_gap-=7.5

        # add name text
        stats_list = self.stats_data['base_stats']
        count = 0
        v_gap = 10.5
        h_gap = 16
        for i in range(4):
            for j in range(2):
                name = TextElement(stats_list[count]['name'], "white", 10, (game.SCREEN_WIDTH_TILES/2 - h_gap)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - v_gap)*game.TILE_SIZE, "midleft")
                self.add(name)
                # value = TextElement(str(stats_list[count]['value']), "yellow", 10, name.rect.right + 10 if name.rect else 0, (game.SCREEN_HEIGHT_TILES/2 - v_gap)*game.TILE_SIZE, "midleft")
                value = TextElement(str(0), "yellow", 13, (game.SCREEN_WIDTH_TILES/2 - h_gap + 14.5)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - v_gap)*game.TILE_SIZE, "midright")
                self.add(value)
                count+=1
                h_gap -= 22
            h_gap = 16
            v_gap -= 7.5

        # add decription text
        count = 0
        v_gap = 8
        h_gap = 16
        for i in range(4):
            for j in range(2):
                text = TextElement(stats_list[count]['description'].upper(), "grey", 8, (game.SCREEN_WIDTH_TILES/2 - h_gap)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - v_gap)*game.TILE_SIZE, "midleft", 200)
                self.add(text)
                count+=1
                h_gap -= 22
            h_gap = 16
            v_gap -= 7.5

    def update(self,game):
        # add name text
        stats_list = self.stats_data['base_stats']
        count = 0
        v_gap = 10.5
        h_gap = 16
        for i in range(4):
            for j in range(2):
                # value = TextElement(str(stats_list[count]['value']), "yellow", 10, name.rect.right + 10 if name.rect else 0, (game.SCREEN_HEIGHT_TILES/2 - v_gap)*game.TILE_SIZE, "midleft")
                value = TextElement(str(0), "yellow", 13, (game.SCREEN_WIDTH_TILES/2 - h_gap + 14.5)*game.TILE_SIZE, (game.SCREEN_HEIGHT_TILES/2 - v_gap)*game.TILE_SIZE, "midright")
                self.add(value)
                count+=1
                h_gap -= 22
            h_gap = 16
            v_gap -= 7.5

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_state()
                     