import pygame
from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from entities.throw_projectile import Throw_projectile
from levels.components.fire_breath import FireBreath
from levels.components.fire_tile import Fire_Tile
from stats import StatType, Stats
from utils.help import Share

DRAGON_BREATH_TYPE = ItemType(
    r"dragon's_breath",
    r"Dragon's Breath",
    ItemCategory.SKILL,
    Rarity.RARE,
    ItemTexture(
        constant.Texture.dragon_breath
    ),
    description="Upon activation, breaths out a barrange of fire balls in front and consumes 10 Energy each, the effect is cancel if activation button is press again or the player is out of Energy. 15s cooldown",
    cooldown=15.0,
    energy_usage=0
)

class DragonBreathStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(DRAGON_BREATH_TYPE, quantity)
        self.time = 0
        self.is_active = False
        from levels.components.fire_breath import FireBreath
        self.fire_breath: None | FireBreath = None
        
    def update(self, inventory_manager):
        self.time += Share.clock.get_time() / 1000
        return super().update(inventory_manager)
    
    def use(self, snake):
        self.active = True
        if snake.stamina < self.item_type.energy_usage:
            return False

        if self.cool_down > 0:
            if self.is_active == False:
                return False
            else:
                self.remove_effect(snake)
                return False
        
        self.apply_effect(snake)
        self.cool_down = self.item_type.cooldown
        
        return True
    
    def apply_effect(self, snake):
        self.fire_breath = FireBreath(snake.level)
        snake.level.add(self.fire_breath)
        self.is_active = True
        self.energy_regen_rate = Stats.getValue(StatType.ENERGY_REGEN)
        Stats.setValue(StatType.ENERGY_REGEN, -100)
        self.add_runtime_overriding(snake, 'update', 'after', self.activate)
    
    def remove_effect(self, snake):
        if self.fire_breath is not None:
            self.fire_breath.kill()
        self.fire_breath = None
        self.is_active = False
        Stats.setValue(StatType.ENERGY_REGEN, self.energy_regen_rate)
        self.remove_runtime_overriding(snake, 'update', 'after', self.activate)
    
    def activate(self, snake):
        if self.time >= 0.5:
            self.time = 0
            snake.stamina -= 10
            head = snake.blocks[0].rect
            mouse_pos = pygame.mouse.get_pos()
            Share.audio.set_sound_volume("fire-blast", 0.5)
            Share.audio.play_sound("fire-blast")
            throw_project = Throw_projectile(snake.level,
                                             head.centerx,
                                             head.centery,
                                             mouse_pos[0],
                                             mouse_pos[1],
                                             'orange',
                                             16 * constant.TILE_SIZE,
                                             5,
                                             4,
                                             trail_color=(255,64,0),
                                             on_expire_class=Fire_Tile,
                                             on_expire_kwargs={'width_tile': 2, 'height_tile': 2, 'burn_time': 5}
                                             )
            snake.level.add(throw_project)
        if snake.stamina <= 0:
            snake.stamina = 0
            self.remove_effect(snake)
            return
    
    def get_item_entity_class(self):
        return DragonBreathEntity
    
class DragonBreathEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, DRAGON_BREATH_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return DragonBreathStack(self.quantity)
        