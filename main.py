from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition
from kivymd.app import MDApp
from kivymd.uix.behaviors import ScaleBehavior, CommonElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDFadeSlideTransition
import json
import re
import random
import time
from cuvinte import words
from kivy.clock import Clock

Window.size = (400, 780)
Window.top = 30
Window.left = 1000

user_logged_in = None
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class Game(MDBoxLayout):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.register_event_type("on_release")

    def on_release(self, *args):

        args[0].current = args[1]


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
        screen_manager.transition = MDFadeSlideTransition(duration=0.5)

    def change_transition_for_welcome(self, screen_manager):
        screen_manager.transition = FadeTransition()


class BoardBlitzScreen(MDScreen):
    def go_back(self, screen_manager):
        screen_manager.current = "home"


class HeadSpinScreen(MDScreen):
    pass


class WordRushScreen(MDScreen):
    pass

class WordRushRulesScreen(MDScreen):
    pass


class WordRushSettingsScreen(MDScreen):
    gameMode = 0 # Default, game mode este 0, adica POINTS. ROUNDS este 1
    nrPoints = 10 # Default, se joaca pana prima echipa obtine 10 puncte
    nrRounds = 10 # Default, se joaca 10 runde
    nrTeams = 2 # Default, numarul de echipe este 0.
    timeLeft = 60 # Default, echipele au 60 de secunde sa raspunda

    def buton_gameMode(self, widget): # Functie care ne schimba game mode-ul
        if widget.text == "Points":
            widget.text = "Rounds"
            WordRushSettingsScreen.gameMode = 1
        else:
            widget.text = "Points"
            WordRushSettingsScreen.gameMode = 0
    def slider_nrEchipe(self, widget): # Functie care ne schimba numarul de echipe
        WordRushSettingsScreen.nrTeams = int(widget.value)
    def slider_timeLeft(self, widget):
        WordRushSettingsScreen.timeLeft = int(widget.value)
    def slider_nrRounds(self, widget):
        WordRushSettingsScreen.nrRounds = int(widget.value)
    def slider_nrPoints(self, widget):
        WordRushSettingsScreen.nrPoints = int(widget.value)



    def getGamemode(self):
        return WordRushSettingsScreen.gameMode
    def getNrTeams(self):
        return WordRushSettingsScreen.nrTeams
    def getTimeLeft(self):
        return WordRushSettingsScreen.timeLeft


class WordRushPlayScreen(MDScreen):
    gameMode = WordRushSettingsScreen.gameMode
    nrTeams = WordRushSettingsScreen.nrTeams
    nrPoints = WordRushSettingsScreen.nrPoints
    nrRounds = WordRushSettingsScreen.nrRounds
    timeLeft = WordRushSettingsScreen.timeLeft
    teamPoints = [0 for contor in range(0, nrTeams + 1)]
    teamPasses = [3 for contor in range(0, nrTeams + 1)]
    round = 0
    team = 0

    def build(self):
        Clock.schedule_interval(self.update_clock, 1)

    def update_clock(self, *args):
        # Called once a second using the kivy.clock module
        # Add one second to the current time and display it on the label
        self.timeLeft = self.timeLeft - 1

    def joc(self):
        if self.gameMode == 0:
            for self.round in range(1, self.nrRounds + 1):
                # Afisam ce runda este. Un pop up sau sa ramana pe ecran
                for self.team in range(1, self.nrTeams + 1):
                    print("Este randul echipei ", self.team)
                    roundType = random.randint(1, 4)
                    indexWord = random.randint(0,len(words)-1)
                    cuvant =  words[indexWord]# extragem din lista cuvantul
                    print("Tipul rundei: ", sep="")
                    if roundType == 1:
                        print("Descris")
                    elif roundType == 2:
                        print("Mimat")
                    else:
                        print("Desenat")
                    print(cuvant)

                    while(self.teamPasses[self.team] != 0):  # Un while pe care il folosesc pentru a permite alegerea altui cuvant
                        pasam = int(input("Doriti sa primiti alt cuvant? Mai aveti " + str(self.teamPasses[self.team]) + " pass-uri disponibile. Introduceti 1 daca da, 0 altfel"))
                        if pasam == 1:
                            self.teamPasses[self.team] = self.teamPasses[self.team] - 1
                            roundType = random.randint(1, 4)
                            indexWord = random.randint(0, len(words) - 1)
                            cuvant = words[indexWord]
                            print("Tipul rundei: ", sep="")
                            if roundType == 1:
                                print("Descris")
                            elif roundType == 2:
                                print("Mimat")
                            else:
                                print("Desenat")
                            print(cuvant)
                        else:
                            break
                    # Aici trebuie sa pun un buton ca sa ii dau ocazia celui care joaca sa dea ready, nu sa inceapa instant runda
                    # pornesc timer 60 de secunde de raspuns

                    while self.timeLeft:
                        mins, secs = divmod(self.timeLeft, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer)
                        time.sleep(1)
                        self.timeLeft -= 1
                    # opresc timer
                    print("A ghicit echipa cuvantul/expresia? Tastati 0 pentru nu sau 1 pentru da")
                    punct = int(input())
                    self.teamPoints[self.team] += punct
        else:
            endGame = 0  # E o valoare care ne ajuta sa ne dam seama daca jocul s-a terminat (adica daca o echipa a ajuns la punctajul dorit)
            winner = -1  # Aici salvam care e echipa castigatoare
            while (1):
                for team in range(1, self.nrTeams + 1):
                    print("Este randul echipei ", team)
                    roundType = random.randint(1, 4)
                    indexWord = random.randint(0, len(words)-1)
                    cuvant = words[indexWord]# extragem din lista cuvantul in mod aleator
                    print("Tipul rundei: ", sep="")
                    if roundType == 1:
                        print("Descris")
                    elif roundType == 2:
                        print("Mimat")
                    else:
                        print("Desenat")
                    print(cuvant)

                    while(self.teamPasses[self.team] != 0):  # Un while pe care il folosesc pentru a permite alegerea altui cuvant
                        pasam = int(input("Doriti sa primiti alt cuvant? Mai aveti " + str(self.teamPasses[self.team]) + " pass-uri disponibile. Introduceti 1 daca da, 0 altfel"))
                        if pasam == 1:
                            self.teamPasses[self.team] = self.teamPasses[self.team] - 1
                            roundType = random.randint(1, 4)
                            indexWord = random.randint(0, len(words) - 1)
                            cuvant = words[indexWord]
                            print("Tipul rundei: ", sep="")
                            if roundType == 1:
                                print("Descris")
                            elif roundType == 2:
                                print("Mimat")
                            else:
                                print("Desenat")
                            print(cuvant)
                        else:
                            break
                    # aici as pune o pauza de 5 secunde ca sa ii dau timp celui care joaca sa retina ce cuvant are de jucat
                    # pornesc timer 60 de secunde de raspuns
                    while self.timeLeft:
                        mins, secs = divmod(self.timeLeft, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer)
                        time.sleep(1)
                        self.timeLeft -= 1
                    # opresc timer
                    print("A ghicit echipa cuvantul/expresia? Tastati 0 pentru nu sau 1 pentru da")
                    punct = int(input())
                    self.teamPoints[self.team] += punct
                    if (self.teamPoints[self.team] == self.nrPoints):
                        endGame = 1
                        winner = team
                        break
                if (endGame == 1):
                    break
            print("Echipa ", winner, " a castigat!")
            # cumva ar trebui sa trimit inapoi la aplicatie


class TicTacToeScreen(MDScreen):
    pass


class HelpUsDecideScreen(MDScreen):
    pass


class AccountInformation(MDFloatLayout):
    pass


class PartyPlaytime(MDApp):
    account_dialog = None

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

    def exit_dialogue(self):

        self.account_dialog.dismiss()

    def animate_wrong_email(self, widget):

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
            self.animate_wrong_email(self.account_dialog.content_cls.ids.email_information)
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
