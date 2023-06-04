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
from tictactoe_helpers import medium_states, hard_states, solution_for_states

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


class TicTacToeOptions(MDFloatLayout):
    pass


class TicTacToeBox(MDBoxLayout):
    pass


class BoardBlitzButton(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class TicTacToeButton(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class TicTacToeOptionButton(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class HeadSpinButtonSettings(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class HeadSpinButtonPlay(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class WordRushButtonSettings(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
    def change_cursor(self, cursor_name):
        Window.set_system_cursor(cursor_name)


class WordRushButtonPlay(MDBoxLayout, FocusBehavior, CommonElevationBehavior):
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

                with open("wordrush_settings.json", 'r+') as wordrush_settings_default_file:
                    settings = json.load(
                        wordrush_settings_default_file)

                    default_settings = {"username": self.ids.username_register.text,
                                        "gameMode": "0",
                                        "nrPoints": "10",
                                        "nrRounds": "10",
                                        "nrTeams": "2"
                                        }
                    settings["wordrush_settings"].append(default_settings)
                    wordrush_settings_default_file.seek(0)
                    json.dump(settings, wordrush_settings_default_file, indent=4)
                    screen_manager.current = 'login'


class LoginScreen(MDScreen):
    def switch_password_mode(self):
        """
        Da voie utilizatorului sa schimbe modul de vizualizare a parolei introduse
        """
        if self.ids.password_login.password is True:
            self.ids.password_login.password = False
            self.ids.password_login.icon_right = "lock-open"
        else:
            self.ids.password_login.password = True
            self.ids.password_login.icon_right = "lock"
        self.ids.password_login.focus = True

    def login(self, screen_manager):
        """
        Verifica daca contul introdus se afla in baza de date si logheaza utilizatorul
        """
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
        """
        Animeaza datele introduse gresit
        """
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


class TicTacToeGame(MDScreen):
    pass


class HeadSpinScreen(MDScreen):
    def go_back(self, screen_manager):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "home"

    def play_game(self, screen_manager):
        screen_manager.current = "headspinPlay"


class HeadSpinSettings(MDFloatLayout):
    pass


class HeadSpinRules(MDFloatLayout):
    pass


class HeadSpinPlay(MDScreen):
    def __init__(self, **kwargs):
        super(HeadSpinPlay, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

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
    headspin_ranking_dialog = None
    clasament_final = []

    # Fuctie ce se apeleaza in momentul in care utilizatorul da play.
    # Se extrag setarile din fisier si se initializeaza jocul.

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

        HeadSpinPlay.headspin_score = {}
        for team in HeadSpinPlay.player_teams:
            team_name = str(team[0] + " & " + team[1])
            HeadSpinPlay.headspin_score[team_name] = 0

        HeadSpinPlay.index_round = 1
        HeadSpinPlay.headspin_ranking_dialog = None

    # Functie de initializare a setarilor in cazul in care se da replay

    def initialize(self):
        HeadSpinPlay.index_round = 1
        new_word = random.choice(HeadSpinPlay.final_words)
        HeadSpinPlay.final_words.remove(new_word)
        self.ids.word_to_guess.text = new_word
        self.ids.round_number.text = str(HeadSpinPlay.index_round)
        self.ids.next_round_button.disabled = False
        HeadSpinPlay.clasament_final = []
        HeadSpinPlay.headspin_ranking_dialog = None

    # Functie ce schimba echipa curenta si reseteaza corespunzator starile butoanelor

    def change_team(self):
        self.ids.next_round_button.disabled = True
        new_word = random.choice(HeadSpinPlay.final_words)
        HeadSpinPlay.final_words.remove(new_word)
        self.ids.word_to_guess.text = new_word
        if HeadSpinPlay.index_echipa == int(HeadSpinPlay.teams_headspin) - 2 and \
           HeadSpinPlay.index_round == int(HeadSpinPlay.rounds_headspin):
            self.ids.next_round_button.disabled = True
        self.ids.check_button.disabled = False
        self.ids.pass_button.disabled = False
        if HeadSpinPlay.index_echipa == int(HeadSpinPlay.teams_headspin) - 1:
            HeadSpinPlay.index_echipa = 0
            new_team_name = list(HeadSpinPlay.headspin_score.keys())[0]
        else:
            HeadSpinPlay.index_echipa += 1
            new_team_name = list(HeadSpinPlay.headspin_score.keys())[int(HeadSpinPlay.index_echipa)]
        HeadSpinPlay.words_per_team = HeadSpinPlay.words_per_round
        self.ids.team_name.text = new_team_name
        self.ids.words_per_team_id.text = "Words: " + str(HeadSpinPlay.words_per_round)

    # Functie ce se apeleaza atunci cand un cuvant este ghicit, contorizand scorul si schimband cuvantul curent

    def check_pressed(self):
        if HeadSpinPlay.words_per_team == 1:
            self.ids.pass_button.disabled = True
            self.ids.check_button.disabled = True
            current_team = self.ids.team_name.text
            HeadSpinPlay.headspin_score[current_team] += 1
            HeadSpinPlay.words_per_team -= 1
            self.ids.next_round_button.disabled = False
            if HeadSpinPlay.index_echipa == int(HeadSpinPlay.teams_headspin) - 1 and \
                    HeadSpinPlay.index_round == int(HeadSpinPlay.rounds_headspin):
                self.ids.next_round_button.disabled = True
                self.get_ranking()
                self.end_game_headspin()
            self.ids.words_per_team_id.text = "Words: " + str(HeadSpinPlay.words_per_team)
        elif HeadSpinPlay.words_per_team != 0:
            self.change_word()
            current_team = self.ids.team_name.text
            HeadSpinPlay.headspin_score[current_team] += 1

    # Functie ce schimba cuvantul curent de pe ecran

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
                if HeadSpinPlay.index_echipa == int(HeadSpinPlay.teams_headspin) - 1 and \
                   HeadSpinPlay.index_round == int(HeadSpinPlay.rounds_headspin):
                    self.ids.next_round_button.disabled = True
                    self.get_ranking()
                    self.end_game_headspin()

    # Functie ce se apeleaza atunci cand un cuvant nu este ghicit, schimbandu-se doar cuvantul curent

    def pass_pressed(self):
        if HeadSpinPlay.words_per_team == 1:
            self.ids.pass_button.disabled = True
            self.ids.check_button.disabled = True
            HeadSpinPlay.words_per_team -= 1
            self.ids.words_per_team_id.text = "Words: " + str(HeadSpinPlay.words_per_team)
            self.ids.next_round_button.disabled = False
            if HeadSpinPlay.index_echipa == int(HeadSpinPlay.teams_headspin) - 1 and \
                    HeadSpinPlay.index_round == int(HeadSpinPlay.rounds_headspin):
                self.ids.next_round_button.disabled = True
                self.get_ranking()
                self.end_game_headspin()
        elif HeadSpinPlay.words_per_team != 0:
            self.change_word()

    # Functie ce tine evidenta rundelor, afisand un mesaj corespunzator

    def round_change(self):
        if HeadSpinPlay.index_echipa == int(HeadSpinPlay.teams_headspin) - 1:
            if HeadSpinPlay.index_round != int(HeadSpinPlay.rounds_headspin):
                HeadSpinPlay.index_round += 1
                self.ids.round_number.text = str(HeadSpinPlay.index_round)
            else:
                self.ids.next_round_button.disabled = True

    # Functie ce stabileste clasamentul final, salvandu-l in functie de numarul de puncte al fiecarei echipe

    def get_ranking(self):
        ranking = sorted(HeadSpinPlay.headspin_score.items(), key=lambda x: x[1], reverse=True)
        clasament = dict({})
        for elem in ranking:
            if elem[1] in clasament.keys():
                clasament[elem[1]].append(elem[0])
            else:
                clasament[elem[1]] = [elem[0]]
        HeadSpinPlay.clasament_final = sorted(clasament.items(), key=lambda x: x[0], reverse=True)

    def go_home_headspin(self, *args):
        self.headspin_ranking_dialog.dismiss()
        self.headspin_ranking_dialog = None
        self.app.root.current = 'headspin'

    # Functie ce se apeleaza automat in ultima runda in momentul in care ultima echipa a ghicit sau nu a ghicit toate
    # cuvintele alocate. Pe baza clasamentului generat de get_ranking() se editeaza dialogul deschis.

    def end_game_headspin(self):
        self.get_ranking()
        if not self.headspin_ranking_dialog:
            self.headspin_ranking_dialog = MDDialog(
                type="custom",
                content_cls=RankingInformationHeadspin(),
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="EXIT",
                        font_name="fonts/BrunoAce-Regular.ttf",
                        font_size="30sp",
                        on_release=self.go_home_headspin,
                        pos_hint={"center_x": .5, "center_y": .5}
                    )
                ]
            )

            # Se adauga dinamic intr-un container cate o eticheta cu fiecare echipa si scorul corespunzator.

            container = MDBoxLayout(orientation='vertical',
                                    spacing='5dp',
                                    padding='10dp',
                                    pos_hint={"center_x": .5, "center_y": .5},
                                    size_hint_y=0.5
                                    )
            mini_container = MDFloatLayout(pos_hint={"center_x": .5, "center_y": .5})
            sus = 450

            for place, teams in enumerate(HeadSpinPlay.clasament_final, start=1):
                points, team = teams
                str_teams = ", ".join(team)

                eticheta = MDLabel(
                    id=f"{place}",
                    text=f"{place}. {str_teams} - {points} points",
                    size_hint_y=mini_container.y,
                    y=mini_container.top + dp(sus),
                    height=dp(100),
                    pos_hint={"center_x": 0.5},
                    font_name="fonts/LuckiestGuy-Regular.ttf",
                )
                sus -= 40
                if place <= 3:
                    eticheta.bold = True
                else:
                    eticheta.bold = False
                eticheta.font_size = "20sp"
                eticheta.font_name = "fonts/LuckiestGuy-Regular.ttf"
                mini_container.add_widget(eticheta)
            container.add_widget(mini_container)

            self.headspin_ranking_dialog.content_cls.add_widget(container)

        self.headspin_ranking_dialog.open()

# Se ocupa de trecerea de la pagina principala a jocului la meniul principal si la play game


class WordRushScreen(MDScreen):
    def go_back(self, screen_manager):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "home"

    def play_game(self, screen_manager):
        screen_manager.current = "wordrushPlay"


# Clasa asta trebuie sa existe pentru a putea avea in fisierul kivy o sectiune dedicata setarilor
# jocului WordRush, dar nu face nimic


class WordRushSettings(MDFloatLayout):
    pass


# Clasa asta trebuie sa existe pentru a putea avea in fisierul kivy o sectiune dedicata setarilor
# jocului WordRush, dar nu face nimic


class WordRushRules(MDFloatLayout):
    pass


# Clasa asta se ocupa de toata logica jocului WordRush. Aici sunt toate functiile care asigura functionalitatea jocului


class WordRushPlay(MDScreen):
    def __init__(self, **kwargs):
        super(WordRushPlay, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def exit_game(self, *args):
        self.wordrush_ranking_dialog.dismiss()
        self.wordrush_ranking_dialog = None
        self.app.root.current = 'wordrush'

    # Variabile pe care le folosesc pentru a folosi setarile jocului

    gameMode = 0
    nrPoints = 10
    nrRounds = 10
    nrTeams = 5

    # Variabile care ajuta in desfasurarea jocului

    teamPoints = [0 for _ in range(0, nrTeams + 1)]
    teamPasses = [3 for _ in range(0, nrTeams + 1)]
    team = 0
    checkable = 1
    ended = 0
    wordrush_ranking_dialog = None

    # O functie care gestioneaza functionalitatea butonului check

    def check(self):
        if self.checkable == 1 and self.ended != 1:
            self.teamPoints[self.team] += 1
            self.checkable = 0
            self.update_screen()

    # O functie care se ocupa de actualizarea ecranului la fiecare modificare adusa

    def update_screen(self):
        if self.gameMode == 1 and self.teamPoints[self.team] == self.nrPoints:
            # Aici doar modificam ce afisam pe ecran
            self.ids.roundLabel.text = "     End"
            self.ids.teamLabel.text = "Winner: "
            max_score = max(self.teamPoints)
            for i in range(1, self.nrTeams + 1):
                if self.teamPoints[i] == max_score:
                    self.ids.teamLabel.text += "Team " + str(i) + " "
            self.ids.pointsLabel.text = "Final score = " + str(self.teamPoints[self.team])
            self.ids.wordLabel.text = "Game ended. Return to main menu"
            self.ids.roundTypeLabel.text = ""
            self.ids.nextLabel.text = "See ranking"
            self.ended = 1
        if self.gameMode == 0 and self.round >= self.nrRounds and self.team == self.nrTeams:
            # Aici doar modificam ce afisam pe ecran
            self.ids.roundLabel.text = "     End"
            self.ids.teamLabel.text = "Winners: "
            max_score = max(self.teamPoints)
            for i in range(1, self.nrTeams+1):
                if self.teamPoints[i] == max_score:
                    self.ids.teamLabel.text += "Team " + str(i) + " "
            self.ids.pointsLabel.text = "Final score = " + str(self.teamPoints[self.team])
            self.ids.wordLabel.text = "Game ended. Return to main menu"
            self.ids.roundTypeLabel.text = ""
            self.ids.nextLabel.text = "See ranking"
            self.ended = 1
        if self.ended == 1:
            self.ids.checkLabel.disabled = True
            self.ids.passLabel.disabled = True
            self.ids.passLabel.text = "Pass"
            if not self.wordrush_ranking_dialog:
                self.wordrush_ranking_dialog = MDDialog(  # Generam widget-ul pentru clasament
                    type="custom",
                    content_cls=RankingInformationWordRush(),
                    auto_dismiss=False,
                    buttons=[
                        MDFlatButton(
                            text="EXIT",
                            font_name="fonts/BrunoAce-Regular.ttf",
                            font_size="30sp",
                            on_release=self.exit_game,
                            pos_hint={"center_x": .5, "center_y": .5}
                        )
                    ]
                )

                container = MDBoxLayout(orientation='vertical',  # Aici va sta clasamentul
                                        spacing='5dp',
                                        padding='10dp',
                                        pos_hint={"center_x": .5, "center_y": .5},
                                        size_hint_y=0.5
                                        )
                mini_container = MDFloatLayout(pos_hint={"center_x": .5, "center_y": .5})
                sus = 450

                clasament = []
                for i in range(1, self.nrTeams+1):
                    clasament.append([self.teamPoints[i], "Team " + str(i)])
                clasament.sort(reverse=True)
                i = 0
                fin = self.nrTeams - 1
                while i < fin:  # Punem echipele cu acelasi scor pe acelasi loc in clasament
                    if clasament[i][0] == clasament[i+1][0]:
                        clasament[i][1] = clasament[i][1] + ", " + clasament[i+1][1]
                        del clasament[i+1]
                        i = i - 1
                        fin = fin - 1
                    i = i + 1

                for place, teams in enumerate(clasament, start=1):
                    points, team = teams
                    str_teams = "".join(team)

                    eticheta = MDLabel(  # Punem echipele pe locul lor in clasament in widget
                        id=f"{place}",
                        text=f"{place}. {str_teams} - {points} points",
                        size_hint_y=mini_container.y,
                        y=mini_container.top + dp(sus),
                        height=dp(100),
                        pos_hint={"center_x": 0.5},
                        font_name="fonts/LuckiestGuy-Regular.ttf",
                    )
                    sus -= 40
                    if place <= 3:
                        eticheta.bold = True
                    eticheta.font_size = "20sp"
                    eticheta.font_name = "fonts/LuckiestGuy-Regular.ttf"
                    mini_container.add_widget(eticheta)
                container.add_widget(mini_container)

                self.wordrush_ranking_dialog.content_cls.add_widget(container)

            self.wordrush_ranking_dialog.open()

        if self.ended != 1:  # Jocul nu e gata. Continua
            if self.team == self.nrTeams:  # Se ocupa de trecerea ciclica de la o echipa la alta
                self.team = 1
            else:
                self.team = self.team + 1
            self.ids.teamLabel.text = "Team " + str(self.team)
            if self.team == 1:
                self.round = self.round + 1
            if self.gameMode == 0:
                self.ids.roundLabel.text = "Round " + str(self.round) + "/" + str(self.nrRounds)
            self.ids.pointsLabel.text = "Your points: " + str(self.teamPoints[self.team])
            round_type = random.randint(1, 4)
            index_word = random.randint(0, len(words) - 1)
            cuvant = words[index_word]
            if round_type == 1:
                self.ids.wordLabel.text = cuvant
                self.ids.roundTypeLabel.text = "DESCRIBE"
                self.ids.logoLabel.source = "logos/explain.png"
            elif round_type == 2:
                self.ids.wordLabel.text = cuvant
                self.ids.roundTypeLabel.text = "MIME"
                self.ids.logoLabel.source = "logos/mime.png"
            else:
                self.ids.wordLabel.text = cuvant
                self.ids.roundTypeLabel.text = "DRAW"
                self.ids.logoLabel.source = "logos/draw.png"
            self.ids.passLabel.text = "Pass (" + str(self.teamPasses[self.team]) + ")"
            self.checkable = 1

    # O functie care se ocupa de functionalitatea butonului de pass (echipa alege sa joace alt cuvant)

    def pass_word(self):
        if self.teamPasses[self.team] != 0 and self.ended != 1:
            self.teamPasses[self.team] -= 1
            round_type = random.randint(1, 4)
            index_word = random.randint(0, len(words) - 1)
            cuvant = words[index_word]
            if round_type == 1:
                self.ids.wordLabel.text = cuvant
                self.ids.roundTypeLabel.text = "DESCRIBE"
                self.ids.logoLabel.source = "logos/explain.png"
            elif round_type == 2:
                self.ids.wordLabel.text = cuvant
                self.ids.roundTypeLabel.text = "MIME"
                self.ids.logoLabel.source = "logos/mime.png"
            else:
                self.ids.wordLabel.text = cuvant
                self.ids.roundTypeLabel.text = "DRAW"
                self.ids.logoLabel.source = "logos/draw.png"
            self.ids.passLabel.text = "Pass (" + str(self.teamPasses[self.team]) + ")"
            self.checkable = 1

    # O functie care se ocupa de initializarea jocului

    def wordrush_play(self):
        self.ids.passLabel.disabled = False
        self.ids.checkLabel.disabled = False
        self.wordrush_ranking_dialog = None
        self.ids.nextLabel.text = "Allow next team"
        self.ids.teamLabel.text = "Team 1"
        self.ended = 0
        self.checkable = 1

        # Secventa urmatoare preia setarile personalizate ale utilizatorului din fisierul .json si initializeaza
        # datele membre ale clasei cu valorile respective

        with open("wordrush_settings.json", 'r+') as wordrush_files:
            settings = json.load(wordrush_files)

            for setting in settings["wordrush_settings"]:
                if setting["username"] == user_logged_in:
                    # Daca utilizatorul a introdus o valoare gresita pentru gameMode, se alege cea default = 0
                    if setting["gameMode"] != "0" and setting["gameMode"] != "1":
                        setting["gameMode"] = "0"
                    self.gameMode = int(setting["gameMode"])
                    self.nrPoints = int(setting["nrPoints"])
                    self.nrRounds = int(setting["nrRounds"])
                    self.nrTeams = int(setting["nrTeams"])
                    # Initializare pass + points
                    self.teamPoints = [0 for contor in range(0, self.nrTeams + 1)]
                    self.teamPasses = [3 for contor in range(0, self.nrTeams + 1)]
                    break

        self.team = 1
        self.round = 1
        if self.gameMode == 0:
            self.ids.roundLabel.text = "Round 1/" + str(self.nrRounds)
        else:
            self.ids.roundLabel.text = "Playing for \n" + str(self.nrPoints) + " points"
        self.ids.pointsLabel.text = "Your points: " + str(self.teamPoints[self.team])
        self.ids.passLabel.text = "Pass(3)"
        # Exact ca mai sus, generam o runda - tipul rundei si cartonasul ei
        round_type = random.randint(1, 4)
        index_word = random.randint(0, len(words) - 1)
        cuvant = words[index_word]
        if round_type == 1:
            self.ids.wordLabel.text = cuvant
            self.ids.roundTypeLabel.text = "DESCRIBE"
            self.ids.logoLabel.source = "logos/explain.png"
        elif round_type == 2:
            self.ids.wordLabel.text = cuvant
            self.ids.roundTypeLabel.text = "MIME"
            self.ids.logoLabel.source = "logos/mime.png"
        else:
            self.ids.wordLabel.text = cuvant
            self.ids.roundTypeLabel.text = "DRAW"
            self.ids.logoLabel.source = "logos/draw.png"


# Avem nevoie de clasa asta pentru a afisa clasamentul


class RankingInformationWordRush(MDFloatLayout):
    pass


class TicTacToeScreen(MDScreen):
    def go_back(self, screen_manager):
        screen_manager.transition.direction = 'right'
        screen_manager.current = "home"


class GameRulesInformation(MDFloatLayout):
    pass


class TicTacToeRulesInformation(MDFloatLayout):
    pass


class AccountInformation(MDFloatLayout):
    pass


class RankingInformation(MDFloatLayout):
    pass


class GameInformation(MDFloatLayout):
    pass


class RankingInformationHeadspin(MDFloatLayout):
    pass


class PartyPlaytime(MDApp):
    account_dialog = None
    headspin_dialog = None
    headspin_rules_dialog = None
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
    tictactoe_rules = None
    tictactoe_choose_options = None
    player_button_selected = "players_button_2"
    tictactoe_mode = "bot"
    tictactoe_difficulty = "easy"
    tictactoe_exit_dialog = None
    tictactoe_current_move = "x"
    tictactoe_finish = False
    tictactoe_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    tictactoe_occupied = []
    tictactoe_winner = None
    wordrush_dialog = None
    wordrush_rules_dialog = None
    wordrush_exit_game = None
    animation_message = Animation(
        duration=0.4,
        opacity=1
    ) + Animation(
        duration=0.4,
        opacity=0
    )

    def build(self):
        return Builder.load_file('party.kv')

    def account_info(self):
        """
        Deschide meniul ce contine informatiile contului
        """
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

    # Functie ce deschide un dialog si afiseaza setarile introduse pentru jocul Headspin

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

    def headspin_settings_exit(self):
        self.headspin_dialog.dismiss()

    # Functie ce salveaza setarile nou introduse in dialog

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
                        setting["words_per_round"] = \
                            self.headspin_dialog.content_cls.ids.words_per_round_information.text
                        setting["words"] = self.headspin_dialog.content_cls.ids.words_information.text
                        setting["players"] = self.headspin_dialog.content_cls.ids.players_information.text

                        headspin_settings.seek(0)
                        json.dump(settings, headspin_settings, indent=4)
                        headspin_settings.truncate()
                        self.headspin_dialog.dismiss()
                        return

    # Functie ce deschide dialogul cu reguli pentru Headspin

    def headspin_rules(self):
        if not self.headspin_rules_dialog:
            self.headspin_rules_dialog = MDDialog(
                type='custom',
                content_cls=HeadSpinRules()
            )
        self.headspin_rules_dialog.open()

    def exit_headspin_rules(self):
        self.headspin_rules_dialog.dismiss()

    # Functie ce avertizeaza utilizatorul ca a apasat pe X, luand decizia de a parasi jocul

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

    def dismiss_headspin_game(self, *args):
        self.headspin_exit_game.dismiss()

    def exit_current_headspin_game(self, *args):
        self.headspin_exit_game.dismiss()
        self.root.current = 'headspin'

    def wordrush_settings(self):  # Functia asta se ocupa de salvarea si incarcarea setarilor pentru jocul WordRush
        if not self.wordrush_dialog:  # Astfel se deschide meniul
            self.wordrush_dialog = MDDialog(
                type="custom",
                content_cls=WordRushSettings(),
            )

        with open("wordrush_settings.json", 'r+') as wordrush_files:
            settings = json.load(wordrush_files)
            # Fiecare optiune primeste setarea salvata de utilizator
            for setting in settings["wordrush_settings"]:
                if setting["username"] == user_logged_in:
                    # Utilizatorul a introdus o valoare gresita. GameMode primeste valoarea default 0
                    if setting["gameMode"] != "0" and setting["gameMode"] != "1":
                        setting["gameMode"] = "0"
                    self.wordrush_dialog.content_cls.ids.gameMode.text = setting[
                        "gameMode"]  # Punem in casete valoarile din setari
                    self.wordrush_dialog.content_cls.ids.nrPoints.text = setting["nrPoints"]
                    self.wordrush_dialog.content_cls.ids.nrRounds.text = setting["nrRounds"]
                    self.wordrush_dialog.content_cls.ids.nrTeams.text = setting["nrTeams"]
                    break

        self.wordrush_dialog.open()

    def wordrush_settings_exit(self):  # Se ocupa de iesirea din meniul de setari
        self.wordrush_dialog.dismiss()

    def wordrush_save_settings(self):  # Se ocupa de salvarea setarilor introduse in meniul de setari
        with open("wordrush_settings.json", 'r+') as wordrush_settings:
            settings = json.load(wordrush_settings)

            for setting in settings["wordrush_settings"]:  # Trecem prin utilizatori
                if setting["username"] == user_logged_in:  # Pana il gasim pe cel logat
                    setting["gameMode"] = self.wordrush_dialog.content_cls.ids.gameMode.text
                    # Verificam validitatea setarii pentru gameMode. Daca e invalida, dam valoarea default
                    if setting["gameMode"] != "0" and setting["gameMode"] != "1":
                        setting["gameMode"] = "0"
                    setting["nrPoints"] = self.wordrush_dialog.content_cls.ids.nrPoints.text
                    setting["nrRounds"] = self.wordrush_dialog.content_cls.ids.nrRounds.text
                    setting["nrTeams"] = self.wordrush_dialog.content_cls.ids.nrTeams.text

                    wordrush_settings.seek(0)
                    json.dump(settings, wordrush_settings, indent=4)
                    wordrush_settings.truncate()
                    self.wordrush_dialog.dismiss()
                    return

    def wordrush_rules(self):  # Aceasta functie se ocupa de afisarea regulilor
        if not self.wordrush_rules_dialog:
            self.wordrush_rules_dialog = MDDialog(
                type='custom',
                content_cls=WordRushRules()
            )
        self.wordrush_rules_dialog.open()

    # Aceasta functie se ocupa de iesirea din fereastra cu reguli pentru WordRush

    def exit_wordrush_rules(self):
        self.wordrush_rules_dialog.dismiss()

    # Aceasta functie se ocupa de afisarea ferestrei pentru iesirea dintr-un meci activ de WordRush

    def exit_wordrush_game(self):
        if not self.wordrush_exit_game:
            self.wordrush_exit_game = MDDialog(
                title="Do you want to exit this game?",
                buttons=[
                    MDFlatButton(
                        text="NO",
                        on_release=self.dismiss_wordrush_game
                    ),
                    MDFlatButton(
                        text="YES",
                        on_release=self.exit_current_wordrush_game
                    ),
                ]
            )

        self.wordrush_exit_game.open()

    # Aceasta functie se ocupa de anularea iesirii dintr-un meci activ de WordRush

    def dismiss_wordrush_game(self, *args):
        self.wordrush_exit_game.dismiss()

    # Aceasta functie se ocupa de iesirea dintr-un meci activ de WordRush

    def exit_current_wordrush_game(self, *args):
        self.wordrush_exit_game.dismiss()
        self.root.current = 'wordrush'

    def exit_dialogue(self):
        self.account_dialog.dismiss()

    def game_information(self):
        """
        Deschide meniul ce ofera informatii despre jocuri din pagina de home
        """
        if not self.information_dialog:
            self.information_dialog = MDDialog(
                type='custom',
                content_cls=GameInformation()
            )

        self.information_dialog.open()

    def exit_game_information(self):
        self.information_dialog.dismiss()

    def open_tictactoe_rules(self):
        """
        Deschide meniul ce ofera informatii despre tictactoe
        """
        if not self.tictactoe_rules:
            self.tictactoe_rules = MDDialog(
                type="custom",
                content_cls=TicTacToeRulesInformation()
            )

        self.tictactoe_rules.open()

    def exit_tictactoe_rules(self):
        self.tictactoe_rules.dismiss()

    def open_rules(self):
        """
        Deschide meniul ce ofera informatii despre boardblitz
        """
        if not self.boardblitz_rules:
            self.boardblitz_rules = MDDialog(
                type="custom",
                content_cls=GameRulesInformation()
            )

        self.boardblitz_rules.open()

    def exit_game_rules(self):
        self.boardblitz_rules.dismiss()

    def boardblitz_players(self, *args):
        """
        Gestioneaza meniul de dinaintea inceperii jocului de BoardBlitz, functionalitatea alegerii
        optiunilor(cuplarea butoanelor din meniu cu cele din pagina) precum si validarea acestora
        pentru inceperea jocului.
        """
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
        """
        Coreleaza numarul de casete de nickname(din meniul de optiuni, precum si in meniul de ranking)
        ale playerilor cu optiunea aleasa.
        """
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
        """
        Deschide meniul optiunilor ce trebuie alese pentru a incepe jocul de Boardblitz.
        """
        if not self.boardblitz_start:
            self.boardblitz_start = MDDialog(
                type="custom",
                content_cls=BoardBlitzStart()
            )

        self.boardblitz_start.open()

    def exit_boardblitz_start(self):

        self.boardblitz_start.dismiss()

    def exit_boardblitz_game(self):
        """
        Deschide meniul pentru parasirea jocului de BoardBlitz
        """
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
        """
        Alege random un avatar pentru fiecare player.
        """
        avatars = []

        while len(avatars) < 4:
            chosen_avatar = random.randint(0, 7)

            while chosen_avatar in avatars:
                chosen_avatar = random.randint(0, 7)

            avatars.append(chosen_avatar)

        return avatars

    def send_away_aliens(self, screen, colors):
        """
        Face ca pionii de culori specificate sa dispara de pe ecran.
        """
        for color in colors:
            for alien_number in "1234":
                screen.ids[color + "_alien_" + alien_number].pos = (dp(1000), dp(1000))

    def bring_in_aliens(self, screen, colors):
        """
        Face ca pionii de culori specificate sa apara pe ecran.
        """
        for color in colors:
            for alien_number in "1234":
                current_alien = color + "_alien_" + alien_number
                screen.ids[current_alien].pos = \
                    (dp(coordinates[current_alien]["width"]), dp(coordinates[current_alien]["height"]))

    def blockage(self, alien, color, dice_rolled):
        """
        Verifica pentru zarul aruncat daca pionul are sau nu un blocaj in fata.
        """
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
        """
        Gaseste lista de pioni ce pot efectua o mutare avand in vedere zarul aruncat.
        """
        alien_moves = []
        player_turn = ["red", "blue", "green", "yellow"]

        alien_color = player_turn[turn - 1]

        for i in "1234":
            current_alien = alien_color + "_alien_" + i

            if aliens_state[current_alien] == 0 and dice_rolled == 6 and \
                    self.blockage(current_alien, alien_color, dice_rolled) is False:
                alien_moves.append(current_alien)
            elif aliens_state[current_alien] > 0 and self.blockage(current_alien, alien_color, dice_rolled) is False:
                alien_moves.append(current_alien)

        return alien_moves

    def go_to_next_turn(self, dice, next_player_dice, dice_number, dice_rolled, *args):
        """
        Efectueaza animatia zarului de la o runda la alta.
        """
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
        """
        Intoarce utilizatorul la pagina jocului si reseteaza jocul de BoardBlitz.
        """
        self.boardblitz_ranking_dialog.dismiss()
        self.reset_boardblitz()
        self.root.current = 'boardblitz'

    def end_game(self):
        """
        Afiseaza meniul de ranking de la finalul jocului de BoardBlitz.
        """
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
        """
        Efectueaza miscarea pionului ales si gestioneaza situatiile urmate de aceasta miscare:
            - jocul se termina
            - player-ul curent a ajuns la finish (iese din pool-ul de playeri ce continua jocul)
        """
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
                corners_to_surpass = [current_box_number] if current_box_number in [12, 25, 38, 51] \
                    else corners_to_surpass[:-1] + [corners_to_surpass[-1] - 1]
            if current_box_number == 52 and dice_rolled == 6:
                corners_to_surpass = [5]
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
                Clock.schedule_once(partial(self.go_to_next_turn, things[0], things[1], things[2], dice_rolled),
                                    duration)
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
                    Clock.schedule_once(partial(self.go_to_next_turn, things[0], things[1], things[2], dice_rolled),
                                        0.2)

    def animate_dice(self, dice, dice_number):
        """
        Animeaza zarul apasat si activeaza pionii ce se pot muta, altfel se trece la urmatorul player
        """
        if dice.opacity == 0 or dice_clicked[dice_number]:
            return
        dice_clicked[dice_number] = True

        def rotate_back_dice(dt):
            nonlocal dice, dice_number
            screen = self.root.get_screen("boardblitz_game")
            next_player_dice = screen.ids["dice_player_" +
                                          str(next_dice[PartyPlaytime.number_of_players_boardblitz][dice_number])]

            dice.rotate_value_angle = 0

            dice_rolled = random.randint(1, 6)
            if random.randint(2, 4) == 3:
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
        """
        Pentru fiecare player sunt aduse in ecran elementele pentru inceperea jocului de BoardBlitz.
        Avatarele sunt alese, nickname-urile atribuite si pionii adusi in ecran
        """
        boardblitz_game_screen = self.root.get_screen("boardblitz_game")
        PartyPlaytime.number_of_players_boardblitz = int(PartyPlaytime.player_button_selected[-1])

        boardblitz_game_screen.ids.first_player_nickname.text = nickname_user_logged_in
        boardblitz_game_screen.ids.second_player_nickname.text = \
            self.boardblitz_start.content_cls.ids.boardblitz_nickname_1.text
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

            boardblitz_game_screen.ids.third_player_nickname.text = \
                self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.text

            boardblitz_game_screen.ids.third_player_avatar.source = boardblitz_avatars[chosen_avatar_list[2]]

            self.send_away_aliens(boardblitz_game_screen, ["yellow"])
            self.bring_in_aliens(boardblitz_game_screen, ["green", "red", "blue"])

        else:
            boardblitz_game_screen.ids.third_avatar_box.pos_hint = {"center_y": .77, "center_x": .2}
            boardblitz_game_screen.ids.fourth_avatar_box.pos_hint = {"center_y": .77, "right": 1}

            boardblitz_game_screen.ids.third_player_nickname.text = \
                self.boardblitz_start.content_cls.ids.boardblitz_nickname_2.text

            boardblitz_game_screen.ids.fourth_player_nickname.text = \
                self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.text
            nickname_4_length = 10 * len(self.boardblitz_start.content_cls.ids.boardblitz_nickname_3.text)
            boardblitz_game_screen.ids.fourth_player_nickname.width = str(nickname_4_length) + "dp"

            boardblitz_game_screen.ids.third_player_avatar.source = boardblitz_avatars[chosen_avatar_list[2]]
            boardblitz_game_screen.ids.fourth_player_avatar.source = boardblitz_avatars[chosen_avatar_list[3]]

            self.bring_in_aliens(boardblitz_game_screen, ["green", "yellow", "red", "blue"])

    def reset_dice(self):
        """
        Reseteaza zarul
        """
        boardblitz_game_screen = self.root.get_screen("boardblitz_game")
        boardblitz_game_screen.ids.dice_player_1.opacity = 1

        for i in "234":
            boardblitz_game_screen.ids["dice_player_" + i].opacity = 0

        for i in range(1, 5):
            dice_clicked[i] = False

    def reset_alien_size(self):
        """
        Reseteaza marimea pionilor
        """
        screen = self.root.get_screen("boardblitz_game")
        for color in ["red", "blue", "green", "yellow"]:
            for alien_number in "1234":
                current_alien = color + "_alien_" + alien_number
                screen.ids[current_alien].icon_size = "30sp"

    def reset_ranking(self):
        """
        Reseteaza ranking-ul
        """
        PartyPlaytime.boardblitz_finish_aliens = {"red": 0, "green": 0, "blue": 0, "yellow": 0}
        PartyPlaytime.number_of_players_finished = 0
        PartyPlaytime.boardblitz_ranking = {"red": 0, "green": 0, "blue": 0, "yellow": 0}

    def reset_boardblitz(self):
        """
        Reseteaza toate optiunile necesare, pentru a se putea juca iar BoardBlitz.
        """
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
        """
        Asigura parasirea jocului de BoardBlitz.
        """
        self.boardblitz_exit_game.dismiss()

        self.reset_boardblitz()

        self.root.current = 'boardblitz'

    def exit_tictactoe_game(self):
        """
        Deschide meniul de parasire a jocului de TicTacToe.
        """
        if not self.tictactoe_exit_dialog:
            self.tictactoe_exit_dialog = MDDialog(
                title="Do you want to exit this game?",
                buttons=[
                    MDFlatButton(
                        text="NO",
                        on_release=self.dismiss_tictactoe_game
                    ),
                    MDFlatButton(
                        text="YES",
                        on_release=self.exit_current_tictactoe_game
                    ),
                ]
            )

        self.tictactoe_exit_dialog.open()

    def tictactoe_go_home(self):
        """
        Returneaza player-ul la pagina jocului de TicTacToe dupa finalizarea acestuia.
        """
        self.reset_tictactoe()
        self.root.current = "tictactoe"

    def predict_next_move(self):
        """
        In functie de dificultatea aleasa (mediu sau dificil) calculeaza urmatoarea mutare.
        """
        state = PartyPlaytime.tictactoe_board

        check = medium_states if PartyPlaytime.tictactoe_difficulty == "medium" else hard_states
        for i, j in check:
            if state[i] == state[j] and state[i] != 0 and state[solution_for_states[(i, j)]] == 0:
                return solution_for_states[(i, j)]

        return -1

    def make_random_choice(self, choice_made=-1):
        """
        Genereaza urmatoarea mutare a botului pentru orice dificultate.
        """
        screen = self.root.get_screen("tictactoe_game")
        if choice_made == -1:
            bot_choice = random.randint(0, 8)
            while bot_choice in PartyPlaytime.tictactoe_occupied:
                bot_choice = random.randint(0, 8)
        else:
            bot_choice = choice_made

        PartyPlaytime.tictactoe_occupied.append(bot_choice)

        screen.ids["tac_box_" + str(bot_choice + 1)].button_value = "0"
        screen.ids["tac_box_" + str(bot_choice + 1)].disabled = True

        PartyPlaytime.tictactoe_board[bot_choice] = 2

    def bot_makes_move(self):
        """
        Calculeaza mutarea bot-ului pentru TicTacToe.
        """
        screen = self.root.get_screen("tictactoe_game")
        if PartyPlaytime.tictactoe_difficulty == "easy":
            self.make_random_choice()
        else:
            predicted_choice = self.predict_next_move()
            self.make_random_choice(predicted_choice)

    def animate_message(self, ending):
        """
        Animeaza mesajul de final pentru TicTacToe care anunta castigatorul
        sau daca a fost egal.
        """
        screen = self.root.get_screen("tictactoe_game")
        if ending == "draw":
            screen.ids.end_message.text = "draw!!"
        else:
            screen.ids.end_message.text = nickname_user_logged_in \
                if PartyPlaytime.tictactoe_winner == 'x' \
                else screen.ids.bot_nickname.text
            screen.ids.end_message.text += " won!!"

        animation = Animation(
            duration=0.2,
            opacity=1
        )

        animation.start(screen.ids.game_ending)
        animation.start(screen.ids.ending_home_box)

        PartyPlaytime.animation_message.repeat = True
        PartyPlaytime.animation_message.start(screen.ids.end_message)

    def animate_win(self, *args):
        """
        Coloreaza formatia castigatoare.
        """
        screen = self.root.get_screen("tictactoe_game")
        for i in args:
            screen.ids["tac_box_" + str(i + 1)].button_disabled_color = "#238823"

        self.animate_message("win")

    def check_win_tictactoe(self):
        """
        Verifica daca exista un castigator pentru situatia curenta.
        """
        state = PartyPlaytime.tictactoe_board

        for i in range(3):
            if state[3*i + 0] == state[3*i + 1] and state[3*i + 1] == state[3*i + 2] and state[3*i + 0] != 0:
                self.animate_win(3*i + 0, 3*i + 1, 3*i + 2)
                return True
            if state[i + 0] == state[i + 3] and state[i + 3] == state[i + 6] and state[i + 0] != 0:
                self.animate_win(i + 0, i + 3, i + 6)
                return True

        if state[0] == state[4] and state[4] == state[8] and state[0] != 0:
            self.animate_win(0, 4, 8)
            return True
        if state[2] == state[4] and state[4] == state[6] and state[2] != 0:
            self.animate_win(2, 4, 6)
            return True

        return False

    def tictactoe_make_move(self, button_id):
        """
        Pentru casuta selectata, se va afisa mutarea facuta. Apoi alterneaza randul cu
        celalalt player sau, daca se joaca impotriva unui bot, va muta si pentru bot.
        Verifica daca jocul s-a terminat.
        """
        if not PartyPlaytime.tictactoe_finish:
            screen = self.root.get_screen("tictactoe_game")
            if PartyPlaytime.tictactoe_mode == "bot":
                screen.ids[button_id].button_value = "X"
                screen.ids[button_id].disabled = True

                button_number = int(button_id.split("_")[-1]) - 1

                PartyPlaytime.tictactoe_board[button_number] = 1

                PartyPlaytime.tictactoe_occupied.append(button_number)

                PartyPlaytime.tictactoe_winner = "x"
                if self.check_win_tictactoe():
                    PartyPlaytime.tictactoe_finish = True
                elif len(PartyPlaytime.tictactoe_occupied) == 9:
                    self.animate_message("draw")
                else:
                    self.bot_makes_move()
                    PartyPlaytime.tictactoe_winner = "0"
                    if self.check_win_tictactoe():
                        PartyPlaytime.tictactoe_finish = True
            else:
                if PartyPlaytime.tictactoe_current_move == 'x':
                    value = 'X'
                    number = 1
                    winner = 'x'
                    next_move = '0'
                else:
                    value = '0'
                    number = 2
                    winner = '0'
                    next_move = 'x'

                screen.ids[button_id].button_value = value
                screen.ids[button_id].disabled = True

                button_number = int(button_id.split("_")[-1]) - 1

                PartyPlaytime.tictactoe_board[button_number] = number

                PartyPlaytime.tictactoe_occupied.append(button_number)

                PartyPlaytime.tictactoe_winner = winner
                PartyPlaytime.tictactoe_current_move = next_move
                if self.check_win_tictactoe():
                    PartyPlaytime.tictactoe_finish = True
                elif len(PartyPlaytime.tictactoe_occupied) == 9:
                    self.animate_message("draw")

    def reset_tictactoe(self):
        """
        Reseteaza jocul de TicTacToe pentru a putea fi jucat din nou.
        """
        PartyPlaytime.tictactoe_current_move = "x"
        screen = self.root.get_screen("tictactoe_game")
        screen.ids.bot_nickname.width = "30dp"
        screen.ids.bot_nickname.text = "BOT"
        PartyPlaytime.tictactoe_finish = False
        PartyPlaytime.tictactoe_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        PartyPlaytime.tictactoe_occupied = []
        PartyPlaytime.tictactoe_winner = None
        screen.ids.game_ending.opacity = 0
        screen.ids.ending_home_box.opacity = 0
        PartyPlaytime.animation_message.cancel(screen.ids.end_message)

        for i in "123456789":
            screen.ids["tac_box_" + i].button_value = ""
            screen.ids["tac_box_" + i].disabled = False
            screen.ids["tac_box_" + i].button_disabled_color = "black"

    def exit_current_tictactoe_game(self, *args):
        """
        Paraseste jocul curent de TicTacToe
        """
        self.tictactoe_exit_dialog.dismiss()

        self.reset_tictactoe()

        self.root.current = 'tictactoe'

    def dismiss_tictactoe_game(self, *args):
        self.tictactoe_exit_dialog.dismiss()

    def exit_tictactoe_options(self):

        self.tictactoe_choose_options.dismiss()

    def prepare_avatars_tictactoe(self):
        """
        Alege random avatare pentru cei doi playeri sau pentru player si bot.
        Pune pe ecran nickname-urile aferente.
        """
        chosen_avatar_list = self.choose_avatars_for_boardblitz()

        screen = self.root.get_screen("tictactoe_game")

        screen.ids.player_avatar.source = boardblitz_avatars[chosen_avatar_list[0]]
        screen.ids.bot_avatar.source = boardblitz_avatars[chosen_avatar_list[1]]

        screen.ids.player_nickname.text = nickname_user_logged_in

        if PartyPlaytime.tictactoe_mode == "player":
            player_nickname = self.tictactoe_choose_options.content_cls.ids.tictactoe_nickname.text
            nickname_length = 10 * len(player_nickname)
            screen.ids.bot_nickname.width = str(nickname_length) + "dp"
            screen.ids.bot_nickname.text = player_nickname

    def tictactoe_options(self, *args):
        """
        Gestioneaza meniul de optiuni pentru inceperea jocului de TicTacToe.
        Coreleaza butoanele de optiuni Versus Bot si Versus Player cu cele din pagina
        jocului. Valideaza nickname-ul player-ului introdus. Da start la joc.
        """
        if args[0] == "start_game":
            nickname_box = self.tictactoe_choose_options.content_cls.ids.tictactoe_nickname
            if PartyPlaytime.tictactoe_mode == "player" \
                    and (len(nickname_box.text) >= 12 or len(nickname_box.text) == 0):
                self.animate_wrong_widget(nickname_box)
            else:
                self.tictactoe_choose_options.dismiss()

                self.prepare_avatars_tictactoe()

                self.root.current = "tictactoe_game"
        elif args[0] != "choose_options":
            if not self.tictactoe_choose_options:
                self.tictactoe_choose_options = MDDialog(
                    type="custom",
                    content_cls=TicTacToeOptions()
                )
            button_pressed = args[1].split('_')[1]
            old_button = PartyPlaytime.tictactoe_mode
            PartyPlaytime.tictactoe_mode = button_pressed

            screen = self.root.get_screen("tictactoe")

            screen.ids["versus_" + old_button].\
                md_bg_color = "white"
            screen.ids["versus_" + old_button].\
                unfocus_color = "white"

            self.tictactoe_choose_options.content_cls.ids["versus_" + old_button + "_2"].\
                md_bg_color = "white"
            self.tictactoe_choose_options.content_cls.ids["versus_" + old_button + "_2"].\
                unfocus_color = "white"

            screen.ids["versus_" + button_pressed].\
                md_bg_color = (1, 1, 1, .8)
            screen.ids["versus_" + button_pressed].\
                unfocus_color = (1, 1, 1, .8)

            self.tictactoe_choose_options.content_cls.ids["versus_" + button_pressed + "_2"].\
                md_bg_color = (1, 1, 1, .8)
            self.tictactoe_choose_options.content_cls.ids["versus_" + button_pressed + "_2"].\
                unfocus_color = (1, 1, 1, .8)

            self.update_tictactoe_options()
        else:
            if not self.tictactoe_choose_options:
                self.tictactoe_choose_options = MDDialog(
                    type="custom",
                    content_cls=TicTacToeOptions()
                )

            self.tictactoe_choose_options.open()

    def update_tictactoe_options(self):
        """
        Coreleaza butoanele de Versus Bot si Versus Player cu optiunile aferente.
        Versus Player - introducere nickname player
        Versus Bot - alegerea dificultatii
        """
        if PartyPlaytime.tictactoe_mode == "bot":
            self.tictactoe_choose_options.content_cls.ids.tictactoe_nickname.\
                pos_hint = {"center_y": 3.5}

            self.tictactoe_choose_options.content_cls.ids.easy_button.\
                pos_hint = {"center_x": .5, "center_y": .7}
            self.tictactoe_choose_options.content_cls.ids.medium_button.\
                pos_hint = {"center_x": .5, "center_y": .5}
            self.tictactoe_choose_options.content_cls.ids.hard_button.\
                pos_hint = {"center_x": .5, "center_y": .3}
        else:
            self.tictactoe_choose_options.content_cls.ids.tictactoe_nickname. \
                pos_hint = {"center_y": .5}

            self.tictactoe_choose_options.content_cls.ids.easy_button. \
                pos_hint = {"center_x": .5, "center_y": 3.7}
            self.tictactoe_choose_options.content_cls.ids.medium_button. \
                pos_hint = {"center_x": .5, "center_y": 3.5}
            self.tictactoe_choose_options.content_cls.ids.hard_button. \
                pos_hint = {"center_x": .5, "center_y": 3.3}

    def set_tictactoe_difficulty(self, difficulty):
        """
        Evidentiaza butonul de dificultate ales
        """
        self.tictactoe_choose_options.content_cls.ids[PartyPlaytime.tictactoe_difficulty + "_button"].\
            button_text_color = "white"

        PartyPlaytime.tictactoe_difficulty = difficulty

        self.tictactoe_choose_options.content_cls.ids[PartyPlaytime.tictactoe_difficulty + "_button"]. \
            button_text_color = "black"

    def animate_wrong_widget(self, widget):
        """
        Animeaza informatia introdusa gresit.
        """
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
        """
        Salveaza modificarile facute la informatiile facute.
        Inainte de a salva, modificarile sunt validate, iar daca acestea nu sunt
        valide, este animata casuta unde informatia trebuie introdusa corect.
        """
        global email_regex, nickname_user_logged_in

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
                        nickname_user_logged_in = self.account_dialog.content_cls.ids.nickname_information.text

                        accounts_file.seek(0)
                        json.dump(accounts, accounts_file, indent=4)
                        accounts_file.truncate()
                        self.account_dialog.dismiss()
                        return


if __name__ == '__main__':
    PartyPlaytime().run()
