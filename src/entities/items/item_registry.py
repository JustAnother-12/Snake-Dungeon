from tkinter import E


class ItemRegistry:
    from entities.items.item_type import ItemCategory, Rarity

    item_registry = {
        ItemCategory.INSTANT: {
            Rarity.COMMON: {
                'dungeon_essence': 'DungeonEssenceEntity',
                'earth_essence': 'EarthEssenceEntity',
                'gale_essence': 'GaleEssenceEntity',
                'gluttony_essence': 'GluttonyEssenceEntity',
                'gold_essence': 'GoldEssenceEntity',
                'lightning_essence': 'LightningEssenceEntity',
                'luck_essence': 'LuckEssenceEntity',
                'water_essence': 'WaterEssenceEntity',
            },
            Rarity.UNCOMMON: {},
            Rarity.RARE: {},
        },
        ItemCategory.EQUIPMENT: {
            Rarity.COMMON: {},
            Rarity.UNCOMMON: {},
            Rarity.RARE: {},
        },
        ItemCategory.CONSUMABLE: {
            Rarity.COMMON: {},
            Rarity.UNCOMMON: {},
            Rarity.RARE: {},
        },
        ItemCategory.SKILL: {
            Rarity.COMMON: {},
            Rarity.UNCOMMON: {},
            Rarity.RARE: {},
        },
    }

    @staticmethod
    def create_item(item_category: ItemCategory, rarity: Rarity, level, *args, **kwargs):
        import random
        file_name, class_name = random.choice(list(ItemRegistry.item_registry[item_category][rarity].items()))
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
