from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.uix.screenmanager import FadeTransition
from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.uix.behaviors import ScaleBehavior, CommonElevationBehavior, RotateBehavior
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSlideTransition
import json
import re
import random
from functools import partial
from boardblitz_helpers import boardblitz_avatars, coordinates, start_boxes, corners, players_color
from boardblitz_helpers import next_dice as nd
from cuvinte import words

Window.size = (400, 780)
Window.top = 30
Window.left = 1000

user_logged_in = None
nickname_user_logged_in = None
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

next_dice = nd

dice_clicked = {
    1: False,
    2: False,
    3: False,
    4: False,
}

aliens_state = {
    "red_alien_1": 0,
    "red_alien_2": 0,
    "red_alien_3": 0,
    "red_alien_4": 0,

    "yellow_alien_1": 0,
    "yellow_alien_2": 0,
    "yellow_alien_3": 0,
    "yellow_alien_4": 0,

    "green_alien_1": 0,
    "green_alien_2": 0,
    "green_alien_3": 0,
    "green_alien_4": 0,

    "blue_alien_1": 0,
    "blue_alien_2": 0,
    "blue_alien_3": 0,
    "blue_alien_4": 0
}


def reset_next_dice():
    global next_dice
    next_dice = nd


def reset_aliens_state():
    for alien in aliens_state.keys():
        aliens_state[alien] = 0


class Dice(MDIconButton, RotateBehavior):
    pass


class GameCardBehavior(MDBoxLayout, FocusBehavior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_event_type("on_release")

    def on_release(self, *args):
        args[0].current = args[1]

    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class BoardBlitzStart(MDFloatLayout):
    pass


class BoardBlitzButton(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class HeadSpinButtonSettings(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class HelpUsDecideButtonSettings(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class HeadSpinButtonPlay(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class HelpUsDecideButtonPlay(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class Game(MDBoxLayout):
    pass


class ElevatedBox(CommonElevationBehavior, MDFloatLayout):
    pass


class ScaleLabel(ScaleBehavior, MDLabel):
    pass


class WindowManager(MDScreenManager):
    pass


class HomeScreen(MDScreen):
    pass


class RegisterScreen(MDScreen):
    def switch_password_mode(self):
        if self.ids.password_register.password is True:
            self.ids.password_register.password = False
            self.ids.password_register.icon_right = "lock-open"
        else:
            self.ids.password_register.password = True
            self.ids.password_register.icon_right = "lock"
        self.ids.password_register.focus = True

    def animate_wrong_widget(self, widget):
        animate = Animation(
            duration=0.2,
            line_color_normal=(1, 0, 0, 1),
            hint_text_color_normal=(1, 0, 0, 1),
            icon_right_color_normal=(1, 0, 0, 1),
            text_color_normal=(1, 0, 0, 1)
        ) + Animation(
            duration=0.2,
            line_color_normal=(0, 0, 0, 0.38),
            hint_text_color_normal=(0, 0, 0, 0.38),
            icon_right_color_normal=(0, 0, 0, 0.38),
            text_color_normal=(0, 0, 0, 0.38)
        ) + Animation(
            duration=0.2,
            line_color_normal=(1, 0, 0, 1),
            hint_text_color_normal=(1, 0, 0, 1),
            icon_right_color_normal=(1, 0, 0, 1),
            text_color_normal=(1, 0, 0, 1)
        ) + Animation(
            duration=0.2,
            line_color_normal=(0, 0, 0, 0.38),
            hint_text_color_normal=(0, 0, 0, 0.38),
            icon_right_color_normal=(0, 0, 0, 0.38),
            text_color_normal=(0, 0, 0, 0.38)
        )
        animate.start(widget)

    def create_account(self, screen_manager):
        wrong_input = False
        global email_regex

        if not re.fullmatch(email_regex, self.ids.email_register.text):
            self.animate_wrong_widget(self.ids.email_register)
            wrong_input = True

        if len(self.ids.password_register.text) < 8:
            self.animate_wrong_widget(self.ids.password_register)
            wrong_input = True

        if self.ids.username_register.text == "":
            self.animate_wrong_widget(self.ids.username_register)
            return

        with open("user_accounts.json", 'r+') as accounts_file:
            accounts = json.load(accounts_file)

            for user in accounts["user_accounts"]:
                if user["username"] == self.ids.username_register.text:
                    self.animate_wrong_widget(self.ids.username_register)
                    break
            else:
                if wrong_input is True:
                    return

                new_account = {"username": self.ids.username_register.text,
                               "password": self.ids.password_register.text,
                               "first_name": self.ids.first_name_register.text,
                               "last_name": self.ids.last_name_register.text,
                               "e-mail": self.ids.email_register.text,
                               "nickname": self.ids.nickname_register.text
                               }
                accounts["user_accounts"].append(new_account)
                accounts_file.seek(0)
                json.dump(accounts, accounts_file, indent=4)
                screen_manager.current = 'login'

                with open("headspin_settings.json", 'r+') as headspin_settings_default_file:
                    settings = json.load(headspin_settings_default_file)

                    default_settings = {"username": self.ids.username_register.text,
                                        "round": "4",
                                        "team": "2",
                                        "words": "Kilimanjaro",
                                        "words_per_round": "10",
                                        "players": "John, Linda, William, Andreea"
                                        }
                    settings["headspin_settings"].append(default_settings)
                    headspin_settings_default_file.seek(0)
                    json.dump(settings, headspin_settings_default_file, indent=4)
                    screen_manager.current = 'login'

                with open("helpusdecide_settings.json", 'r+') as helpusdecide_settings_default_file:
                    settings = json.load(helpusdecide_settings_default_file)

                    default_settings = {"username": self.ids.username_register.text,
                                        "options": "Option 1, Option 2",
                                        "players": "John, Linda, William, Andreea"
                                        }
                    settings["helpusdecide_settings"].append(default_settings)
                    helpusdecide_settings_default_file.seek(0)
                    json.dump(settings, helpusdecide_settings_default_file, indent=4)
                    screen_manager.current = 'login'


class LoginScreen(MDScreen):
    def switch_password_mode(self):
        if self.ids.password_login.password is True:
            self.ids.password_login.password = False
            self.ids.password_login.icon_right = "lock-open"
        else:
            self.ids.password_login.password = True
            self.ids.password_login.icon_right = "lock"
        self.ids.password_login.focus = True

    def login(self, screen_manager):
        with open("user_accounts.json", 'r+') as accounts_file:
            accounts = json.load(accounts_file)

            for user in accounts["user_accounts"]:
                if user["username"] == self.ids.username_login.text \
                        and user["password"] == self.ids.password_login.text:
                    global user_logged_in, nickname_user_logged_in
                    user_logged_in = user["username"]
                    nickname_user_logged_in = user["nickname"]
                    screen_manager.current = "home"
                    break
            else:
                self.animate_wrong_account()

    def animate_wrong_account(self):
        animate = Animation(
            duration=0.2,
            line_color_normal=(1, 0, 0, 1),
            hint_text_color_normal=(1, 0, 0, 1),
            icon_right_color_normal=(1, 0, 0, 1),
            text_color_normal=(1, 0, 0, 1)
        )+Animation(
            duration=0.2,
            line_color_normal=(0, 0, 0, 0.38),
            hint_text_color_normal=(0, 0, 0, 0.38),
            icon_right_color_normal=(0, 0, 0, 0.38),
            text_color_normal=(0, 0, 0, 0.38)
        )+Animation(
            duration=0.2,
            line_color_normal=(1, 0, 0, 1),
            hint_text_color_normal=(1, 0, 0, 1),
            icon_right_color_normal=(1, 0, 0, 1),
            text_color_normal=(1, 0, 0, 1)
        )+Animation(
            duration=0.2,
            line_color_normal=(0, 0, 0, 0.38),
            hint_text_color_normal=(0, 0, 0, 0.38),
            icon_right_color_normal=(0, 0, 0, 0.38),
            text_color_normal=(0, 0, 0, 0.38)
        )
        animate.start(self.ids.password_login)
        animate.start(self.ids.username_login)


class WelcomeScreen(MDScreen):
    def change_transition(self, screen_manager):
        screen_manager.transition = MDSlideTransition()

    def change_transition_for_welcome(self, screen_manager):
        screen_manager.transition = FadeTransition()


class BoardBlitzScreen(MDScreen):
    def go_back(self, screen_manager):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "home"


class BoardBlitzGame(MDScreen):
    pass


class HeadSpinScreen(MDScreen):
    def go_back(self, screen_manager):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "home"

    def play_game(self, screen_manager):
        screen_manager.current = "headspinPlay"


class HeadSpinSettings(MDFloatLayout):
    pass


class HelpUsDecideSettings(MDFloatLayout):
    pass


class HeadSpinRules(MDFloatLayout):
    pass


class HelpUsDecideRules(MDFloatLayout):
    pass


class HeadSpinPlay(MDScreen):
    def exit_game(self, screen_manager):
        screen_manager.current = "headspin"

    rounds_headspin = None
    teams_headspin = None
    final_words = None
    words_per_round = None
    player_teams = None
    headspin_score = None
    index_echipa = -1
    words_per_team = None
    index_round = 1

    def headspin_play(self):
        with open("headspin_settings.json", 'r+') as headspin_files:
            settings = json.load(headspin_files)

            for setting in settings["headspin_settings"]:
                if setting["username"] == user_logged_in:
                    HeadSpinPlay.rounds_headspin = int(setting["round"])
                    HeadSpinPlay.teams_headspin = int(setting["team"])
                    words_headspin = setting["words"].split(",")
                    HeadSpinPlay.words_per_round = int(setting["words_per_round"])
                    players_headspin = setting["players"].split(",")
                    break

        players = []
        for person in players_headspin:
            new_person = person.strip()
            players.append(new_person)

        HeadSpinPlay.player_teams = []
        while len(players) > 0:
            first_player = random.choice(players)
            players.remove(first_player)
            second_player = random.choice(players)
            players.remove(second_player)
            HeadSpinPlay.player_teams.append((first_player, second_player))

        HeadSpinPlay.final_words = words
        for word in words_headspin:
            new_word = word.strip()
            HeadSpinPlay.final_words.append(str(new_word))

        print(HeadSpinPlay.final_words)
        print(HeadSpinPlay.player_teams)
        print(HeadSpinPlay.rounds_headspin)
        print(HeadSpinPlay.teams_headspin)
        print(HeadSpinPlay.words_per_round)

        HeadSpinPlay.headspin_score = {}
        for team in HeadSpinPlay.player_teams:
            team_name = str(team[0] + " & " + team[1])
            HeadSpinPlay.headspin_score[team_name] = 0

        print(HeadSpinPlay.headspin_score)

    def initialize(self):
        HeadSpinPlay.index_round = 1
        new_word = random.choice(HeadSpinPlay.final_words)
        HeadSpinPlay.final_words.remove(new_word)
        self.ids.word_to_guess.text = new_word

    def change_team(self):
        self.ids.check_button.disabled = False
        self.ids.pass_button.disabled = False
        if HeadSpinPlay.index_echipa == int(HeadSpinPlay.teams_headspin) - 1:
            HeadSpinPlay.index_echipa = 0
            new_team_name = list(HeadSpinPlay.headspin_score.keys())[0]
        else:
            HeadSpinPlay.index_echipa += 1
            new_team_name = list(HeadSpinPlay.headspin_score.keys())[int(HeadSpinPlay.index_echipa)]
        HeadSpinPlay.words_per_team = HeadSpinPlay.words_per_round
        print(HeadSpinPlay.index_echipa)
        print(HeadSpinPlay.index_round)
        self.ids.team_name.text = new_team_name
        self.ids.words_per_team_id.text = "Words: " + str(HeadSpinPlay.words_per_round)

    def check_pressed(self):
        if HeadSpinPlay.words_per_team != 0:
            self.change_word()
            current_team = self.ids.team_name.text
            HeadSpinPlay.headspin_score[current_team] += 1
            print(HeadSpinPlay.headspin_score)
        else:
            self.ids.check_button.disabled = True
            self.ids.pass_button.disabled = True

    def change_word(self):
        if HeadSpinPlay.words_per_team != 0:
            new_word = random.choice(HeadSpinPlay.final_words)
            HeadSpinPlay.final_words.remove(new_word)
            HeadSpinPlay.words_per_team -= 1
            self.ids.words_per_team_id.text = "Words: " + str(HeadSpinPlay.words_per_team)
            self.ids.word_to_guess.text = new_word
            if HeadSpinPlay.words_per_team == 0:
                self.ids.check_button.disabled = True
                self.ids.pass_button.disabled = True

    def pass_pressed(self):
        if HeadSpinPlay.words_per_team != 0:
            self.change_word()
            print(HeadSpinPlay.headspin_score)
        else:
            self.ids.pass_button.disabled = True
            self.ids.check_button.disabled = True

    def round_change(self):
        if HeadSpinPlay.index_echipa == int(HeadSpinPlay.teams_headspin) - 1:
            if HeadSpinPlay.index_round != int(HeadSpinPlay.rounds_headspin):
                HeadSpinPlay.index_round += 1
                self.ids.round_number.text = str(HeadSpinPlay.index_round)
            else:
                self.ids.next_round_button.disabled = True

    def end_next_team(self):
        self.ids.next_round_button.disabled = True


class HelpUsDecidePlay(MDScreen):
    def exit_game(self, screen_manager):
        screen_manager.current = "helpusdecide"


class WordRushScreen(MDScreen):
    pass


class TicTacToeScreen(MDScreen):
    pass


class HelpUsDecideScreen(MDScreen):
    def go_back(self, screen_manager):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "home"

    def play_game(self, screen_manager):
        screen_manager.current = "helpusdecidePlay"


class GameRulesInformation(MDFloatLayout):
    pass


class AccountInformation(MDFloatLayout):
    pass


class RankingInformation(MDFloatLayout):
    pass


class GameInformation(MDFloatLayout):
    pass


class PartyPlaytime(MDApp):
    account_dialog = None
    headspin_dialog = None
    helpusdecide_dialog = None
    headspin_rules_dialog = None
    helpusdecide_rules_dialog = None
    information_dialog = None
    boardblitz_rules = None
    boardblitz_start = None
    boardblitz_exit_game = None
    player_chosen_to_start_boardblitz = False
    current_player_boardblitz = None
    number_of_players_boardblitz = None
    boardblitz_miscellaneous = []
    boardblitz_finish_aliens = {"red": 0, "green": 0, "blue": 0, "yellow": 0}
    number_of_players_finished = 0
    boardblitz_ranking = {"red": 0, "green": 0, "blue": 0, "yellow": 0}
    boardblitz_ranking_dialog = None
    headspin_exit_game = None
    helpusdecide_exit_game = None
    player_button_selected = "players_button_2"

    def build(self):
        return Builder.load_file('party.kv')

    def account_info(self):
        if not self.account_dialog:
            self.account_dialog = MDDialog(
                type="custom",
                content_cls=AccountInformation(),
            )

        with open("user_accounts.json", 'r+') as accounts_file:
            accounts = json.load(accounts_file)

            for user in accounts["user_accounts"]:
                if user["username"] == user_logged_in:
                    self.account_dialog.content_cls.ids.first_name_information.text = user["first_name"]
                    self.account_dialog.content_cls.ids.last_name_information.text = user["last_name"]
                    self.account_dialog.content_cls.ids.email_information.text = user["e-mail"]
                    self.account_dialog.content_cls.ids.nickname_information.text = user["nickname"]
                    break

        self.account_dialog.open()

    def headspin_settings(self):
        if not self.headspin_dialog:
            self.headspin_dialog = MDDialog(
                type="custom",
                content_cls=HeadSpinSettings(),
            )

        with open("headspin_settings.json", 'r+') as headspin_files:
            settings = json.load(headspin_files)

            for setting in settings["headspin_settings"]:
                if setting["username"] == user_logged_in:
                    self.headspin_dialog.content_cls.ids.round_information.text = setting["round"]
                    self.headspin_dialog.content_cls.ids.team_information.text = setting["team"]
                    self.headspin_dialog.content_cls.ids.words_information.text = setting["words"]
                    self.headspin_dialog.content_cls.ids.words_per_round_information.text = setting["words_per_round"]
                    self.headspin_dialog.content_cls.ids.players_information.text = setting["players"]
                    break

        self.headspin_dialog.open()

    def helpusdecide_settings(self):
        if not self.helpusdecide_dialog:
            self.helpusdecide_dialog = MDDialog(
                type="custom",
                content_cls=HelpUsDecideSettings(),
            )

        with open("helpusdecide_settings.json", 'r+') as helpusdecide_files:
            settings = json.load(helpusdecide_files)

            for setting in settings["helpusdecide_settings"]:
                if setting["username"] == user_logged_in:
                    self.helpusdecide_dialog.content_cls.ids.options_information.text = setting["options"]
                    self.helpusdecide_dialog.content_cls.ids.players_information.text = setting["players"]
                    break

        self.helpusdecide_dialog.open()

    def headspin_settings_exit(self):
        self.headspin_dialog.dismiss()

    def helpusdecide_settings_exit(self):
        self.helpusdecide_dialog.dismiss()

    def headspin_save_settings(self):
        nicknames = self.headspin_dialog.content_cls.ids.players_information.text.split(',')
        number = int(self.headspin_dialog.content_cls.ids.team_information.text)

        if len(nicknames) != number * 2:
            self.animate_wrong_widget(self.headspin_dialog.content_cls.ids.players_information)
        else:
            with open("headspin_settings.json", 'r+') as headspin_settings:
                settings = json.load(headspin_settings)

                for setting in settings["headspin_settings"]:
                    if setting["username"] == user_logged_in:
                        setting["round"] = self.headspin_dialog.content_cls.ids.round_information.text
                        setting["team"] = self.headspin_dialog.content_cls.ids.team_information.text
                        setting["words_per_round"] = self.headspin_dialog.content_cls.ids.words_per_round_information.text
                        setting["words"] = self.headspin_dialog.content_cls.ids.words_information.text
                        setting["players"] = self.headspin_dialog.content_cls.ids.players_information.text

                        headspin_settings.seek(0)
                        json.dump(settings, headspin_settings, indent=4)
                        headspin_settings.truncate()
                        self.headspin_dialog.dismiss()
                        return

    def helpusdecide_save_settings(self):
        with open("helpusdecide_settings.json", 'r+') as helpusdecide_settings:
            settings = json.load(helpusdecide_settings)

            for setting in settings["helpusdecide_settings"]:
                if setting["username"] == user_logged_in:
                    setting["options"] = self.helpusdecide_dialog.content_cls.ids.options_information.text
                    setting["players"] = self.helpusdecide_dialog.content_cls.ids.players_information.text

                    helpusdecide_settings.seek(0)
                    json.dump(settings, helpusdecide_settings, indent=4)
                    helpusdecide_settings.truncate()
                    self.helpusdecide_dialog.dismiss()
                    return

    def headspin_rules(self):
        if not self.headspin_rules_dialog:
            self.headspin_rules_dialog = MDDialog(
                type='custom',
                content_cls=HeadSpinRules()
            )
        self.headspin_rules_dialog.open()

    def helpusdecide_rules(self):
        if not self.helpusdecide_rules_dialog:
            self.helpusdecide_rules_dialog = MDDialog(
                type='custom',
                content_cls=HelpUsDecideRules()
            )
        self.helpusdecide_rules_dialog.open()

    def exit_headspin_rules(self):
        self.headspin_rules_dialog.dismiss()

    def exit_helpusdecide_rules(self):
        self.helpusdecide_rules_dialog.dismiss()

    def exit_headspin_game(self):
        if not self.headspin_exit_game:
            self.headspin_exit_game = MDDialog(
                title="Do you want to exit this game?",
                buttons=[
                    MDFlatButton(
                        text="NO",
                        on_release=self.dismiss_headspin_game
                    ),
                    MDFlatButton(
                        text="YES",
                        on_release=self.exit_current_headspin_game
                    ),
                ]
            )

        self.headspin_exit_game.open()

    def exit_helpusdecide_game(self):
        if not self.helpusdecide_exit_game:
            self.helpusdecide_exit_game = MDDialog(
                title="Do you want to leave this poll?",
                buttons=[
                    MDFlatButton(
                        text="NO",
                        on_release=self.dismiss_helpusdecide_game
                    ),
                    MDFlatButton(
                        text="YES",
                        on_release=self.exit_current_helpusdecide_game
                    ),
                ]
            )

        self.helpusdecide_exit_game.open()

    def dismiss_headspin_game(self, *args):
        self.headspin_exit_game.dismiss()

    def dismiss_helpusdecide_game(self, *args):
        self.helpusdecide_exit_game.dismiss()

    def exit_current_headspin_game(self, *args):
        self.headspin_exit_game.dismiss()
        self.root.current = 'headspin'

    def exit_current_helpusdecide_game(self, *args):
        self.helpusdecide_exit_game.dismiss()
        self.root.current = 'helpusdecide'

    def exit_dialogue(self):
        self.account_dialog.dismiss()

    def game_information(self):
        if not self.information_dialog:
            self.information_dialog = MDDialog(
                type='custom',
                content_cls=GameInformation()
            )

        self.information_dialog.open()

    def exit_game_information(self):
        self.information_dialog.dismiss()

    def open_rules(self):
        if not self.boardblitz_rules:
            self.boardblitz_rules = MDDialog(
                type="custom",
                content_cls=GameRulesInformation()
            )

        self.boardblitz_rules.open()

    def exit_game_rules(self):
        self.boardblitz_rules.dismiss()

    def boardblitz_players(self, *args):
        if self.boardblitz_ranking_dialog is None:
            self.boardblitz_ranking_dialog = MDDialog(
                type="custom",
                content_cls=RankingInformation(),
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="back",
                        font_name="fonts/LuckiestGuy-Regular.ttf",
                        font_size="30sp",
                        on_release=self.go_home
                    )
                ]
            )
        if args[0] == "start_game":
            forbidden_nickname = False
            for i in range(1, int(PartyPlaytime.player_button_selected[-1])):
                if self.boardblitz_start.content_cls.ids["boardblitz_nickname_" + str(i)].text == "" \
                        or len(self.boardblitz_start.content_cls.ids["boardblitz_nickname_" + str(i)].text) >= 12:
                    forbidden_nickname = True
                    self.animate_wrong_widget(self.boardblitz_start.content_cls.ids["boardblitz_nickname_" + str(i)])

            if not forbidden_nickname:
                self.boardblitz_start.dismiss()

                self.start_boardlitz_game()

                self.root.current = 'boardblitz_game'

        elif args[0] != "choose_names_and_play":
            screen = self.root.get_screen("boardblitz")

            if not self.boardblitz_start:
                self.boardblitz_start = MDDialog(
                    type="custom",
                    content_cls=BoardBlitzStart()
                )

            screen.ids[PartyPlaytime.player_button_selected].md_bg_color = "white"
            screen.ids[PartyPlaytime.player_button_selected].unfocus_color = "white"

            self.boardblitz_start.content_cls.ids[PartyPlaytime.player_button_selected + "_2"].md_bg_color = "white"
            self.boardblitz_start.content_cls.ids[PartyPlaytime.player_button_selected + "_2"].unfocus_color = "white"

            screen.ids[args[1]].md_bg_color = (1, 1, 1, .8)
            screen.ids[args[1]].unfocus_color = (1, 1, 1, .8)

            self.boardblitz_start.content_cls.ids[args[1] + "_2"].md_bg_color = (1, 1, 1, .8)
            self.boardblitz_start.content_cls.ids[args[1] + "_2"].unfocus_color = (1, 1, 1, .8)

            PartyPlaytime.player_button_selected = args[1]

            self.update_nickname_boxes()
        else:
            self.open_boardblitz_start()

    def update_nickname_boxes(self):
        if self.boardblitz_ranking_dialog is None:
            self.boardblitz_ranking_dialog = MDDialog(
                type="custom",
                content_cls=RankingInformation(),
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="back",
                        font_name="fonts/LuckiestGuy-Regular.ttf",
                        font_size="30sp",
                        on_release=self.go_home
                    )
                ]
            )

        if PartyPlaytime.player_button_selected[-1] == '2':
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.pos_hint = {"center_y": .5}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.pos_hint = {"center_y": 3}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.pos_hint = {"center_y": 3}

            self.boardblitz_ranking_dialog.content_cls.ids.ranking_nickname_3.pos_hint = {"center_x": .5,
                                                                                          "center_y": 20.3}
            self.boardblitz_ranking_dialog.content_cls.ids.ranking_nickname_4.pos_hint = {"center_x": .5,
                                                                                          "center_y": 20.1}

        elif PartyPlaytime.player_button_selected[-1] == '3':
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.pos_hint = {"center_y": .6}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.pos_hint = {"center_y": .4}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.pos_hint = {"center_y": 3}

            self.boardblitz_ranking_dialog.content_cls.ids.ranking_nickname_3.pos_hint = {"center_x": .5,
                                                                                          "center_y": .3}
            self.boardblitz_ranking_dialog.content_cls.ids.ranking_nickname_4.pos_hint = {"center_x": .5,
                                                                                          "center_y": 20.1}
        else:
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.pos_hint = {"center_y": .7}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.pos_hint = {"center_y": .5}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.pos_hint = {"center_y": .3}

            self.boardblitz_ranking_dialog.content_cls.ids.ranking_nickname_3.pos_hint = {"center_x": .5,
                                                                                          "center_y": .3}
            self.boardblitz_ranking_dialog.content_cls.ids.ranking_nickname_4.pos_hint = {"center_x": .5,
                                                                                          "center_y": .1}

    def open_boardblitz_start(self):
        if not self.boardblitz_start:
            self.boardblitz_start = MDDialog(
                type="custom",
                content_cls=BoardBlitzStart()
            )

        self.boardblitz_start.open()

    def exit_boardblitz_start(self):

        self.boardblitz_start.dismiss()

    def exit_boardblitz_game(self):
        if not self.boardblitz_exit_game:
            self.boardblitz_exit_game = MDDialog(
                title="Do you want to exit this game?",
                buttons=[
                    MDFlatButton(
                        text="NO",
                        on_release=self.dismiss_boardblitz_game
                    ),
                    MDFlatButton(
                        text="YES",
                        on_release=self.exit_current_boardblitz_game
                    ),
                ]
            )

        self.boardblitz_exit_game.open()

    def dismiss_boardblitz_game(self, *args):
        self.boardblitz_exit_game.dismiss()

    def choose_avatars_for_boardblitz(self):
        avatars = []

        while len(avatars) < 4:
            chosen_avatar = random.randint(0, 7)

            while chosen_avatar in avatars:
                chosen_avatar = random.randint(0, 7)

            avatars.append(chosen_avatar)

        return avatars

    def send_away_aliens(self, screen, colors):
        for color in colors:
            for alien_number in "1234":
                screen.ids[color + "_alien_" + alien_number].pos = (dp(1000), dp(1000))

    def bring_in_aliens(self, screen, colors):
        for color in colors:
            for alien_number in "1234":
                current_alien = color + "_alien_" + alien_number
                screen.ids[current_alien].pos = (dp(coordinates[current_alien]["width"]), dp(coordinates[current_alien]["height"]))

    def blockage(self, alien, color, dice_rolled):
        starting_point = {
            "red": 7, "green": 20, "yellow": 33, "blue": 46
        }

        blocking_aliens = 0

        if aliens_state[alien] == 0:
            for blocking_alien in aliens_state:
                if not blocking_alien.startswith(color):
                    if aliens_state[blocking_alien] == starting_point[color]:
                        blocking_aliens += 1
        elif aliens_state[alien] > 0:
            if 53 <= aliens_state[alien] <= 57 and 58 - aliens_state[alien] < dice_rolled:
                return True
            elif 58 <= aliens_state[alien] <= 62 and 63 - aliens_state[alien] < dice_rolled:
                return True
            elif 63 <= aliens_state[alien] <= 67 and 68 - aliens_state[alien] < dice_rolled:
                return True
            elif 68 <= aliens_state[alien] <= 72 and 73 - aliens_state[alien] < dice_rolled:
                return True
            elif color == "red" and 46 <= aliens_state[alien] <= 51 and aliens_state[alien] + dice_rolled >= 52:
                return False
            elif color == "green" and 7 <= aliens_state[alien] <= 12 and aliens_state[alien] + dice_rolled >= 13:
                return False
            elif color == "yellow" and 20 <= aliens_state[alien] <= 25 and aliens_state[alien] + dice_rolled >= 26:
                return False
            elif color == "blue" and 33 <= aliens_state[alien] <= 38 and aliens_state[alien] + dice_rolled >= 39:
                return False
            else:
                for blocking_alien in aliens_state:
                    if not blocking_alien.startswith(color):
                        if aliens_state[blocking_alien] == aliens_state[alien] + dice_rolled:
                            blocking_aliens += 1

        return True if blocking_aliens >= 2 else False

    def find_alien_moves(self, turn, dice_rolled):
        alien_moves = []
        player_turn = ["red", "blue", "green", "yellow"]

        alien_color = player_turn[turn - 1]

        for i in "1234":
            current_alien = alien_color + "_alien_" + i

            if aliens_state[current_alien] == 0 and dice_rolled == 6 and self.blockage(current_alien, alien_color, dice_rolled) == False:
                alien_moves.append(current_alien)
            elif aliens_state[current_alien] > 0 and self.blockage(current_alien, alien_color, dice_rolled) == False:
                alien_moves.append(current_alien)

        return alien_moves

    def go_to_next_turn(self, dice, next_player_dice, dice_number, dice_rolled, *args):
        PartyPlaytime.boardblitz_miscellaneous = []

        if dice_rolled != 6:

            disappear_animation = Animation(
                duration=0.2,
                opacity=0
            )

            appear_animation = Animation(
                duration=0.2,
                opacity=1
            )
            disappear_animation.start(dice)
            appear_animation.start(next_player_dice)
        dice_clicked[dice_number] = False

    def go_home(self, *args):
        self.boardblitz_ranking_dialog.dismiss()
        self.reset_boardblitz()
        self.root.current = 'boardblitz'

    def end_game(self):
        if not self.boardblitz_ranking_dialog:
            self.boardblitz_ranking_dialog = MDDialog(
                type="custom",
                content_cls=RankingInformation(),
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="back",
                        font_name="fonts/LuckiestGuy-Regular.ttf",
                        font_size="30sp",
                        on_release=self.go_home
                    )
                ]
            )

        players = {
            "blue": "boardblitz_nickname_1",
            "green": "boardblitz_nickname_2",
            "yellow": "boardblitz_nickname_3"
        }

        if PartyPlaytime.number_of_players_boardblitz == 3:
            PartyPlaytime.boardblitz_ranking.pop("yellow")
        elif PartyPlaytime.number_of_players_boardblitz == 2:
            PartyPlaytime.boardblitz_ranking.pop("yellow")
            PartyPlaytime.boardblitz_ranking.pop("green")

        for color in PartyPlaytime.boardblitz_ranking.items():
            player_nickname = nickname_user_logged_in \
                if color[0] == "red" \
                else self.boardblitz_start.content_cls.ids[players[color[0]]].text

            place = str(color[1]) if color[1] != 0 else str(PartyPlaytime.number_of_players_boardblitz)

            self.boardblitz_ranking_dialog.content_cls.ids["ranking_nickname_" + place].text = \
                "#" + place + " " + player_nickname

        self.boardblitz_ranking_dialog.open()

    def alien_is_pressed(self, alien_id):
        screen = self.root.get_screen("boardblitz_game")

        alien_moves = PartyPlaytime.boardblitz_miscellaneous[4]
        normal_color = PartyPlaytime.boardblitz_miscellaneous[3]
        dice_rolled = PartyPlaytime.boardblitz_miscellaneous[5]

        color_name = alien_id.split('_')[0]

        for alien in alien_moves:
            screen.ids[alien].disabled = True
            screen.ids[alien].icon_color = normal_color

        if aliens_state[alien_id] == 0:
            start_box = coordinates[start_boxes[alien_id]]
            box_number = start_boxes[alien_id].split('_')[1]
            first_corner = "box_" + str(int(box_number) + 4)
            second_corner = "box_" + str(int(box_number) + 5)
            destination = "box_" + str(int(box_number) + 6)

            animation = Animation(
                duration=0.3,
                pos=(dp(start_box["width"]), dp(start_box["height"]))
            ) + Animation(
                duration=0.3,
                pos=(dp(coordinates[first_corner]["width"]), dp(coordinates[first_corner]["height"]))
            ) + Animation(
                duration=0.2,
                pos=(dp(coordinates[second_corner]["width"]), dp(coordinates[second_corner]["height"]))
            ) + Animation(
                duration=0.2,
                pos=(dp(coordinates[destination]["width"]), dp(coordinates[destination]["height"]))
            )

            animation.start(screen.ids[alien_id])
            aliens_state[alien_id] = int(box_number) + 6
            things = PartyPlaytime.boardblitz_miscellaneous
            Clock.schedule_once(partial(self.go_to_next_turn, things[0], things[1], things[2], dice_rolled), 1)
        elif aliens_state[alien_id] >= 53:
            current_box_number = aliens_state[alien_id]
            end = False
            if current_box_number + dice_rolled in [58, 63, 68, 73]:
                destination = alien_id + "_finish"

                PartyPlaytime.boardblitz_finish_aliens[color_name] += 1
                if PartyPlaytime.boardblitz_finish_aliens[color_name] == 4:

                    PartyPlaytime.number_of_players_finished += 1


                    PartyPlaytime.boardblitz_ranking[color_name] = PartyPlaytime.number_of_players_finished

                    if PartyPlaytime.number_of_players_boardblitz - PartyPlaytime.number_of_players_finished >= 2:
                        players = PartyPlaytime.number_of_players_boardblitz
                        next_dice[players] = {
                            i: next_dice[players][i]
                            if next_dice[players][i] != players_color[color_name]
                            else next_dice[players][next_dice[players][i]]
                            for i in next_dice[players].keys()
                        }

                        next_dice[players].pop(players_color[color_name])

                    if PartyPlaytime.number_of_players_finished + 1 == PartyPlaytime.number_of_players_boardblitz:
                        end = True
            else:
                destination = "box_" + str(current_box_number + dice_rolled)

            animation = Animation(
                duration=0.2,
                pos=(dp(coordinates[destination]["width"]),
                     dp(coordinates[destination]["height"])),
                icon_size=sp(22)
            ) if destination.endswith("finish") else Animation(
                duration=0.2,
                pos=(dp(coordinates[destination]["width"]),
                     dp(coordinates[destination]["height"])),
            )

            animation.start(screen.ids[alien_id])

            if end:
                self.end_game()
            else:
                aliens_state[alien_id] = -1 if destination.endswith("finish") else int(destination.split('_')[-1])
                things = PartyPlaytime.boardblitz_miscellaneous
                Clock.schedule_once(partial(self.go_to_next_turn, things[0], things[1], things[2], dice_rolled), 0.2)
        else:
            offset = {"red": 1, "blue": 29, "green": 45, "yellow": 37}
            current_box_number = aliens_state[alien_id]
            finish = False
            end = False

            corners_to_surpass = [
                i for i in range(current_box_number, current_box_number + dice_rolled + 1) if i in corners
            ]

            number = current_box_number + dice_rolled
            if current_box_number + dice_rolled > 52:
                destination_number = (current_box_number + dice_rolled) % 52
            else:
                destination_number = current_box_number + dice_rolled

            if (color_name == "red" and current_box_number + dice_rolled > 51) or \
                (color_name == "blue" and current_box_number + dice_rolled > 38 and 33 <= current_box_number <= 38) or \
                (color_name == "green" and current_box_number + dice_rolled > 12 and 7 <= current_box_number <= 12) or\
                (color_name == "yellow" and current_box_number + dice_rolled > 25 and 20 <= current_box_number <= 25):

                if dice_rolled == 6 and current_box_number in [12, 25, 38, 51]:
                    finish = True

                    PartyPlaytime.boardblitz_finish_aliens[color_name] += 1
                    if PartyPlaytime.boardblitz_finish_aliens[color_name] == 4:

                        PartyPlaytime.number_of_players_finished += 1

                        PartyPlaytime.boardblitz_ranking[color_name] = PartyPlaytime.number_of_players_finished

                        if PartyPlaytime.number_of_players_boardblitz - PartyPlaytime.number_of_players_finished >= 2:
                            players = PartyPlaytime.number_of_players_boardblitz
                            next_dice[players] = {
                                i: next_dice[players][i]
                                if next_dice[players][i] != players_color[color_name]
                                else next_dice[players][next_dice[players][i]]
                                for i in next_dice[players].keys()
                            }

                            next_dice[players].pop(players_color[color_name])

                        if PartyPlaytime.number_of_players_finished + 1 == PartyPlaytime.number_of_players_boardblitz:
                            end = True

                destination_number = number + offset[color_name]
                corners_to_surpass = [current_box_number] if current_box_number in [12, 25, 38, 51] else corners_to_surpass[:-1] + [corners_to_surpass[-1] - 1]

            if not finish:

                animation = Animation(duration=0)
                duration = 0

                for i in range(len(corners_to_surpass)):
                    animation += Animation(
                        duration=0.2,
                        pos=(dp(coordinates["box_" + str(corners_to_surpass[i])]["width"]),
                             dp(coordinates["box_" + str(corners_to_surpass[i])]["height"]))
                    )
                    duration += 0.2

                if len(corners_to_surpass) == 0 or current_box_number + dice_rolled != corners_to_surpass[-1]:
                    animation += Animation(
                        duration=0.2,
                        pos=(dp(coordinates["box_" + str(destination_number)]["width"]),
                             dp(coordinates["box_" + str(destination_number)]["height"]))
                    )
                    duration += 0.2

                animation.start(screen.ids[alien_id])
                aliens_state[alien_id] = destination_number
                things = PartyPlaytime.boardblitz_miscellaneous
                Clock.schedule_once(partial(self.go_to_next_turn, things[0], things[1], things[2], dice_rolled), duration)
            else:
                animation = Animation(
                    duration=0.2,
                    pos=(dp(coordinates[alien_id + "_finish"]["width"]),
                         dp(coordinates[alien_id + "_finish"]["height"])),
                    icon_size=sp(22)
                )
                animation.start(screen.ids[alien_id])

                if end:
                    self.end_game()
                else:
                    aliens_state[alien_id] = -1
                    things = PartyPlaytime.boardblitz_miscellaneous
                    Clock.schedule_once(partial(self.go_to_next_turn, things[0], things[1], things[2], dice_rolled), 0.2)

    def animate_dice(self, dice, dice_number):
        if dice.opacity == 0 or dice_clicked[dice_number]:
            return
        dice_clicked[dice_number] = True

        def rotate_back_dice(dt):
            nonlocal dice, dice_number
            screen = self.root.get_screen("boardblitz_game")
            next_player_dice = screen.ids["dice_player_" + str(next_dice[PartyPlaytime.number_of_players_boardblitz][dice_number])]

            dice.rotate_value_angle = 0

            dice_rolled = random.randint(1, 6)
            if random.randint(2,4) == 3:
                dice_rolled = 6

            dice.icon = "dice-" + str(dice_rolled)
            next_player_dice.icon = dice.icon

            alien_moves = self.find_alien_moves(dice_number, dice_rolled)

            if len(alien_moves) != 0:
                normal_color = screen.ids[alien_moves[0]].icon_color

                PartyPlaytime.boardblitz_miscellaneous = [
                    dice,
                    next_player_dice,
                    dice_number,
                    normal_color,
                    alien_moves,
                    dice_rolled
                ]

                for alien in alien_moves:
                    screen.ids[alien].disabled = False
                    screen.ids[alien].icon_color = "black"
            else:
                if dice_rolled == 6:
                    dice_clicked[dice_number] = False
                else:
                    self.go_to_next_turn(dice, next_player_dice, dice_number, dice_rolled)

        animation = Animation(
            duration=0.4,
            rotate_value_angle=360
        )
        animation.start(dice)
        Clock.schedule_once(rotate_back_dice, 0.5)

    def start_boardlitz_game(self):
        boardblitz_game_screen = self.root.get_screen("boardblitz_game")
        PartyPlaytime.number_of_players_boardblitz = int(PartyPlaytime.player_button_selected[-1])

        boardblitz_game_screen.ids.first_player_nickname.text = nickname_user_logged_in
        boardblitz_game_screen.ids.second_player_nickname.text = self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.text
        nickname_2_length = 10 * len(self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.text)
        boardblitz_game_screen.ids.second_player_nickname.width = str(nickname_2_length) + "dp"

        chosen_avatar_list = self.choose_avatars_for_boardblitz()

        boardblitz_game_screen.ids.first_player_avatar.source = boardblitz_avatars[chosen_avatar_list[0]]
        boardblitz_game_screen.ids.second_player_avatar.source = boardblitz_avatars[chosen_avatar_list[1]]

        if PartyPlaytime.player_button_selected[-1] == '2':
            boardblitz_game_screen.ids.third_avatar_box.pos_hint = {"center_y": 3, "center_x": .2}
            boardblitz_game_screen.ids.fourth_avatar_box.pos_hint = {"center_y": 3, "right": 1}

            self.send_away_aliens(boardblitz_game_screen, ["green", "yellow"])
            self.bring_in_aliens(boardblitz_game_screen, ["red", "blue"])

        elif PartyPlaytime.player_button_selected[-1] == '3':
            boardblitz_game_screen.ids.third_avatar_box.pos_hint = {"center_y": .77, "center_x": .2}
            boardblitz_game_screen.ids.fourth_avatar_box.pos_hint = {"center_y": 3, "right": 1}

            boardblitz_game_screen.ids.third_player_nickname.text = self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.text

            boardblitz_game_screen.ids.third_player_avatar.source = boardblitz_avatars[chosen_avatar_list[2]]

            self.send_away_aliens(boardblitz_game_screen, ["yellow"])
            self.bring_in_aliens(boardblitz_game_screen, ["green", "red", "blue"])

        else:
            boardblitz_game_screen.ids.third_avatar_box.pos_hint = {"center_y": .77, "center_x": .2}
            boardblitz_game_screen.ids.fourth_avatar_box.pos_hint = {"center_y": .77, "right": 1}

            boardblitz_game_screen.ids.third_player_nickname.text = self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.text

            boardblitz_game_screen.ids.fourth_player_nickname.text = self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.text
            nickname_4_length = 10 * len(self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.text)
            boardblitz_game_screen.ids.fourth_player_nickname.width = str(nickname_4_length) + "dp"

            boardblitz_game_screen.ids.third_player_avatar.source = boardblitz_avatars[chosen_avatar_list[2]]
            boardblitz_game_screen.ids.fourth_player_avatar.source = boardblitz_avatars[chosen_avatar_list[3]]

            self.bring_in_aliens(boardblitz_game_screen, ["green", "yellow", "red", "blue"])

    def reset_dice(self):
        boardblitz_game_screen = self.root.get_screen("boardblitz_game")
        boardblitz_game_screen.ids.dice_player_1.opacity = 1

        for i in "234":
            boardblitz_game_screen.ids["dice_player_" + i].opacity = 0

        for i in range(1, 5):
            dice_clicked[i] = False

    def reset_alien_size(self):
        screen = self.root.get_screen("boardblitz_game")
        for color in ["red", "blue", "green", "yellow"]:
            for alien_number in "1234":
                current_alien = color + "_alien_" + alien_number
                screen.ids[current_alien].icon_size = "30sp"

    def reset_ranking(self):
        PartyPlaytime.boardblitz_finish_aliens = {"red": 0, "green": 0, "blue": 0, "yellow": 0}
        PartyPlaytime.number_of_players_finished = 0
        PartyPlaytime.boardblitz_ranking = {"red": 0, "green": 0, "blue": 0, "yellow": 0}

    def reset_boardblitz(self):
        PartyPlaytime.player_chosen_to_start_boardblitz = False
        PartyPlaytime.current_player_boardblitz = None
        PartyPlaytime.number_of_players_boardblitz = None
        self.reset_dice()
        reset_aliens_state()
        reset_next_dice()
        PartyPlaytime.boardblitz_miscellaneous = []
        self.reset_alien_size()
        self.reset_ranking()

    def exit_current_boardblitz_game(self, *args):
        self.boardblitz_exit_game.dismiss()

        self.reset_boardblitz()

        self.root.current = 'boardblitz'

    def animate_wrong_widget(self, widget):
        animate = Animation(
            duration=0.2,
            line_color_normal=(1, 0, 0, 1),
            hint_text_color_normal=(1, 0, 0, 1),
            icon_right_color_normal=(1, 0, 0, 1),
            text_color_normal=(1, 0, 0, 1)
        ) + Animation(
            duration=0.2,
            line_color_normal=(0, 0, 0, 0.38),
            hint_text_color_normal=(0, 0, 0, 0.38),
            icon_right_color_normal=(0, 0, 0, 0.38),
            text_color_normal=(0, 0, 0, 0.38)
        ) + Animation(
            duration=0.2,
            line_color_normal=(1, 0, 0, 1),
            hint_text_color_normal=(1, 0, 0, 1),
            icon_right_color_normal=(1, 0, 0, 1),
            text_color_normal=(1, 0, 0, 1)
        ) + Animation(
            duration=0.2,
            line_color_normal=(0, 0, 0, 0.38),
            hint_text_color_normal=(0, 0, 0, 0.38),
            icon_right_color_normal=(0, 0, 0, 0.38),
            text_color_normal=(0, 0, 0, 0.38)
        )
        animate.start(widget)

    def save_changes_made(self):

        global email_regex

        if not re.fullmatch(email_regex, self.account_dialog.content_cls.ids.email_information.text):
            self.animate_wrong_widget(self.account_dialog.content_cls.ids.email_information)
        else:
            with open("user_accounts.json", 'r+') as accounts_file:
                accounts = json.load(accounts_file)

                for user in accounts["user_accounts"]:
                    if user["username"] == user_logged_in:
                        user["first_name"] = self.account_dialog.content_cls.ids.first_name_information.text
                        user["last_name"] = self.account_dialog.content_cls.ids.last_name_information.text
                        user["e-mail"] = self.account_dialog.content_cls.ids.email_information.text
                        user["nickname"] = self.account_dialog.content_cls.ids.nickname_information.text

                        accounts_file.seek(0)
                        json.dump(accounts, accounts_file, indent=4)
                        accounts_file.truncate()
                        self.account_dialog.dismiss()
                        return


if __name__ == '__main__':
    PartyPlaytime().run()
