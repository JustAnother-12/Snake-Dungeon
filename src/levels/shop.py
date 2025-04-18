
from typing import List
import pygame
from entities.items.item_registry import ItemRegistry
from ui.elements.text import TextElement
from entities.NPC_entity import NPC
from config import constant
from loot import LootPool
from utils.help import Share


class Shop_level:
    def __init__(self, level) -> None:
        self.level = level
        self.npc = NPC(self.level, (constant.SCREEN_WIDTH_TILES//2 *
                       constant.TILE_SIZE, constant.SCREEN_HEIGHT_TILES//2*constant.TILE_SIZE))

        self.InstantPool = LootPool((0, 0, 0, 100, 0, 0, 0))
        self.ConsumablePool = LootPool((0, 0, 0, 0, 100, 0, 0))
        self.EquipmentAndSkillPool = LootPool((0, 0, 0, 0, 0, 60, 40))

        self.instantItems: List[pygame.sprite.Group] = []
        self.consumableItems: List[pygame.sprite.Group] = []
        self.equipAndSkillItems: List[pygame.sprite.Group] = []

        self.item_positions = [
            # Instant items
            [(constant.MAP_LEFT + (4+(i*3))*constant.TILE_SIZE,
              (constant.SCREEN_HEIGHT_TILES//2 + 4)*constant.TILE_SIZE) for i in range(2)],
            # Consumable items
            [(constant.MAP_RIGHT - (9-(i*3))*constant.TILE_SIZE,
              (constant.SCREEN_HEIGHT_TILES//2 + 4)*constant.TILE_SIZE) for i in range(2)],
            # Equipment/skill items
            [((constant.SCREEN_WIDTH_TILES//2 - 7)*constant.TILE_SIZE + (3+(i*3))*constant.TILE_SIZE,
              (constant.SCREEN_HEIGHT_TILES//2 + 4)*constant.TILE_SIZE) for i in range(3)]
        ]

    def init_Stock(self):
        '''
        Tạo 3 loại item trong shop
        - 2 item instant
        - 2 item consumable
        - 3 item equipment/skill
        '''
        # Tạo 2 item instant

        instantItems = []
        consumableItems = []
        equipAndSkillItems = []

        while len(instantItems) < 2:
            instantItem = self.InstantPool.get_item()
            if instantItem in instantItems:
                continue

            instantItems.append(instantItem)
            item_shop = pygame.sprite.Group()
            item = ItemRegistry.create_item(
                instantItem[0], instantItem[1], self.level, pos=self.item_positions[0][len(self.instantItems)])
            item.shop_item = True
            item_shop.add(item)
            price_text = TextElement(str((int)(item.item_type.price*(item.item_type.sale/100))),
                                     'yellow', 10, self.item_positions[0][len(self.instantItems)][0] + constant.TILE_SIZE, self.item_positions[0][len(self.instantItems)][1] + 3*constant.TILE_SIZE, 'center')
            item_shop.add(price_text)
            self.instantItems.append(item_shop)

        # tạo 2 item consumable
        while len(consumableItems) < 2:
            consumableItem = self.ConsumablePool.get_item()
            if consumableItem in consumableItems:
                continue

            consumableItems.append(consumableItem)
            item_shop = pygame.sprite.Group()
            item = ItemRegistry.create_item(
                consumableItem[0], consumableItem[1], self.level, pos=self.item_positions[1][len(self.consumableItems)])
            item.shop_item = True
            item_shop.add(item)
            price_text = TextElement(str((int)(item.item_type.price*(item.item_type.sale/100))),
                                     'yellow', 10, self.item_positions[1][len(self.consumableItems)][0] + constant.TILE_SIZE, self.item_positions[1][len(self.consumableItems)][1] + 3*constant.TILE_SIZE, 'center')
            item_shop.add(price_text)
            self.consumableItems.append(item_shop)

        # Tạo 3 item equipment/skill
        while len(equipAndSkillItems) < 3:
            EquipAndSkillItem = self.EquipmentAndSkillPool.get_item()
            if EquipAndSkillItem in equipAndSkillItems:
                continue
            equipAndSkillItems.append(EquipAndSkillItem)
            item_shop = pygame.sprite.Group()
            item = ItemRegistry.create_item(
                EquipAndSkillItem[0], EquipAndSkillItem[1], self.level, pos=self.item_positions[2][len(self.equipAndSkillItems)])
            item.shop_item = True
            item_shop.add(item)
            price_text = TextElement(str((int)(item.item_type.price*(item.item_type.sale/100))),
                                     'yellow', 10, self.item_positions[2][len(self.equipAndSkillItems)][0] + constant.TILE_SIZE, self.item_positions[2][len(self.equipAndSkillItems)][1] + 3*constant.TILE_SIZE, 'center')
            item_shop.add(price_text)
            self.equipAndSkillItems.append(item_shop)

        print(instantItems)
        print(consumableItems)
        print(equipAndSkillItems)

    def reStock(self):
        '''
        remove equip and skill item -> reset new item euipment/skill -> display all item again
        '''
        self.level.remove(*self.equipAndSkillItems)
        self.equipAndSkillItems.clear()

        equipAndSkillItems = []
        while len(self.equipAndSkillItems) < 3:
            EquipAndSkillItem = self.EquipmentAndSkillPool.get_item()
            if EquipAndSkillItem in equipAndSkillItems:
                continue
            equipAndSkillItems.append(EquipAndSkillItem)
            item_shop = pygame.sprite.Group()
            item = ItemRegistry.create_item(
                EquipAndSkillItem[0], EquipAndSkillItem[1], self.level, pos=self.item_positions[2][len(self.equipAndSkillItems)])
            item.shop_item = True
            item_shop.add(item)
            price_text = TextElement(str((int)(item.item_type.price*(item.item_type.sale/100))),
                                     'yellow', 10, self.item_positions[2][len(self.equipAndSkillItems)][0] + constant.TILE_SIZE, self.item_positions[2][len(self.equipAndSkillItems)][1] + 3*constant.TILE_SIZE, 'center')
            item_shop.add(price_text)
            self.equipAndSkillItems.append(item_shop)

        self.level.add(*self.equipAndSkillItems)

    def remove_Stock(self):
        self.level.remove(self.npc)
        self.level.remove(*self.instantItems)
        self.level.remove(*self.consumableItems)
        self.level.remove(*self.equipAndSkillItems)
        self.instantItems.clear()
        self.consumableItems.clear()
        self.equipAndSkillItems.clear()

    def display_Stock(self):
        Share.audio.play_music('shop', -1, 5000)
        self.level.add(self.npc)
        self.level.add(*self.instantItems)
        self.level.add(*self.consumableItems)
        self.level.add(*self.equipAndSkillItems)
