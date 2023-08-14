import json

from app.constants import relative_resource_path
from app.logging_config import logger


class Effect:

    def __init__(self, name):
        self.name = name
        self.power = self.get_stat_for_effect("power")

        # Targets can be 'target' 'multihit' or 'self'
        # Target: The effect will be applied to the target of the card
        # Multihit: The effect will target the entire opposing side
        # Self: The effect will target the current player
        self.target = self.get_stat_for_effect("target")

        self.effect_type = self.get_stat_for_effect("effect_type")

        self.max_number_of_turns_active = self.get_stat_for_effect("max_number_of_turns_active")
        self.turns_remaining = self.max_number_of_turns_active

        self.phase = self.get_stat_for_effect("phase")

    def get_stat_for_effect(self, stat_name):
        json_file = (relative_resource_path("app/assets/data/effects.json"))
        with open(json_file, 'r') as file:
            data = json.load(file)

        for effect in data:
            if effect['name'] == self.name:
                return effect[stat_name]

        return None

    def is_heal(self):
        return self.effect_type == "heal"

    def reduce_counter(self, target):
        self.turns_remaining -= 1
        if self.turns_remaining == 0:
            logger.debug(f"Effect {self.name} had no turns remaining, removing it. {target.name} had {len(target.active_effects)} effects")
            target.active_effects.remove(self)
            logger.debug(f"{target.name} now has {len(target.active_effects)} effects")
