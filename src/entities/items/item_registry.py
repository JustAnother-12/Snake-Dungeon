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
            },
            Rarity.UNCOMMON: {},
            Rarity.RARE: {
                "ouroboros": "OuroborosEntity",
            },
        },
        ItemCategory.CONSUMABLE: {
            Rarity.COMMON: {
                'bomb_item': 'BombEntity',
                'reverse': 'ReverseEntity',
                'speed_potion': 'SpeedPotionEntity',
                'energy_drink': 'EnergyDrinkEntity',
                'resistance_potion': 'ResistancePotionEntity',
            },
            Rarity.UNCOMMON: {},
            Rarity.RARE: {},
        },
        ItemCategory.SKILL: {
            Rarity.COMMON: {
                "ritual_dagger": "RitualDaggerEntity",
            },
            Rarity.UNCOMMON: {},
            Rarity.RARE: {
                "ghost_body": "GhostEntity",
            },
        },
    }

    @staticmethod
    def create_item(item_category, rarity: Rarity, level, *args, **kwargs):
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
                return None
        file_name, class_name = random.choice(list(ItemRegistry.item_registry[item_category][rarity].items()))
        if file_name == None or class_name == None:
            return None
        try: 
            import importlib
            module = importlib.import_module(f"entities.items.{item_category.value}.{file_name}")
            if hasattr(module, class_name):
                cls = getattr(module, class_name)
                try: 
                    level.item_group.add(cls(level, *args, **kwargs))
                except Exception as e:
                    print(f"Error creating item: {e}")
                    return None
            else:
                return None
        except ImportError as e:
            print(f"Error importing item: {e}")
            return None
