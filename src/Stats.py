
from enum import Enum


class Stats:
    stats = {
        "SPEED": {
            "value": 0,
            "description": "increase movement speed"
        },
        "LENGTH": {
            "value": 0,
            "description": "the overall length of the body"
        },
        "ARMOUR": {
            "value": 0,
            "description": "Increase I-frame upon hit"
        },
        "ENERGY CAPACITY": {
            "value": 0,
            "description": "increase max energy"
        },
        "ENERGY REGEN": {
            "value": 0,
            "description": "increase energy regeneration speed"
        },
        "TREASURY": {
            "value": 0,
            "description": "increase chances for more Chests"
        },
        "LUCK": {
            "value": 0,
            "description": "increase luck for loots"
        },
        "FOOD POTENCY": {
            "value": 0,
            "description": "increase amount of length foods give"
        }
    }

    @staticmethod
    def setValue(key, value):
        Stats.stats[key]["value"] = value

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
