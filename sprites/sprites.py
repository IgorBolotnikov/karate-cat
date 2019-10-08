from secrets import randbelow
from tkinter import PhotoImage, Canvas
from time import sleep
from PIL import Image, ImageTk, ImageSequence

from .constants import *


class PlayerSpriteMixin():

    def load_player_sprite(self, root, is_ai=False):
        self.is_ai = is_ai
        self.root = root
        self.set_animation_paths()
        self.load_generic_animations()
        self.load_ai_animations() if is_ai else self.load_player_animations()
        self.current_animation_id = None
        self.is_idle = True
        self.stop_idle_animation = False
        self.frame_id = None


    # ===== PUBLIC METHODS =====


    def get_animation_duration(self, animation):
        duration = 0
        for index in range(len(animation) - 1):
            duration += animation[index][1]
        return duration


    def set_animation_paths(self):
        if self.is_ai:
            self.path = MONSTERS[randbelow(len(MONSTERS))]
            self.attack_path = self.path['path'] + MONSTER_ATTACK_PATH
            self.die_path = self.path['path'] + MONSTER_DIE_PATH
            self.hit_path = self.path['path'] + MONSTER_HIT_PATH
            self.idle_path = self.path['path'] + MONSTER_IDLE_PATH
            self.special_path = None
        else:
            self.die_path = CAT_DIE_PATH
            self.idle_path = CAT_IDLE_PATH
            self.combo_path = CAT_COMBO_PATH
            self.high_kick_path = CAT_HIGH_KICK_PATH
            self.hit_path = CAT_HIT_PATH
            self.punch_path = CAT_PUNCH_PATH
            self.top_kick_path = CAT_TOP_KICK_PATH


    def load_generic_animations(self):
        self.die_anim = self._load_animation(self.die_path)
        self.hit_anim = self._load_animation(self.hit_path)
        self.idle_anim = self._load_animation(self.idle_path)


    def load_player_animations(self):
        # self.combo_anim = self._load_animation(self.combo_path)
        # self.high_kick_anim = self._load_animation(self.high_kick_path)
        self.attack_anim = self._load_animation(self.punch_path)
        # self.top_kick_anim = self._load_animation(self.top_kick_path)


    def load_ai_animations(self):
        self.attack_anim = self._load_animation(self.attack_path)
        if self.special_path:
            self.special = self._load_animation(self.special_path)


    def set_coordinates(self, x_coord, y_coord):
        self.x_offset = self.path['offset'][0] if self.is_ai else CAT_OFFSET[0]
        self.y_offset = self.path['offset'][1] if self.is_ai else CAT_OFFSET[1]
        self.x_coord = x_coord + self.x_offset
        self.y_coord = y_coord + self.y_offset


    def update_char_sprite(self, index, frame):
        self.root.delete(self.frame_id)
        if self.is_ai:
            self.frame_id = self.root.create_image(
                self.x_coord, self.y_coord, image=frame)
        else:
            self.frame_id = self.root.create_image(
                self.x_coord, self.y_coord, image=frame)
        self.root.image = frame
        self.root.update()


    def switch_animation(self, new_animation):
        # self.box.after_cancel(self.current_animation)
        self.stop_idle_animation = True
        if not self.is_idle: return
        self.current_animation_id = self.root.after(
            0, self.run_animation, 0, new_animation)


    def run_idle_animation(self, index, animation):
        if self.stop_idle_animation:
            return
        if index >= len(self.idle_anim): index = 0
        frame = animation[index][0]
        duration = animation[index][1]
        self.update_char_sprite(index, frame)
        index += 1
        self.root.after(duration, self.run_idle_animation, index, animation)


    def run_animation(self, index, animation):
        if index >= len(animation):
            self.stop_idle_animation = False
            self.is_idle = True
            self.root.after(0, self.run_idle_animation, 0, self.idle_anim)
            return
        self.is_idle = False
        frame = animation[index][0]
        duration = animation[index][1]
        self.update_char_sprite(index, frame)
        index += 1
        self.root.after(duration, self.run_animation, index, animation)


    def run_dying_animation(self, index, animation):
        if index >= len(self.die_anim):
            self.stop_idle_animation = True
            self.is_idle = True
            return
        self.is_idle = False
        frame = animation[index][0]
        duration = animation[index][1]
        self.update_char_sprite(index, frame)
        index += 1
        self.root.after(duration, self.run_dying_animation, index, animation)


    # ===== PROTECTED METHODS =====

    def _load_animation(self, file_path):
        sequence = ImageSequence.Iterator(Image.open(file_path))
        idle_animation = []
        for image in sequence:
            duration = image.info['duration']
            idle_animation.append([ImageTk.PhotoImage(image), duration])
        return idle_animation
