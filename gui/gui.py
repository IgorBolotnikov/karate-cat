import tkinter.messagebox as messagebox
from secrets import randbelow
from tkinter import *
from time import sleep
from PIL import Image, ImageTk, ImageSequence
from .constants import *
from player import player
from api import app


class GUI():

    def __init__(self):
        self.root = Tk()
        self.frame = Canvas(self.root)
        self.root.resizable(width=False, height=False)
        self.name_entry = None
        self.class_entry = None
        self.google = app.GoogleAPI()
        self.weather = app.WeatherAPI()
        self.current_location = None
        self.current_scene = None


    @staticmethod
    def show_message(message):
        return messagebox.showinfo('Message', message)


    @staticmethod
    def ask_confirmation(message):
        return messagebox.askyesno('Warning', message)


    @staticmethod
    def get_menu_rectangle_coords(menu_width, menu_height):
        x_coord_start = int(WINDOW_WIDTH / 2 - menu_width / 2)
        y_coord_start = int(WINDOW_HEIGHT / 2 - menu_height / 2)
        x_coord_end = x_coord_start + menu_width
        y_coord_end = y_coord_start + menu_height
        return (x_coord_start, y_coord_start, x_coord_end, y_coord_end)


    # FOR FUTURE USAGE

    # def bind_aminations_to_controls(self, object):
    #     object.bind('1', self.respond_to_controls)
    #     object.bind('2', self.respond_to_controls)
    #     object.bind('3', self.respond_to_controls)
    #     object.bind('4', self.respond_to_controls)
    #
    #
    # def respond_to_controls(self, event):
    #     if event.keysym == '1':
    #         self.player.switch_animation(self.player.combo_anim)
    #     if event.keysym == '2':
    #         self.player.switch_animation(self.player.top_kick_anim)
    #     if event.keysym == '3':
    #         self.player.switch_animation(self.player.attack_anim)
    #     if event.keysym == '4':
    #         self.player.switch_animation(self.player.punch_anim)


    def draw_main_screen(self, menu_items, menu_commands):
        self.draw_frame()
        self.draw_background(MAIN_SCENE_PATH)
        self.draw_main_menu(menu_items, menu_commands)


    def draw_new_game_screen(self, classes, commands):
        self.draw_frame()
        self.draw_background(MAIN_SCENE_PATH)
        self.draw_new_player_menu(classes, commands)


    def draw_character_screen(self, player, commands):
        self.draw_frame()
        self.draw_background(MAIN_SCENE_PATH)
        self.draw_character_menu(player, commands)


    def draw_new_location_screen(self, commands):
        if not self.current_scene:
            return
        self.draw_frame()
        self.draw_background(self.current_scene)
        self.draw_location_menu(commands)


    def draw_location_screen(self, commands):
        self.draw_frame()
        self.draw_background(MAIN_SCENE_PATH)
        self.draw_location_menu(commands)


    def draw_fight_screen(self, player, enemy, commands):
        self.draw_frame()
        if self.current_scene:
            self.draw_background(self.current_scene)
        else:
            self.draw_background(SCENES[2])
        if self.current_location:
            self.draw_header(f'Outskirts of {self.current_location.split(",")[0]}')
        else:
            self.draw_header('Outskirts of Noorgaard')
        self.status_text = None
        self.draw_player(player)
        self.draw_enemy(enemy)
        self.player.healthbar = None
        self.player.healthbar_text = None
        self.draw_character_healthbar(self.player)
        self.enemy.healthbar = None
        self.enemy.healthbar_text = None
        self.draw_character_healthbar(self.enemy)
        self.chosen_bodypart = StringVar()
        self.draw_action_display(commands)


    def draw_endgame_screen(self, commands):
        self.draw_frame()
        if self.current_scene:
            self.draw_background(self.current_scene)
        else:
            self.draw_background(SCENES[2])

        if self.current_location:
            self.draw_header(f'Outskirts of {self.current_location.split(",")[0]}')
        else:
            self.draw_header('Outskirts of Noorgaard')
        self.draw_endgame_message(commands)


    def update_fight_screen(self, commands):
        self.draw_character_healthbar(self.player)
        self.draw_character_healthbar(self.enemy)
        self.update_action_display(commands)


    def draw_save_slots_screen(self, slots, commands, load=False):
        self.draw_frame()
        self.draw_background(MAIN_SCENE_PATH)
        self.draw_slots_menu(commands, load)
        self.draw_save_slots(slots)


    def draw_frame(self):
        self.frame.destroy()
        self.frame = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.frame.pack()


    def draw_menu_rectangle(self, coords):
        return self.frame.create_rectangle(coords, fill=MENU_BG_COLOR)


    def draw_text(self, coords, text):
        return self.frame.create_text(
            coords, font=GAME_FONT, justify='center', text=text)


    def draw_button(self, menu_coords, position, text, command):
        coords = self.get_button_coords(menu_coords, position)
        button = Button(
            self.frame, text=text, command=command,
            height=BUTTON_HEIGHT_CHARS, width=BUTTON_WIDTH_CHARS)
        button.place(x=coords[0], y=coords[1])
        return button


    def get_button_coords(self, menu_coords, position):
        if position == 'left':
            x_coord = menu_coords[0] + PADDING
        if position == 'centre':
            x_coord = int(WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2)
        if position == 'right':
            x_coord = menu_coords[2] - BUTTON_WIDTH - PADDING
        y_coord = menu_coords[3] - BUTTON_HEIGHT - PADDING
        return (x_coord, y_coord)

    # ===== MAIN MENU =====

    # mathematics incoming!
    def draw_menu_item(self, item, item_num, start_y_offset, command):
        item_offset = int(item_num * (MAIN_BUTTON_HEIGHT + BUTTON_SPACING))
        x_coord = int(WINDOW_WIDTH / 2 - MAIN_BUTTON_WIDTH / 2)
        y_coord = int(WINDOW_HEIGHT / 2 - start_y_offset \
                      + item_offset - MAIN_BUTTON_HEIGHT / 2)
        button_frame = Frame(
            self.frame, height=MAIN_BUTTON_HEIGHT, width=MAIN_BUTTON_WIDTH)
        button = Button(button_frame, font=(GAME_FONT, BUTTON_FONT_SIZE),
                        command=command, cursor='circle', relief=BUTTON_LOOK,
                        text=item)
        button_frame.place(x=x_coord, y=y_coord)
        button_frame.propagate(False)
        button.pack(expand=True, fill='both')


    # mathematics incoming!
    def draw_main_menu(self, menu_items, commands):
        menu_height = int(len(menu_items) * MAIN_BUTTON_HEIGHT \
                          + (len(menu_items) - 1) * BUTTON_SPACING)
        start_y_offset = int(menu_height / 2)
        for number, item in enumerate(menu_items):
            self.draw_menu_item(
                item, number, start_y_offset, commands[number])

    # ===== NEW GAME MENU =====

    def draw_new_player_menu(self, classes, commands):
        menu_coords = self.get_menu_rectangle_coords(
            NEW_GAME_MENU_WIDTH, NEW_GAME_MENU_HEIGHT)
        self.name_entry = Entry(self.frame, font=GAME_FONT, width=19, bd=1)
        self.class_entry = Listbox(
            self.frame, font=GAME_FONT, selectmode='single', height=len(classes))
        self.draw_menu_rectangle(menu_coords)
        self.draw_text((TEXT_X_COORD, NAME_TEXT_Y_COORD), ENTER_NAME_TEXT)
        self.draw_text((TEXT_X_COORD, CLASS_TEXT_Y_COORD), CHOOSE_CLASS_TEXT)
        self.name_entry.place(x=ENTRY_X_COORD, y=ENTRY_Y_COORD)
        self.class_entry.place(x=LIST_X_COORD, y=LIST_Y_COORD)
        self.draw_button(menu_coords, 'left' ,'BACK', commands[0])
        self.draw_button(menu_coords, 'right', 'CONFIRM', commands[1])
        for item in classes: self.class_entry.insert('end', item)

    # ===== LOCATION MENU =====

    def get_weather(self, event):
        self.loc_list.grid_forget()
        if not self.loc_list.curselection():
            return
        self.loc_choice.set(self.loc_list.get(self.loc_list.curselection()))
        locations = self.loc_choice.get().split(', ')
        city = locations[0]
        country = locations[-1]
        self.current_location = self.loc_choice.get()
        weather = self.weather.get_weather_by_city(city, country)
        scene = [scene for scene in SCENES if scene['name'] == weather]
        self.current_scene = scene[0]


    def _show_suggestions(self, *args):
        self.loc_list.destroy()
        suggestions = self.google.get_locations_by_input(self.loc_choice.get())
        if suggestions:
            self.loc_list = Listbox(
                self.frame, height=len(suggestions), selectmode='single')
            for suggestion in suggestions:
                self.loc_list.insert('end', suggestion)
            self.loc_list.place(
                x=int(WINDOW_WIDTH / 2 - 90),
                y=LOC_MENU_Y_START + PADDING + 25 + TEXT_HEIGHT)
            self.loc_list.bind('<<ListboxSelect>>', self.get_weather)
        self.frame.update()


    def _listen_for_input(self):
        while True:
            user_input = self.entry.get()
            if input != self.string:
                self.string = user_input
                self._show_suggestions


    def draw_location_menu(self, commands):
        menu_coords = self.get_menu_rectangle_coords(
            LOC_MENU_WIDTH, LOC_MENU_HEIGHT)
        self.loc_choice = StringVar()
        self.loc_choice.set(self.current_location) if self.current_location else ''
        self.loc_choice.trace_add("write", self._show_suggestions)
        self.loc_entry = Entry(
            width=LOC_INPUT_WIDTH, textvar=self.loc_choice)
        self.loc_list = Listbox(self.frame)
        self.draw_menu_rectangle(menu_coords)
        self.draw_text((LOC_TEXT_X_COORD, LOC_TEXT_Y_COORD), LOC_TEXT)
        self.loc_entry.place(
            x=int(WINDOW_WIDTH / 2 - 91),
            y=menu_coords[1] + PADDING + TEXT_HEIGHT)
        self.draw_button(menu_coords, 'left', 'BACK', commands[0])
        self.draw_button(menu_coords, 'centre', 'PREVIEW', commands[1])
        self.draw_button(menu_coords, 'right', 'PLAY', commands[2])

    # ===== FIGHTING GUI =====

    def draw_background(self, file_path):
        self.scene_file = file_path # make dynamic
        self.scene = ImageTk.PhotoImage(Image.open(self.scene_file['path']))
        self.frame.create_image(
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, image=self.scene)


    # mathematics incoming!
    def draw_header(self, text):
        header_bg_len = int((len(text)+2) * HEADER_FONT_SIZE * GAME_FONT_RATIO)
        header_bg_x = int(WINDOW_WIDTH / 2 - header_bg_len / 2)
        header_bg_y = HEADER_Y_COORD - int(HEADER_FONT_SIZE / 2)
        self.frame.create_rectangle(
            (header_bg_x, header_bg_y, header_bg_x + header_bg_len,
             header_bg_y + int(HEADER_FONT_SIZE * 1.1)),
            fill=MENU_BG_COLOR, width=2)
        self.frame.create_text((int(WINDOW_WIDTH / 2), HEADER_Y_COORD),
                               text=text, font=(GAME_FONT, HEADER_FONT_SIZE))


    def draw_player(self, player):
        self.player = player
        self.player.root = self.frame
        self.player.load_player_sprite(self.frame)
        self.player.current_animation_id = self.player.root.after(
            0, self.player.run_idle_animation, 0, self.player.idle_anim)
        self.player.set_coordinates(self.scene_file['char_position'][0],
                                    self.scene_file['char_position'][1])


    def draw_enemy(self, enemy, is_ai=True):
        self.enemy = enemy
        self.player.root = self.frame
        self.enemy.load_player_sprite(self.frame, is_ai)
        self.enemy.current_animation_id = self.enemy.root.after(
            0, self.enemy.run_idle_animation, 0, self.enemy.idle_anim)
        self.enemy.set_coordinates(self.scene_file['char_position'][0],
                                   self.scene_file['char_position'][1])


    # mathematics incoming!
    def draw_character_healthbar(self, character):
        health_percentage = int((character.health / character.max_health) * 100)
        health_percentage = 0 if health_percentage < 0 else health_percentage
        current_healthbar_length = (health_percentage / 100) * HEALTHBAR_LENGTH
        health_color = HEALTHBAR_COLORS[health_percentage // 10]
        health_x_coord = character.x_coord
        health_y_coord = character.y_coord + character.y_offset + HEALTH_OFFSET
        health_box_x = health_x_coord - int(HEALTHBAR_LENGTH / 2)
        health_box_y = health_y_coord - int(HEALTHBAR_HEIGHT / 2)
        if not character.healthbar:
            self.frame.create_rectangle(
                (health_box_x, health_box_y,
                 health_box_x + HEALTHBAR_LENGTH,
                 health_box_y + HEALTHBAR_HEIGHT),
                fill=HEALTHBAR_BG_COLOR, width=2)
        self.frame.delete(character.healthbar)
        self.frame.delete(character.healthbar_text)
        character.healthbar = self.frame.create_rectangle(
            (health_box_x + 1, health_box_y + 1,
             health_box_x + current_healthbar_length - 1,
             health_box_y + HEALTHBAR_HEIGHT - 1),
            fill=health_color, width=0)
        character.healthbar_text = self.frame.create_text(
            (health_x_coord, health_y_coord),
            text=str(character.health),
            fill=HEALTH_TEXT_COLOR, font=GAME_FONT)


    def draw_attack_status(self, character, message):
        text_x_coord = character.x_coord
        text_y_coord = character.y_coord + character.y_offset + HEALTH_OFFSET - 30
        self.status_text = self.frame.create_text(
            (text_x_coord, text_y_coord),
            font=GAME_FONT,
            text=message,
            fill=ATTACK_STATUS_COLOR)
        self.frame.after(100, self.move_attack_status, 0)


    def move_attack_status(self, index):
        if index > 5:
            self.frame.delete(self.status_text)
            return
        self.frame.move(self.status_text, 0, -2)
        index += 1
        self.frame.after(100, self.move_attack_status, index)


    def draw_action_display(self, commands):
        prompt = DEFEND_PROMPT if self.ai_turn else ATTACK_PROMPT
        self.frame.create_rectangle(
            (WINDOW_WIDTH / 2 - 50, HEADER_Y_COORD + 30,
             WINDOW_WIDTH / 2 + 50, HEADER_Y_COORD + 50),
            fill=MENU_BG_COLOR)
        self.prompt = self.frame.create_text(
            (WINDOW_WIDTH / 2, HEADER_Y_COORD + 40),
            font=GAME_FONT, justify='center', text=prompt)
        self.bar_coords = (
            0, int(WINDOW_HEIGHT), WINDOW_WIDTH, int(WINDOW_HEIGHT))
        self.frame.create_rectangle(self.bar_coords)
        self.frame.create_rectangle(
            (20, 173, 20 + BUTTON_WIDTH, 173 + BUTTON_HEIGHT),
            fill=MENU_BG_COLOR)
        self.draw_text((20 + BUTTON_WIDTH / 2, 190), 'Choose\nbodypart:')
        for number, bodypart in self.player.bodyparts.items():
            x_coord = 20
            y_coord = 220 + BUTTON_HEIGHT * (number - 1)
            button_frame = Frame(
                self.frame, height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
            button_frame.place(x=x_coord, y=y_coord)
            button_frame.propagate(False)
            Radiobutton(
                button_frame, font=GAME_FONT,
                cursor='circle', indicatoron=0,
                relief=BUTTON_LOOK, text=bodypart,
                variable=self.chosen_bodypart,
                value=bodypart).pack(expand=True, fill='both')
        self.action_button = self.draw_button(
            self.bar_coords, 'left', 'CONFIRM', commands[0])


    def update_action_display(self, commands):
        prompt = DEFEND_PROMPT if self.ai_turn else ATTACK_PROMPT
        self.frame.delete(self.prompt)
        self.prompt = self.frame.create_text(
            (WINDOW_WIDTH / 2, HEADER_Y_COORD + 40),
            font=GAME_FONT, justify='center', text=prompt)
        self.action_button = self.draw_button(
            self.bar_coords, 'left', 'CONFIRM', commands[0])


    def draw_endgame_message(self, commands):
        message = LOSE_MESSAGE if self.is_winner_ai else WIN_MESSAGE
        menu_coords = self.get_menu_rectangle_coords(
            ENDGAME_MESSAGE_WIDTH, ENDGAME_MESSAGE_HEIGHT)
        self.draw_menu_rectangle(menu_coords)
        text_x_coord = int(WINDOW_WIDTH / 2)
        text_y_coord = int(menu_coords[1] + PADDING + TEXT_HEIGHT / 2)
        self.draw_text((text_x_coord, text_y_coord), message)
        self.draw_button(menu_coords, 'centre', 'OK', commands[0])

    # ===== SAVE/LOAD GAME MENU =====

    def draw_one_slot(self, item, item_num, start_y_coord):
        if item['level']:
            text = f'{item["number"]}. {item["name"]}, {item["level"]} LVL'
        else:
            text = f'{item["number"]}. {item["name"]}'
        item_offset = int(item_num * (SLOT_HEIGHT + BUTTON_SPACING))
        x_coord = int(WINDOW_WIDTH / 2 - SLOT_WIDTH / 2)
        y_coord = item_offset + start_y_coord - int(SLOT_HEIGHT / 2) - 2
        button_frame = Frame(self.frame, height=SLOT_HEIGHT, width=SLOT_WIDTH)
        button_frame.place(x=x_coord, y=y_coord)
        button_frame.propagate(False)
        Radiobutton(
            button_frame, font=GAME_FONT, cursor='circle', indicatoron=0,
            relief=BUTTON_LOOK, text=text, variable=self.chosen_slot,
            value=item['number']).pack(expand=True, fill='both')


    def draw_save_slots(self, slots):
        self.chosen_slot = StringVar()
        start_y_coord = SLOT_MENU_Y_START + PADDING + int(SLOT_HEIGHT / 2)
        for number, item in enumerate(slots):
            self.draw_one_slot(item, number, start_y_coord)


    def draw_slots_menu(self, commands, load=False):
        menu_coords = self.get_menu_rectangle_coords(
            SLOT_MENU_WIDTH, SLOT_MENU_HEIGHT)
        self.draw_menu_rectangle(menu_coords)
        left_button_x_coord = SLOT_MENU_X_START + PADDING
        left_button_y_coord = SLOT_MENU_Y_END - BUTTON_HEIGHT - PADDING
        center_button_x_coord = WINDOW_WIDTH / 2 - int(BUTTON_WIDTH / 2)
        center_button_y_coord = SLOT_MENU_Y_END - BUTTON_HEIGHT - PADDING
        right_button_x_coord = SLOT_MENU_X_END - BUTTON_WIDTH - PADDING
        right_button_y_coord = left_button_y_coord
        self.draw_button(menu_coords, 'left', 'BACK', commands[0])
        if load:
            self.draw_button(menu_coords, 'right', 'LOAD', commands[1])
        else:
            self.draw_button(menu_coords, 'centre', 'DELETE', commands[1])
            self.draw_button(menu_coords, 'right', 'SAVE', commands[2])

    # ===== VIEW CHARACTER MENU =====

    def draw_character_menu(self, player, commands):
        menu_coords = self.get_menu_rectangle_coords(
            CHAR_MENU_WIDTH, CHAR_MENU_HEIGHT)
        self.draw_menu_rectangle(menu_coords)
        self.draw_text((STATS_X_COORD, STATS_Y_COORD), player)
        self.draw_button(menu_coords, 'centre', 'BACK', commands[0])
        self.frame.create_rectangle(
            (CHAR_X_COORD - 150, CHAR_Y_COORD - 100,
             CHAR_X_COORD + 50, CHAR_Y_COORD + 100),
            fill=CHAR_BG_COLOR, width=2)
        self.player = player
        self.player.load_player_sprite(self.frame)
        self.player.current_animation_id = self.player.root.after(
            0, self.player.run_idle_animation, 0, self.player.idle_anim)
        self.player.set_coordinates(CHAR_X_COORD, CHAR_Y_COORD)
