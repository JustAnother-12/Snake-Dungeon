import pygame
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ItemCategory, Rarity


class ItemRegistry:

    item_registry = {
        ItemCategory.INSTANT: {
            Rarity.COMMON: {
                "dungeon_essence": "DungeonEssenceEntity",
                "earth_essence": "EarthEssenceEntity",
                "gale_essence": "GaleEssenceEntity",
                "gluttony_essence": "GluttonyEssenceEntity",
                "gold_essence": "GoldEssenceEntity",
                "lightning_essence": "LightningEssenceEntity",
                "luck_essence": "LuckEssenceEntity",
                "water_essence": "WaterEssenceEntity",
            },
            Rarity.UNCOMMON: {
                "energized_crystal": "EnergizedCrystalEntity",
                "green_jade": "GreenJadeEntity",
                "appetite_stimulant": "AppetiteStimulantEntity",
                "aerolite_plate": "AerolitePlateEntity",
            },
            Rarity.RARE: {
                "dungeon_essence": "DungeonEssenceEntity",
                "adrenaline_syringe": "AdrenalineSyringeEntity",
            },
        },
        ItemCategory.EQUIPMENT: {
            Rarity.COMMON: {
                "time_efficiency": "TimeEfficiencyEntity",
                'fire_gem_amulet': 'FireGemAmuletEntity',
            },
            Rarity.UNCOMMON: {
                'trail_of_flame': 'FlameTrailEntity',
                'midas_blood': 'MidasBloodEntity',
                'hephaestus_blood': 'HephaestusBloodEntity',
            },
            Rarity.RARE: {
                "ouroboros": "OuroborosEntity",
                'blood_bomb_devil': 'BloodBombDevilEntity',
            },
        },
        ItemCategory.CONSUMABLE: {
            Rarity.COMMON: {
                'bomb_item': 'BombEntity',
                'reverse': 'ReverseEntity',
                'speed_potion': 'SpeedPotionEntity',
                'energy_drink': 'EnergyDrinkEntity',
                'resistance_potion': 'ResistancePotionEntity',
                'molotov': 'MolotovEntity',
            },
            Rarity.UNCOMMON: {
                'fire_bomb_item': 'FireBombEntity'
            },
            Rarity.RARE: {
                'celestine_fragment': 'CelestineFragmentEntity',
            },
        },
        ItemCategory.SKILL: {
            Rarity.COMMON: {
                "ritual_dagger": "RitualDaggerEntity",
                "ghost_body": "GhostEntity",
            },
            Rarity.UNCOMMON: {
                "dragon_breath": "DragonBreathEntity"
            },
            Rarity.RARE: {
                'celestine_amulet': 'CelestineAmuletEntity',
                'gun_devil_contract': 'GunEntity',
            },
        },
    }

    @staticmethod
    def create_item(item_category, rarity: Rarity, level, *args, **kwargs) -> ItemEntity:
        '''
        Tạo item từ item_category và rarity
        - item_category: loại item (ItemCategory | LootItem)
        - rarity: độ hiếm của item (Rarity)
        '''
        import random
        from loot import LootItem
        if isinstance(item_category, LootItem):
            category_name = item_category.name
            if hasattr(ItemCategory, category_name):
                item_category = getattr(ItemCategory, category_name)
            else:
                raise ValueError(
                    f"Invalid item category: {category_name}")

        list_item = list(
            ItemRegistry.item_registry[item_category][rarity].items())
        if len(list_item) == 0:
            raise ValueError(
                f"No items found for category {item_category} and rarity {rarity}")
        file_name, class_name = random.choice(list_item)
        if file_name == None or class_name == None:
            raise ValueError(
                f"Invalid item name or class name: {file_name}, {class_name}")

        import importlib
        module = importlib.import_module(
            f"entities.items.{item_category.value}.{file_name}")
        if hasattr(module, class_name):
            cls = getattr(module, class_name)
            kwargs_copy = kwargs.copy()
            pos = kwargs_copy.pop('pos', None)
            item = cls(level, *args, **kwargs_copy)
            # set position nếu có truyền vào pos
            if pos is not None:
                item.pos = pygame.Vector2(pos)
                item.rect = item.image.get_rect(topleft=item.pos)
                if not item.check_pos(item.image):
                    item.random_pos(None, r=2)
            # set quantity nếu là consumables
            if item_category is ItemCategory.CONSUMABLE:
                item.quantity = random.randint(1, item.item_type.max_stack)
            return item
        else:
            raise AttributeError(
                f"Class {class_name} not found in module {file_name}")
