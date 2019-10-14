from os import path

BASE_DIR = path.dirname(__file__)

# ===== CSVHandlerMixin CONSTANTS =====

READ = 'r'
WRITE = 'w'
NEWLINE = ''

# ===== SaveFile CONSTANTS =====

SAVE_FILE = BASE_DIR + '/save.csv'
SAVE_HEADERS = ['number', 'name', 'char_class', 'level', 'current_exp',
                'wins', 'losses', 'exp_to_levelup', 'exp_cost',
                'health', 'strength', 'endurance', 'agility']
SAVE_DELIMITER = ','
SAVE_SLOTS = 5

# ===== CharsFile CONSTANTS =====

CHARS_FILE = BASE_DIR + '/characters.csv'
CHARS_HEADERS = ['class_name', 'description', 'health',
                 'strength', 'endurance', 'agility']
CHARS_DELIMITER = ','
