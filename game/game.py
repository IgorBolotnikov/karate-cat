import sys
import os
from time import sleep
from .constants import *
from gui import gui
from player import player
from file_handlers import file_handlers

class Game():

    # ===== MAGIC METHODS =====

    def __init__(self):
        self.gui = gui.GUI()
        self._name = "KARATE CAT"
        self.player1 = None
        self.player2 = None
        # Make sure that there is always a logs file present
        self.save_file = file_handlers.SaveFileHandler()
        self._show_main_screen()


    # ===== PROTECTED METHODS =====

    # ===== MAIN MENU / TITLE SCREEN =====

    def _get_main_menu_commands(self):
        commands = [
            self._menu_new_game,
            self._menu_choose_location,
            self._menu_load_game,
            self._menu_save_game,
            self._menu_view_character,
            self._menu_exit
        ]
        return commands


    def _show_main_screen(self):
        self.gui.draw_main_screen(MENU_ITEMS, self._get_main_menu_commands())


    # ===== NEW GAME MENU =====

    def _create_new_player(self):
        if not self.gui.name_entry or not self.gui.class_entry:
            self.gui.show_message(FILEDS_EMPTY_MESSAGE)
            return
        name = self.gui.name_entry.get()
        char_class = self.gui.class_entry.get(
            self.gui.class_entry.curselection())
        self.player1 = player.Player(name=name, char_class=char_class)
        self.gui.show_message(PLAYER_CREATED_MESSAGE)
        self._show_main_screen()


    def _get_new_game_commands(self):
        commands = [
            self._show_main_screen,
            self._create_new_player
        ]
        return commands


    def _menu_new_game(self):
        commands = self._get_new_game_commands()
        classes = file_handlers.CharsFileHandler().give_char_classes_dict()
        self.gui.draw_new_game_screen(classes.values(), commands)


    # ===== LOCATION MENU =====

    def get_location_commands(self):
        commands = [
            self._show_main_screen,
            self._preview_location,
            self._menu_play
        ]
        return commands


    def _preview_location(self):
        commands = self.get_location_commands()
        self.gui.draw_new_location_screen(commands)


    def _menu_choose_location(self):
        if not self.player1:
            self.gui.show_message(NO_CHARACTER_MESSAGE)
            return
        commands = self.get_location_commands()
        self.gui.draw_location_screen(commands)


    # ===== FIGHT MENU =====

    def _start_a_fight(self):
        if not self.gui.chosen_bodypart.get(): return
        self.gui.frame.delete(self.gui.status_text)
        self.gui.action_button.destroy()
        self._play_one_round(self.attack_player, self.defence_player)
        winner, loser = self._get_winner_and_loser()
        if winner:
            self.gui.delay = loser.get_animation_duration(loser.die_anim)
            loser.switch_animation(loser.die_anim)
            self.gui.is_winner_ai = winner.is_ai
            self.gui.frame.after(
                self.gui.delay,
                self.gui.draw_endgame_screen,
                self.get_endgame_commands())
            winner.wins += 1
            loser.losses += 1
            self.player1.health = self.player1.max_health
            self.player2.health = self.player2.max_health
            self._add_exp_to_player(winner, loser.exp_cost)
            return
        # switch attacking and defending players
        self.attack_player, self.defence_player = \
            self.defence_player, self.attack_player
        self.gui.ai_turn = self.attack_player.is_ai
        self.gui.frame.after(
            self.gui.delay,
            self.gui.update_fight_screen,
            self._get_play_commands())


    def _play_one_round(self, attack_player, defence_player):
        attack = attack_player.choose_bodypart() if attack_player.is_ai \
            else self.gui.chosen_bodypart.get()
        defence = defence_player.choose_bodypart() if defence_player.is_ai \
            else self.gui.chosen_bodypart.get()
        self.gui.delay = attack_player.get_animation_duration(
            attack_player.attack_anim)
        attack_player.switch_animation(attack_player.attack_anim)
        if attack != defence:
            damage = (attack_player.attack_value
                  - defence_player.defence_value)
            defence_player.health -= damage
            defence_player.health = 0 if (
                defence_player.health < 0) else defence_player.health
            message = f'{damage} DMG'
            self.gui.frame.after(
                self.gui.delay,
                self.gui.draw_attack_status,
                defence_player,
                message)
            self.gui.frame.after(
                self.gui.delay,
                defence_player.switch_animation,
                defence_player.hit_anim)
        else:
            message = 'Blocked'
            self.gui.frame.after(
                self.gui.delay,
                self.gui.draw_attack_status,
                defence_player,
                message)


    def _get_winner_and_loser(self):
        if self.player1.health <= 0:
            return self.player2, self.player1
        elif self.player2.health <= 0:
            return self.player1, self.player2
        else:
            return None, None


    def _add_exp_to_player(self, player, exp_amount):
        player.current_exp += exp_amount
        if player.current_exp == player.exp_to_levelup:
            self.gui.show_message(LEVELUP_MESSAGE)
            player._increase_player_level()


    def _get_play_commands(self):
        commands = [
            self._start_a_fight,
            self._show_main_screen,
        ]
        return commands


    def get_endgame_commands(self):
        commands = [
            self._show_main_screen
        ]
        return commands


    def _menu_play(self):
        self.player2 = player.Player(is_ai=True)
        self.attack_player = self.player1
        self.defence_player = self.player2
        self.gui.ai_turn = self.attack_player.is_ai
        self.gui.draw_fight_screen(
            self.player1, self.player2, self._get_play_commands())


    # ===== LOAD GAME MENU =====

    def _load_player(self):
        loaded_player = self.save_file.load_player(
            self.gui.chosen_slot.get())
        if not loaded_player:
            self.gui.show_message(EMPTY_SLOT_MESSAGE)
            return
        self.player1 = player.Player(
            loaded_player['name'], loaded_player['char_class'],
            loaded_player['level'], loaded_player['current_exp'],
            loaded_player['wins'], loaded_player['losses'],
            loaded_player['exp_to_levelup'], loaded_player['exp_cost'],
            loaded_player['health'], loaded_player['strength'],
            loaded_player['endurance'], loaded_player['agility'])
        self.gui.show_message(PLAYER_LOADED_MESSAGE)
        self._show_main_screen()


    def _get_load_game_commands(self):
        commands = [
            self._show_main_screen,
            self._load_player,
        ]
        return commands


    def _menu_load_game(self):
        slots = self.save_file.get_save_slots()
        commands = self._get_load_game_commands()
        self.gui.draw_save_slots_screen(slots, commands, load=True)


    # ===== SAVE GAME MENU =====

    def _delete_slot(self):
        message = self.gui.ask_confirmation(SAVE_DELETE_MESSAGE)
        if message:
            self.save_file.delete_player(int(self.gui.chosen_slot.get()))
            self.gui.show_message(PLAYER_DELETED_MESSAGE)
            slots = self.save_file.get_save_slots()
            commands = self._get_save_game_commands()
            self.gui.draw_save_slots_screen(slots, commands)


    def _save_player(self):
        slots = self.save_file.get_save_slots()
        slot_num = int(self.gui.chosen_slot.get()) # 0-based list
        commands = self._get_save_game_commands()
        if slots[slot_num]['name'] == '[ EMPTY ]':
            self.save_file.save_player(self.player1, slot_num)
            self.gui.show_message(PLAYER_SAVED_MESSAGE)
            slots = self.save_file.get_save_slots()
            self.gui.draw_save_slots_screen(slots, commands)
        else:
            message = self.gui.ask_confirmation(SAVE_OVERWRITE_MESSAGE)
            if message:
                self.save_file.save_player(self.player1, slot_num)
                self.gui.show_message(PLAYER_SAVED_MESSAGE)
                slots = self.save_file.get_save_slots()
                self.gui.draw_save_slots_screen(slots, commands)


    def _get_save_game_commands(self):
        commands = [
            self._show_main_screen,
            self._delete_slot,
            self._save_player,
        ]
        return commands


    def _menu_save_game(self):
        if not self.player1:
            self.gui.show_message(NO_CHARACTER_MESSAGE)
            return
        slots = self.save_file.get_save_slots()
        commands = self._get_save_game_commands()
        self.gui.draw_save_slots_screen(slots, commands)


    def _get_char_menu_commands(self):
        commands = [
            self._show_main_screen,
        ]
        return commands


    def _menu_view_character(self):
        if not self.player1:
            return self.gui.show_message(NO_CHARACTER_MESSAGE)
        commands = self._get_char_menu_commands()
        self.gui.draw_character_screen(self.player1, commands)


    def _menu_exit(self):
        return sys.exit()
