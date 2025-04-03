

import pygame

from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ItemCategory


class InteractionManager:
    def __init__(self, level):
        self.level = level
        self.__interactable_objs = []
        self.interaction_key = pygame.K_e
        self.font = pygame.font.Font(constant.PIXEL_FONT, 8)
    
    def register_interact(self, obj):
        if obj not in self.__interactable_objs:
            self.__interactable_objs.append(obj)

    def unregister_interact(self, obj):
        if obj in self.__interactable_objs:
            self.__interactable_objs.remove(obj)
    
    def is_registered(self, obj):
        return obj in self.__interactable_objs

    def get_closest_obj(self) -> ItemEntity | None:
        if not self.__interactable_objs or  len(self.level.snake) == 0:
            return None
        head_pos = pygame.Vector2(self.level.snake.blocks[0].rect.center)
        
        closest_obj = None
        min_distance = float('inf')

        for item in self.__interactable_objs:
            item_pos = pygame.Vector2(item.rect.center)
            distance = head_pos.distance_to(item_pos)

            if distance < min_distance:
                min_distance = distance
                closest_obj = item
        
        return closest_obj

    def handle_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[self.interaction_key]:
            closest_item = self.get_closest_obj()
            if closest_item:
                closest_item.on_pickup()

    def draw(self, surface):
        """Draw interaction prompts"""
        closest_item: ItemEntity = self.get_closest_obj() # type: ignore
        if not closest_item:
            return
        
        if closest_item.item_type.category == ItemCategory.INSTANT:
            return
        # Draw interaction prompt
        prompt_text = f"Press E to pick up {closest_item.item_type.name}"
        text_surf = self.font.render(prompt_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom=(
            closest_item.rect.centerx, # type: ignore
            closest_item.rect.top - 10 # type: ignore
        ))
        
        # Add text shadow for better visibility
        shadow_surf = self.font.render(prompt_text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(midbottom=(
            text_rect.midbottom[0] + 2,
            text_rect.midbottom[1] + 2
        ))
        
        surface.blit(shadow_surf, shadow_rect)
        surface.blit(text_surf, text_rect)
    