
from enum import Enum

class StatType(Enum):
    SPEED = "SPEED"
    LENGTH = "LENGTH"
    RESISTANCE = "RESISTANCE"
    ENERGY_CAPACITY = "ENERGY CAPACITY"
    ENERGY_REGEN = "ENERGY REGEN"
    TREASURY = "TREASURY"
    LUCK = "LUCK"
    FOOD_POTENCY = "FOOD POTENCY"
class Stats:
    stats = {
        StatType.SPEED: {
            "value": 0,
            "description": "increase movement speed"
        },
        StatType.LENGTH: {
            "value": 0,
            "description": "the overall length of the body"
        },
        StatType.RESISTANCE: {
            "value": 0,
            "description": "Increase I-frame upon hit"
        },
        StatType.ENERGY_CAPACITY: {
            "value": 0,
            "description": "increase max energy"
        },
        StatType.ENERGY_REGEN: {
            "value": 0,
            "description": "increase energy regeneration speed"
        },
        StatType.TREASURY: {
            "value": 0,
            "description": "increase chances for more Chests"
        },
        StatType.LUCK: {
            "value": 0,
            "description": "increase luck for loots"
        },
        StatType.FOOD_POTENCY: {
            "value": 0,
            "description": "increase amount of length foods give"
        }
    }

    @staticmethod
    def setValue(key, value):
        Stats.stats[key]["value"] = min(value, 100)

    @staticmethod
    def increaseValue(key, value):
        Stats.setValue(key, Stats.getValue(key) + value)

    @staticmethod
    def getValue(key):
        return Stats.stats[key]["value"]

    @staticmethod
    def getDescription(key):
        return Stats.stats[key]["description"]

    @staticmethod
    def reset():
        for key in Stats.stats:
            Stats.stats[key]["value"] = 0

