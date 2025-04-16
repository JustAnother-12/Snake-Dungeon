from numpy import concat
import pygame
from entities.items.item_registry import ItemRegistry
from entities.items.item_type import ItemCategory
from ui.elements.text import TextElement
from utils.pixil import Pixil
from entities.NPC_entity import NPC
from config import constant
from loot import LootPool

class Shop_level:
    def __init__(self, level) -> None:
        self.level = level
        self.npc = NPC(self.level, (constant.SCREEN_WIDTH_TILES//2*constant.TILE_SIZE, constant.SCREEN_HEIGHT_TILES//2*constant.TILE_SIZE))

        self.InstantPool = LootPool((0,0,0,100,0,0,0))
        self.ConsumablePool = LootPool((0,0,0,0,100,0,0))
        self.EquipmentAndSkillPool = LootPool((0,0,0,0,0,60,40))

        self.instantItems = []
        self.consumableItems = []
        self.equipAndSkillItems = []
        # self.init_Stock()
        # self.display_Stock()

        self.reStockPrice = 20
        # self.reStockBtn = pygame.sprite.Sprite()
        # self.reStockBtn.image = Pixil.load("gane-assets/graphics/pixil/item-sprite/REVERSE.pixil").frames[0]
        # self.reStockBtn.rect = self.reStockBtn.image.get_rect(topleft = ((constant.SCREEN_WIDTH_TILES//2)*constant.TILE_SIZE, (constant.SCREEN_HEIGHT_TILES//2+4)*constant.TILE_SIZE))

    def init_Stock(self):
        # Tạo 2 item instant
        while True:
            if len(self.instantItems) == 2:
                break
            instantItem = self.InstantPool.get_item()
            if instantItem not in self.instantItems:
                self.instantItems.append(instantItem)

        # tạo 2 item consumable
        while True:
            if len(self.consumableItems) == 2:
                break
            consumableItem = self.ConsumablePool.get_item()
            if consumableItem not in self.consumableItems:
                self.consumableItems.append(consumableItem)

        # Tạo 3 item equipment/skill
        while True:
            if len(self.equipAndSkillItems) == 3:
                break
            EquipAndSkillItem = self.EquipmentAndSkillPool.get_item()
            if EquipAndSkillItem not in self.equipAndSkillItems:
                self.equipAndSkillItems.append(EquipAndSkillItem)

        print(self.instantItems)
        print(self.consumableItems)
        print(self.equipAndSkillItems)

    def reStock(self):
        print("shop_restock")
        # chỉ restock Equipment và Skill
        self.reStockPrice += 10
        self.equipAndSkillItems = []
        while True:
            if len(self.equipAndSkillItems) == 3:
                break
            EquipAndSkillItem = self.EquipmentAndSkillPool.get_item()
            if EquipAndSkillItem not in self.equipAndSkillItems:
                self.equipAndSkillItems.append(EquipAndSkillItem)

        # xóa item cũ
        for item in self.level.item_group:
            category = item.item_type.category
            if(category == ItemCategory.EQUIPMENT or category == ItemCategory.SKILL):
                item.kill()
                for text in self.level:
                    if isinstance(text, TextElement) and text.text == str(item.item_type.price):
                        text.kill()

        # cho item equipment/skill vào trong level
        for index, equipandskill in enumerate(self.equipAndSkillItems):
            ItemRegistry.create_item(
                                    equipandskill[0],
                                    equipandskill[1], 
                                    self.level, 
                                    pos=((constant.SCREEN_WIDTH_TILES//2 - 7)*constant.TILE_SIZE + (3+(index*3))*constant.TILE_SIZE, (constant.SCREEN_HEIGHT_TILES//2 + 4)*constant.TILE_SIZE)
                                    )   

        for item in self.level.item_group:
            item.shop_item = True 

    def display_Stock(self):
        self.level.add(self.npc)

        # cho item instant vào trong level
        for index, instant in enumerate(self.instantItems):
            ItemRegistry.create_item(
                                    instant[0],
                                    instant[1], 
                                    self.level, 
                                    pos=(constant.MAP_LEFT + (4+(index*3))*constant.TILE_SIZE, (constant.SCREEN_HEIGHT_TILES//2 + 4)*constant.TILE_SIZE)
                                    )
            
        # cho item consumable vào trong level 
        for index, consumable in enumerate(self.consumableItems):
            ItemRegistry.create_item(
                                    consumable[0],
                                    consumable[1], 
                                    self.level, 
                                    pos=(constant.MAP_RIGHT - (9-(index*3))*constant.TILE_SIZE, (constant.SCREEN_HEIGHT_TILES//2 + 4)*constant.TILE_SIZE)
                                    )    
            
        # cho item equipment/skill vào trong level
        for index, equipandskill in enumerate(self.equipAndSkillItems):
            ItemRegistry.create_item(
                                    equipandskill[0],
                                    equipandskill[1], 
                                    self.level, 
                                    pos=((constant.SCREEN_WIDTH_TILES//2 - 7)*constant.TILE_SIZE + (3+(index*3))*constant.TILE_SIZE, (constant.SCREEN_HEIGHT_TILES//2 + 4)*constant.TILE_SIZE)
                                    )    
            
        for item in self.level.item_group:
            item.shop_item = True

