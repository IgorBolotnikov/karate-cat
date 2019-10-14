import os

BASE_DIR = os.path.dirname(__file__)

BACKGROUND_COLOR_HEX = '0072BB'

CAT_GRAPHICS_PATH = BASE_DIR + '/Char/Cat/'
CAT_COMBO_PATH = CAT_GRAPHICS_PATH + 'cat_combo.gif'
CAT_DIE_PATH = CAT_GRAPHICS_PATH + 'cat_die.gif'
CAT_FALL_PATH = CAT_GRAPHICS_PATH + 'cat_fall.gif'
CAT_FORCE_PUSH_PATH = CAT_GRAPHICS_PATH + 'cat_force_push.gif'
CAT_HADOUKEN_PATH = CAT_GRAPHICS_PATH + 'cat_hadouken.gif'
CAT_TOP_KICK_PATH = CAT_GRAPHICS_PATH + 'cat_top_kick.gif'
CAT_HIGH_KICK_PATH = CAT_GRAPHICS_PATH + 'cat_high_kick.gif'
CAT_HIT_PATH = CAT_GRAPHICS_PATH + 'cat_hit.gif'
CAT_IDLE_PATH = CAT_GRAPHICS_PATH + 'cat_idle.gif'
CAT_JUMP_KICK_PATH = CAT_GRAPHICS_PATH + 'cat_jump_kick.gif'
CAT_JUMP_PATH = CAT_GRAPHICS_PATH + 'cat_jump.gif'
CAT_PUNCH_PATH = CAT_GRAPHICS_PATH + 'cat_punch.gif'
CAT_UPPERCUT_PATH = CAT_GRAPHICS_PATH + 'cat_uppercut.gif'
CAT_WALK_PATH = CAT_GRAPHICS_PATH + 'cat_walk.gif'
CAT_OFFSET = [-50, 0]

MONSTERS = [
    {
        'path': BASE_DIR + '/Char/Cute_Monster/',
        'offset': [50, 0],
    },{
        'path': BASE_DIR + '/Char/Demonic_Flower/',
        'offset': [50, -12],
    },{
        'path': BASE_DIR + '/Char/Flying_Monster/',
        'offset': [50, -20],
    },{
        'path': BASE_DIR + '/Char/Scull_Monster/',
        'offset': [50, -28],
    }
]

MONSTER_ATTACK_PATH =  'mon_attack.gif'
MONSTER_DIE_PATH = 'mon_die.gif'
MONSTER_HIT_PATH = 'mon_hit.gif'
MONSTER_IDLE_PATH = 'mon_idle.gif'
