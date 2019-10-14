import csv
import os
from copy import deepcopy
from .constants import *


class CSVHandlerMixin():

    def create_csv_file(self, filename, headers, delimiter):
        if os.path.isfile(self.filename):
            return
        with open(filename, WRITE, newline=NEWLINE) as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=headers, delimiter=delimiter)
            writer.writeheader()


    def read_csv_file(self, filename, headers, delimiter):
        with open(filename, READ, newline=NEWLINE) as csv_file:
            reader = csv.DictReader(
                csv_file, fieldnames=headers, delimiter=delimiter)
            rows = [row for row in reader]
            return self._remove_headers(rows)


    def write_csv_file(self, filename, headers, delimiter, contents):
        with open(filename, WRITE, newline=NEWLINE) as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=headers, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(contents)


    def search_csv_file(self, filename, headers, delimiter, keyword):
        with open(filename, READ, newline=NEWLINE) as csv_file:
            reader = csv.DictReader(
                csv_file, fieldnames=headers, delimiter=delimiter)
            result = [line for line in reader if keyword in line.values()]
            return result[0] if result else None


    @staticmethod
    def _remove_headers(rows):
        return rows[1:]


class SaveFileHandler(CSVHandlerMixin):

    def __init__(self):
        self.filename = SAVE_FILE
        self.headers = SAVE_HEADERS
        self.delimiter = SAVE_DELIMITER
        self.create_csv_file(self.filename, self.headers, self.delimiter)
        if not os.stat(self.filename).st_size == 0:
            return
        self._initialize_safe_file()


    def get_save_slots(self):
        slots = self.read_csv_file(self.filename, self.headers, self.delimiter)
        output = []
        for slot in slots:
            number = slot.get('number')
            name = slot.get('name')
            level = slot.get('level')
            output.append({
                'number': number,
                'name': name,
                'level': level
            })
        return output


    def save_player(self, player, slot_number):
        slots = self.read_csv_file(
            self.filename, self.headers, self.delimiter)
        current_slot = slots[int(slot_number) - 1]
        current_slot['name'] = player.name
        current_slot['char_class'] = player.char_class
        current_slot['level'] = int(player.level)
        current_slot['current_exp'] = int(player.current_exp)
        current_slot['wins'] = int(player.wins)
        current_slot['losses'] = int(player.losses)
        current_slot['exp_to_levelup'] = int(player.exp_to_levelup)
        current_slot['exp_cost'] = int(player.exp_cost)
        current_slot['health'] = int(player.health)
        current_slot['strength'] = int(player.strength)
        current_slot['endurance'] = int(player.endurance)
        current_slot['agility'] = int(player.agility)
        self.write_csv_file(self.filename, self.headers, self.delimiter, slots)


    def load_player(self, slot_number):
        slots = self.read_csv_file(
            self.filename, self.headers, self.delimiter)
        player = {}
        current_slot = slots[int(slot_number) - 1]
        for key, value in current_slot.items():
            player[key] = int(value) if value.isnumeric() else value
        return player if player['name'] != '[ EMPTY ]' else None


    def delete_player(self, slot_number):
        slots = self.read_csv_file(
            self.filename, self.headers, self.delimiter)
        current_slot = slots[slot_number - 1]
        current_slot['name'] = '[ EMPTY ]'
        for key in current_slot.keys():
            if key != 'number' and key != 'name': current_slot[key] = ''
        self.write_csv_file(self.filename, self.headers, self.delimiter, slots)


    def _get_blank_slot(self):
        blank_slot = {}
        for item in self.headers:
            blank_slot[item] = '' if item != 'name' else '[ EMPTY ]'
        return blank_slot


    def _initialize_safe_file(self):
        blank_slot = self._get_blank_slot()
        blank_slots = []
        for index in range(SAVE_SLOTS):
            blank_slot['number'] = index + 1
            blank_slots.append(deepcopy(blank_slot))
        self.write_csv_file(
            self.filename, self.headers, self.delimiter, blank_slots)


class CharsFileHandler(CSVHandlerMixin):

    def __init__(self):
        self.filename = CHARS_FILE
        self.headers = CHARS_HEADERS
        self.delimiter = CHARS_DELIMITER
        self.create_csv_file(self.filename, self.headers, self.delimiter)


    def give_char_classes_dict(self):
        classes_info = self.read_csv_file(
            self.filename, self.headers, self.delimiter)
        classes = [char_class.get('class_name') for char_class in classes_info]
        classes_dict = {}
        for num, name in enumerate(classes, 1):
            classes_dict[num] = name
        return classes_dict


    def get_class_stats(self, class_name):
        class_info = self.search_csv_file(
            self.filename, self.headers, self.delimiter, class_name)
        class_stats = {}
        for key, value in class_info.items():
            class_stats[key] = int(value) if value.isnumeric() else value
        return class_stats
