
from typing import Any

from pygame import Event
import pygame
from config.constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
from entities.items.item_type import ActivationType, ItemCategory, Rarity
from ui.elements.button import ButtonElement
from ui.elements.image import ImageElement
from ui.screens.state import State
from ui.elements.text import TextElement
from utils.help import Share
from utils.pixil import Pixil
# from entities.items.item_entity import ItemEntity



class ItemInfoPopup(State):
    from levels import level as l
    def __init__(self, level: "l.Level", item_entity):
        super().__init__(level.game)
        self.module = True

        self.level = level
        self.item_entity = item_entity
        self.item_in_slot_index = level.snake.inventory._check_item_exits(item_entity.to_item_stack())
        if self.item_in_slot_index>=0:
            self.current_stack = level.snake.inventory.slots[self.item_in_slot_index].quantity # type:ignore
        self.item_quantity = item_entity.quantity
        self.skill_count , self.consumable_count, self.equipment_count = level.snake.inventory.count_slots()

        # popup's background display
        self.bg = Pixil.load("game-assets/graphics/pixil/ITEM_DESCRIPTION_BOX.pixil", 2).frames[0]
        self.bg_sprite = ImageElement((SCREEN_WIDTH_TILES/2)*TILE_SIZE, (SCREEN_HEIGHT_TILES/2)*TILE_SIZE, self.bg)
        self.bg_rect = self.bg.get_rect(center=((SCREEN_WIDTH_TILES/2)*TILE_SIZE, (SCREEN_HEIGHT_TILES/2)*TILE_SIZE))

        # rarity display
        match self.item_entity.item_type.rarity:
            case Rarity.COMMON:
                self.rarity = Pixil.load("game-assets/graphics/pixil/RARITY_TAGS.pixil", 3).frames[0]
            case Rarity.UNCOMMON:
                self.rarity = Pixil.load("game-assets/graphics/pixil/RARITY_TAGS.pixil", 3).frames[1]
            case Rarity.RARE:
                self.rarity = Pixil.load("game-assets/graphics/pixil/RARITY_TAGS.pixil", 3).frames[2]

        self.rarity_sprite = ImageElement((SCREEN_WIDTH_TILES/2)*TILE_SIZE, self.bg_rect.top + 3*TILE_SIZE, self.rarity)

        # item's Image display
        self.item_image = Pixil.load(item_entity.item_type.texture.pixil_path, 3).frames[item_entity.item_type.texture.stack_frame]
        self.item_sprite = ImageElement(self.bg_rect.midleft[0]+6*TILE_SIZE, self.bg_rect.midleft[1]-5*TILE_SIZE-4, self.item_image)

        # item category display
        self.category_text = TextElement(str(self.item_entity.item_type.category.name), 'white', 11, self.bg_rect.midright[0]-6*TILE_SIZE, self.bg_rect.midright[1]-8*TILE_SIZE, 'center')

        # item's name display
        self.item_name = TextElement(item_entity.item_type.name.upper(), 'white', 20, self.bg_rect.midleft[0]+12*TILE_SIZE, self.bg_rect.midleft[1]-9*TILE_SIZE, 'topleft', 400)

        # item's description display
        self.description_text = TextElement(item_entity.item_type.description.upper(), 'white', 12, self.bg_rect.midleft[0]+2*TILE_SIZE, self.bg_rect.midleft[1]+TILE_SIZE,'topleft',width=42*TILE_SIZE)
        
        self.add(self.bg_sprite, 
                 self.description_text, 
                 self.rarity_sprite, 
                 self.item_sprite, 
                 self.item_name, 
                 self.category_text, 
                 )
        
        self.take_quantity = 1
        # popup's buttons display
        if not self.item_entity.shop_item:
            self.confirm_btn = ButtonElement(self.bg_rect.bottomleft[0]+10*TILE_SIZE, self.bg_rect.bottomleft[1]-3*TILE_SIZE, "CONFIRM", "white", 14, width=160, height=50)
            self.confirm_key_text = TextElement("E",'yellow', 20, self.bg_rect.bottomleft[0]+3*TILE_SIZE, self.bg_rect.bottomleft[1]-3*TILE_SIZE)
            self.sell_btn = ButtonElement(self.bg_rect.bottomright[0]-15*TILE_SIZE, self.bg_rect.bottomright[1]-3*TILE_SIZE, "SELL FOR ", "white", 14, width=160, height=50)
            self.sell_key_text = TextElement("R",'yellow', 20, self.bg_rect.bottomright[0]-22*TILE_SIZE, self.bg_rect.bottomright[1]-3*TILE_SIZE)
            self.sell_price = int(item_entity.item_type.price*0.6)*self.take_quantity # giá bán bằng 60% so với giá gốc
            self.sell_price_text = TextElement(str(self.sell_price)+" GOLD", 'yellow', 14, self.bg_rect.bottomright[0]-9*TILE_SIZE, self.bg_rect.bottomright[1]-3*TILE_SIZE)
            
            self.add(
                    self.confirm_btn, 
                    self.sell_btn, 
                    self.sell_price_text,
                    self.sell_key_text,
                    self.confirm_key_text
                    )
        else:
            self.buy_btn = ButtonElement(self.bg_rect.centerx, self.bg_rect.centery + 13*TILE_SIZE, "BUY FOR", "white", 14, width=160, height=50)
            self.buy_key_text = TextElement("E",'yellow', 20, self.bg_rect.centerx-7*TILE_SIZE, self.bg_rect.centery + 13*TILE_SIZE)
            self.buy_price = self.take_quantity*item_entity.item_type.price
            self.price_text = TextElement(str(self.buy_price)+" GOLD", 'yellow', 14, self.bg_rect.bottomright[0]-18*TILE_SIZE, self.bg_rect.bottomright[1]-3*TILE_SIZE)
            self.add(
                    self.buy_btn,
                    self.buy_key_text,
                    self.price_text
                    )

        if self.item_quantity>1:
            self.stack_info_text = TextElement("THIS IS A STACK OF ("+str(self.item_quantity)+") ITEMS", 'grey', 10,self.bg_rect.midbottom[0], self.bg_rect.midbottom[1]-7*TILE_SIZE, 'center')
            self.add(self.stack_info_text)

            if self.item_entity.item_type.category == ItemCategory.CONSUMABLE:
                self.increbtn = ButtonElement(self.bg_rect.midright[0]-7*TILE_SIZE, self.bg_rect.midright[1]-2*TILE_SIZE, "+", "white", 14, width=30, height=25)
                self.quantity_text = TextElement(str(self.take_quantity),'white', 14, self.bg_rect.midright[0]-5*TILE_SIZE, self.bg_rect.midright[1]-2*TILE_SIZE, 'center')
                self.decrebtn = ButtonElement(self.bg_rect.midright[0]-3*TILE_SIZE, self.bg_rect.midright[1]-2*TILE_SIZE, "-", "white", 14, width=30, height=25)
                self.add(self.increbtn, self.quantity_text, self.decrebtn)

        self.inventory_manager = self.level.snake.inventory

    def print_message(self, case):
        message = None
        match case:
            case 1:
                message = TextElement("THIS ITEM'S ALREADY EXISTS IN YOUR INVENTORY!", 'yellow',20, self.bg_rect.midbottom[0], self.bg_rect.midbottom[1]+4*TILE_SIZE, 'center')
            case 2:
                message = TextElement("OVERALL STACK EXCEEDS ITEM'S MAX STACK! ("+ str(self.item_entity.item_type.max_stack) +")", 'yellow', 20,  self.bg_rect.midbottom[0], self.bg_rect.midbottom[1]+4*TILE_SIZE, 'center')
            case 3:
                message = TextElement("NO EMPTY "+ str(self.item_entity.item_type.category.name) +" SLOT AVAILABLE!", 'yellow', 20,  self.bg_rect.midbottom[0], self.bg_rect.midbottom[1]+4*TILE_SIZE, 'center')
            case 4:
                message = TextElement("YOU DON'T HAVE ENOUGH GOLD!", 'yellow', 20,  self.bg_rect.midbottom[0], self.bg_rect.midbottom[1]+4*TILE_SIZE, 'center')      
        if message is not None:
            self.add(message)

    def check_for_slots(self):
        if self.item_entity.shop_item and self.level.snake.gold < self.buy_price*self.take_quantity:
            return 4
        
        if self.item_entity.item_type.category != ItemCategory.CONSUMABLE:
            if self.inventory_manager._check_item_exits(self.item_entity.to_item_stack()) >= 0: # type:ignore
                return 1
            else:
                if self.item_entity.item_type.category == ItemCategory.SKILL and self.skill_count == 1:
                    return 3
                if self.item_entity.item_type.category == ItemCategory.EQUIPMENT and self.equipment_count == 3:
                    return 3
                return 0
        else:
            if self.inventory_manager._check_item_exits(self.item_entity.to_item_stack()) >= 0:
                if self.take_quantity + self.current_stack > self.item_entity.item_type.max_stack:
                    return 2
                else:
                    return 0
            else:
                if self.item_entity.item_type.category == ItemCategory.CONSUMABLE and self.consumable_count == 2:
                    return 3
                return 0

    def update(self, *args: Any, **kwargs: Any) -> None:
            
        return super().update(*args, **kwargs)
    
    def getItem(self):
        if self.item_entity.item_type.activation_type == ActivationType.ON_PICKUP and self.item_entity.item_type.category == ItemCategory.INSTANT:
            self.item_entity.apply_instant_effect()
            self.item_entity.kill()
            self.level.interaction_manager.unregister_interact(self.item_entity)
        else:
            self.item_entity.quantity=self.take_quantity
            self.level.snake.inventory.add_item(self.item_entity.to_item_stack())
            self.item_entity.quantity = self.item_quantity - self.take_quantity
            if self.item_entity.quantity == 0:
                self.item_entity.kill()
            self.level.interaction_manager.unregister_interact(self.item_entity)
        self.exit_state()

    def sellItem(self):
        self.level.snake.gold+=(self.sell_price*self.take_quantity)
        self.item_entity.quantity-=self.take_quantity
        if self.item_entity.quantity == 0:
            self.item_entity.kill()
        self.level.interaction_manager.unregister_interact(self.item_entity)
        self.exit_state()
    
    def get_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.item_entity.shop_item:
                if self.confirm_btn.isHovered():
                    Share.audio.play_sound("click")
                    if not self.check_for_slots(): # type:ignore
                        self.getItem()
                    else: 
                        self.print_message(self.check_for_slots())
                if self.sell_btn.isHovered():
                    Share.audio.play_sound("click")
                    Share.audio.play_sound("sell-reroll")
                    self.sellItem()
            else:
                if self.buy_btn.isHovered():
                    Share.audio.play_sound("click")
                    if not self.check_for_slots(): # type:ignore
                        Share.audio.play_sound("sell-reroll")
                        self.level.snake.gold -= (self.buy_price*self.take_quantity)
                        if self.item_entity.alive():
                            self.item_entity.groups()[0].empty()
                        self.getItem()
                    else: 
                        self.print_message(self.check_for_slots())
            if self.item_entity.item_type.category == ItemCategory.CONSUMABLE and self.item_entity.quantity > 1:
                if self.increbtn.isHovered() and self.take_quantity < self.item_entity.quantity:
                    Share.audio.play_sound("click")
                    self.take_quantity+=1
                if self.decrebtn.isHovered() and self.take_quantity > 1:
                    Share.audio.play_sound("click")
                    self.take_quantity-=1
                self.handle_quantity_change()

        elif event.type == pygame.KEYDOWN:
            key = event.key
            pygame.event.clear(eventtype=pygame.KEYDOWN)
            if not self.item_entity.shop_item:
                if key == pygame.K_e:
                    if not self.check_for_slots():
                        self.getItem()
                    else: 
                        self.print_message(self.check_for_slots())
                elif key == pygame.K_r:
                    Share.audio.play_sound("sell-reroll")
                    self.sellItem()
            else:
                 if key == pygame.K_e:
                    if not self.check_for_slots():
                        Share.audio.play_sound("sell-reroll")
                        self.level.snake.gold -= (self.buy_price*self.take_quantity)
                        if self.item_entity.alive():
                            self.item_entity.groups()[0].empty()
                        self.getItem()
                    else: 
                        self.print_message(self.check_for_slots())
            if self.item_entity.item_type.category == ItemCategory.CONSUMABLE and self.item_entity.quantity > 1:
                if key == pygame.K_KP_PLUS and self.take_quantity < self.item_entity.quantity:
                    self.take_quantity+=1
                if key == pygame.K_KP_MINUS and self.take_quantity > 1:
                    self.take_quantity-=1
                self.handle_quantity_change()
            if key == pygame.K_ESCAPE:
                self.exit_state()
        return super().get_event(event)
    
    def handle_quantity_change(self):
        self.quantity_text.set_text(str(self.take_quantity))
        if not self.item_entity.shop_item:
            self.sell_price_text.set_text(str(self.sell_price*self.take_quantity)+" GOLD")
        else: self.price_text.set_text(str(self.buy_price*self.take_quantity)+" GOLD")