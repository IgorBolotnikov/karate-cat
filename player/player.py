import os
from random import randint
from .constants import *
from sprites.sprites import PlayerSpriteMixin
from file_handlers import file_handlers


class Player(PlayerSpriteMixin):

    # ===== MAGIC METHODS =====

    def __init__(self, name=None, char_class=None, level=1,
                 current_exp=0, wins=0, losses=0, exp_to_levelup=100,
                 exp_cost=10, health=None, strength=None, endurance=None,
                 agility=None, is_ai=False):
        self.chars_file = file_handlers.CharsFileHandler()
        self._make_AI_player() if is_ai else \
            self._make_human_player(name, char_class)
        player_class = self.chars_file.get_class_stats(self.char_class)
        self.health = health if health else player_class['health']
        self.max_health = health if health else player_class['health']
        self.strength = strength if strength else player_class['strength']
        self.endurance = endurance if endurance else player_class['endurance']
        self.agility = agility if agility else player_class['agility']
        self.exp_to_levelup = exp_to_levelup
        self.exp_cost = exp_cost
        self.level = level
        self.current_exp = current_exp
        self.wins = wins
        self.losses = losses
        self.is_ai = is_ai


    def __str__(self):
        name = f'Player <{self.name}>\n'
        level = f'Level: {self.level}\n'
        current_exp = f'Current EXP: {self.current_exp}\n'
        exp_to_levelup = f'EXP to Level UP: {self.exp_to_levelup}\n'
        char_class = f'Class: "{self.char_class}"\n'
        health = f'HP: {self.health}\n'
        strength = f'STR: {self.strength}\n'
        endurance = f'END: {self.endurance}\n'
        agility = f'AGI: {self.agility}\n'
        wins = f'Wins: {int(self.wins)}\n'
        losses = f'Losses: {int(self.losses)}'
        return '{}{}{}{}{}{}{}{}{}{}{}'.format(
            name, level, current_exp, exp_to_levelup, char_class,
            health, strength, endurance, agility, wins, losses)


    def __lt__(self, other):
        return (self._rounds_to_survive(other) < other._rounds_to_survive(self))


    def __le__(self, other):
        return (self._rounds_to_survive(other) <= other._rounds_to_survive(self))


    def __eq__(self, other):
        return (self._rounds_to_survive(other) == other._rounds_to_survive(self))


    def __ne__(self, other):
        return (self._rounds_to_survive(other) != other._rounds_to_survive(self))


    def __lt__(self, other):
        return (self._rounds_to_survive(other) < other._rounds_to_survive(self))


    def __gt__(self, other):
        return (self._rounds_to_survive(other) > other._rounds_to_survive(self))


    def __ge__(self, other):
        return (self._rounds_to_survive(other) >= other._rounds_to_survive(self))


    # ===== ADDITIONAL PROPERTIES =====

    # This property return value can be expanded later
    @property
    def attack_value(self):
        return int(self.strength * ATTACK_COEFF)


    # This property return value can be expanded later
    @property
    def defence_value(self):
        return int(self.endurance * DEFENCE_COEFF)


    @property
    def bodyparts(self):
        return BODYPARTS


    # ===== PUBLIC METHODS =====

    def print_bodyparts(self):
        for num, bodypart in BODYPARTS.items():
            print(f'{num}: {bodypart}')


    def choose_bodypart(self):
        if self.is_ai:
            bodypart = randint(1, len(self.bodyparts))
        else:
            bodypart = self.bodypart
        return BODYPARTS[bodypart]


    # ===== PROTECTED METHODS =====

    def _make_human_player(self, name, char_class):
        self.name = name
        self.char_class = char_class


    def _make_AI_player(self):
        # Name can be passed if making particular AI character
        self.name = 'AI'
        classes = self.chars_file.give_char_classes_dict()
        class_num = randint(1, len(self.bodyparts))
        class_name = classes[class_num]
        self.char_class = class_name


    def _increase_player_level(self):
        self.level += 1
        self.current_exp = 0
        self.health += HEALTH_ADDER
        self.max_health += HEALTH_ADDER
        self.strength = int(self.strength * STATS_COEFF)
        self.endurance = int(self.endurance * STATS_COEFF)
        self.agility = int(self.agility * STATS_COEFF)
        self.exp_to_levelup = int(self.exp_to_levelup * EXP_COEFF)
        self.exp_cost = int(self.exp_cost * EXP_COEFF)


    def _rounds_to_survive(self, enemy):
        places_to_hit = len(BODYPARTS)
        # Calculate the probability of failing
        # to deflect an enemy attack and sustaining damage
        damage_probability = (places_to_hit - 1) / places_to_hit
        final_damage = enemy.attack_value - self.defence_value
        probable_gamage_per_hit = damage_probability * final_damage
        # Return the number of enemy attacks
        # a character can survive with given probability
        return round(self.health / probable_gamage_per_hit, 2)
