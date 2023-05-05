from kivy.animation import Animation
from kivy.clock import Clock
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

Window.size = (400, 780)
Window.top = 30
Window.left = 1000

user_logged_in = None
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


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
                    global user_logged_in
                    user_logged_in = user["username"]
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
        screen_manager.current = "home"

    def play_game(self, screen_manager):
        screen_manager.current = "headspinPlay"


class HeadSpinSettings(MDFloatLayout):
    pass


class HeadSpinPlay(MDScreen):
    def exit_game(self, screen_manager):
        screen_manager.current = "headspin"


class WordRushScreen(MDScreen):
    pass


class TicTacToeScreen(MDScreen):
    pass


class HelpUsDecideScreen(MDScreen):
    pass


class GameRulesInformation(MDFloatLayout):
    pass


class AccountInformation(MDFloatLayout):
    pass


class GameInformation(MDFloatLayout):
    pass


class PartyPlaytime(MDApp):
    account_dialog = None
    headspin_dialog = None
    information_dialog = None
    boardblitz_rules = None
    boardblitz_start = None
    boardblitz_exit_game = None
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
                    break

        self.headspin_dialog.open()

    def headspin_settings_exit(self):
        self.headspin_dialog.dismiss()

    def headspin_save_settings(self):
        with open("headspin_settings.json", 'r+') as headspin_settings:
            settings = json.load(headspin_settings)

            for setting in settings["headspin_settings"]:
                if setting["username"] == user_logged_in:
                    setting["round"] = self.headspin_dialog.content_cls.ids.round_information.text
                    setting["team"] = self.headspin_dialog.content_cls.ids.team_information.text
                    setting["timer"] = self.headspin_dialog.content_cls.ids.timer_information.text
                    setting["words"] = self.headspin_dialog.content_cls.ids.words_information.text

                    headspin_settings.seek(0)
                    json.dump(settings, headspin_settings, indent=4)
                    headspin_settings.truncate()
                    self.headspin_dialog.dismiss()
                    return

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
            empty_nickname = False
            for i in range(1, int(PartyPlaytime.player_button_selected[-1])):
                if self.boardblitz_start.content_cls.ids["boardblitz_nickname_" + str(i)].text == "":
                    empty_nickname = True
                    self.animate_wrong_widget(self.boardblitz_start.content_cls.ids["boardblitz_nickname_" + str(i)])

            if not empty_nickname:
                self.boardblitz_start.dismiss()
                print("start ")
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

    def exit_current_boardblitz_game(self, *args):
        self.boardblitz_exit_game.dismiss()
        print("implementeaza")
        self.root.current = 'home'

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