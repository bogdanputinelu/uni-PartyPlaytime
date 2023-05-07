from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition
from kivymd.app import MDApp
from kivymd.uix.behaviors import ScaleBehavior, CommonElevationBehavior
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSlideTransition
import json
import re
import random
from cuvinte import words

Window.size = (400, 780)
Window.top = 30
Window.left = 1000

user_logged_in = None
nickname_user_logged_in = None
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

boardblitz_avatars = [
    "boardblitz_characters/chowder.png", "boardblitz_characters/endive.png",
    "boardblitz_characters/gazpacho.png", "boardblitz_characters/gorgonzola.png",
    "boardblitz_characters/mungdaal.png", "boardblitz_characters/panini.png",
    "boardblitz_characters/shnitzel.png", "boardblitz_characters/truffles.png"
]


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
                                        "timer": "60",
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

    # rounds_headspin = 2
    # teams_headspin = 2
    # words_headspin = ["Kilimanjaro"]
    # timer_headspin = 60
    # players_headspin = 4
    # headspin_score = {}

    def headspin_play(self):
        with open("headspin_settings.json", 'r+') as headspin_files:
            settings = json.load(headspin_files)

            for setting in settings["headspin_settings"]:
                if setting["username"] == user_logged_in:
                    rounds_headspin = int(setting["round"])
                    teams_headspin = int(setting["team"])
                    words_headspin = setting["words"].split(",")
                    timer_headspin = int(setting["timer"])
                    players_headspin = setting["players"].split(",")
                    break

        players = []
        for person in players_headspin:
            new_person = person.strip()
            players.append(new_person)

        player_teams = []
        while len(players) > 0:
            first_player = random.choice(players)
            players.remove(first_player)
            second_player = random.choice(players)
            players.remove(second_player)
            player_teams.append((first_player, second_player))

        final_words = words
        for word in words_headspin:
            new_word = word.strip()
            final_words.append(str(new_word))

        print(final_words)
        print(player_teams)
        print(rounds_headspin)
        print(teams_headspin)
        print(timer_headspin)

        headspin_score = {}
        for team in player_teams:
            team_name = str(team[0] + " & " + team[1])
            headspin_score[team_name] = 0

        print(headspin_score)

        # for round in range(rounds_headspin):
        #     for team in player_teams:
        #         pass

    # def change_round(self, new_round):
    #     self.ids.round_number.text = new_round
    #
    # def change_team(self, new_team_name):
    #     self.ids.team_name.text = new_team_name
    #
    # def change_word(self, new_word):
    #     self.ids.word_to_guess = new_word


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
                    self.headspin_dialog.content_cls.ids.timer_information.text = setting["timer"]
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
                        setting["timer"] = self.headspin_dialog.content_cls.ids.timer_information.text
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
        if PartyPlaytime.player_button_selected[-1] == '2':
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.pos_hint = {"center_y": .5}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.pos_hint = {"center_y": 3}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.pos_hint = {"center_y": 3}

        elif PartyPlaytime.player_button_selected[-1] == '3':
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.pos_hint = {"center_y": .6}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.pos_hint = {"center_y": .4}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.pos_hint = {"center_y": 3}
        else:
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.pos_hint = {"center_y": .7}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.pos_hint = {"center_y": .5}
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.pos_hint = {"center_y": .3}

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

    def start_boardlitz_game(self):
        boardblitz_game_screen = self.root.get_screen("boardblitz_game")

        boardblitz_game_screen.ids.first_player_nickname.text = nickname_user_logged_in
        boardblitz_game_screen.ids.second_player_nickname.text = self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.text
        nickname_2_length = 8.5 * len(self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.text)
        boardblitz_game_screen.ids.second_player_nickname.width = str(nickname_2_length) + "dp"

        chosen_avatar_list = self.choose_avatars_for_boardblitz()

        boardblitz_game_screen.ids.first_player_avatar.source = boardblitz_avatars[chosen_avatar_list[0]]
        boardblitz_game_screen.ids.second_player_avatar.source = boardblitz_avatars[chosen_avatar_list[1]]

        if PartyPlaytime.player_button_selected[-1] == '2':
            boardblitz_game_screen.ids.third_avatar_box.pos_hint = {"center_y": 3, "center_x": .2}
            boardblitz_game_screen.ids.fourth_avatar_box.pos_hint = {"center_y": 3, "right": 1}

        elif PartyPlaytime.player_button_selected[-1] == '3':
            boardblitz_game_screen.ids.third_avatar_box.pos_hint = {"center_y": .77, "center_x": .2}
            boardblitz_game_screen.ids.fourth_avatar_box.pos_hint = {"center_y": 3, "right": 1}

            boardblitz_game_screen.ids.third_player_nickname.text = self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.text

            boardblitz_game_screen.ids.third_player_avatar.source = boardblitz_avatars[chosen_avatar_list[2]]

        else:
            boardblitz_game_screen.ids.third_avatar_box.pos_hint = {"center_y": .77, "center_x": .2}
            boardblitz_game_screen.ids.fourth_avatar_box.pos_hint = {"center_y": .77, "right": 1}

            boardblitz_game_screen.ids.third_player_nickname.text = self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.text

            boardblitz_game_screen.ids.fourth_player_nickname.text = self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.text
            nickname_4_length = 8.5 * len(self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.text)
            boardblitz_game_screen.ids.fourth_player_nickname.width = str(nickname_4_length) + "dp"

            boardblitz_game_screen.ids.third_player_avatar.source = boardblitz_avatars[chosen_avatar_list[2]]
            boardblitz_game_screen.ids.fourth_player_avatar.source = boardblitz_avatars[chosen_avatar_list[3]]

    def exit_current_boardblitz_game(self, *args):
        self.boardblitz_exit_game.dismiss()
        print("implementeaza")
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
