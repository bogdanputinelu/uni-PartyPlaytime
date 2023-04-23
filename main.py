from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


class WelcomeScreen(Screen):
    pass


class PartyPlaytime(Screen):
    pass


class BoardBlitz(Screen):
    pass


class WordRush(Screen):
    pass

class WordRushRules(Screen):
    pass


class WordRushSettings(Screen):
    pass


class WordRushPlay(Screen):
    pass


class Headspin(Screen):
    pass


class HeadspinRules(Screen):
    pass


class HeadspinSettings(Screen):
    pass


class HeadspinPlay(Screen):
    pass


class TicTacToe(Screen):
    pass


class HelpUsDecide(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("screens.kv")


class PartyPlaytimeApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    PartyPlaytimeApp().run()
