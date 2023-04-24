from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import random


class WelcomeScreen(Screen):
    pass


class PartyPlaytime(Screen):
    pass


class BoardBlitz(Screen):
    pass

class BoardBlitzRules(Screen):
    pass


class BoardBlitzSettings(Screen):
    pass


class BoardBlitzPlay(Screen):
    pass


class WordRush(Screen):
    pass

class WordRushRules(Screen):
    pass


class WordRushSettings(Screen):
    pass


class WordRushPlay(Screen):
    pass
    """
    fisier = open("cuvinte.txt", 'r')  # deschidem fisierul de unde luam cuvintele
    listaCuvinte = fisier.read().split(",")# In lista asta sunt cuvintele de mimat/desenat/descris din fisier. Irina, jocurile noastre pot impari fisierul
    nr_echipe = int(input("Numarul de echipe este = "))  # Selectam numarul de echipe
    puncte_echipe = [0 for contor in range(1, nr_echipe + 1)]
    versiune = int(input("Doriti sa jucati pe runde sau pe punctaj? Tastati 0 pentru runde sau 1 pentru punctaj\n"))
    if versiune == 0:
        nr_runde = int(input("Numarul de runde este = "))  # Selectam numarul de runde (in total se joaca nr_runde * nr_echipe runde)
        for runda in range(1, nr_runde + 1):
            # Afisam ce runda este. Un pop up sau sa ramana pe ecran
            for echipa in range(1, nr_echipe + 1):
                print("Este randul echipei ", echipa)
                tip_cartonas = random.randint(1, 4)
                indiceCartonas = random.randint(0,len(listaCuvinte)-1)
                cuvant_cartonas =  listaCuvinte[indiceCartonas]# extragem din lista cuvantul
                print("Tipul rundei: ", sep="")
                if tip_cartonas == 1:
                    print("Descris")
                elif tip_cartonas == 2:
                    print("Mimat")
                else:
                    print("Desenat")
                print(cuvant_cartonas)
                # aici as pune o pauza de 5 secunde ca sa ii dau timp celui care joaca sa retina ce cuvant are de jucat
                # pornesc timer 60 de secunde de raspuns
                # opresc timer
                print("A ghicit echipa cuvantul/expresia? Tastati 0 pentru nu sau 1 pentru da")
                punct = int(input())
                puncte_echipe[echipa-1] += punct
    else:
        nr_puncte = input("Numarul de puncte este = ")  # Selectam numarul de puncte ce trebuie atins pentru a castiga
        gata_joc = 0  # E o valoare care ne ajuta sa ne dam seama daca jocul s-a terminat (adica daca o echipa a ajuns la punctajul dorit)
        echipa_castigatoare = -1  # Aici salvam care e echipa castigatoare
        while (1):
            for echipa in range(1, nr_echipe + 1):
                print("Este randul echipei ", echipa)
                tip_cartonas = random.randint(1, 4)
                indiceCartonas = random.randint(0, len(listaCuvinte)-1)
                cuvant_cartonas = listaCuvinte[indiceCartonas]# extragem din lista cuvantul in mod aleator
                print("Tipul rundei: ", sep="")
                if tip_cartonas == 1:
                    print("Descris")
                elif tip_cartonas == 2:
                    print("Mimat")
                else:
                    print("Desenat")
                # aici as pune o pauza de 5 secunde ca sa ii dau timp celui care joaca sa retina ce cuvant are de jucat
                # pornesc timer 60 de secunde de raspuns
                # opresc timer
                print("A ghicit echipa cuvantul/expresia? Tastati 0 pentru nu sau 1 pentru da")
                punct = int(input())
                puncte_echipe[echipa-1] += punct
                if (puncte_echipe[echipa-1] == nr_puncte):
                    gata_joc = 1
                    echipa_castigatoare = echipa
                    break
            if (gata_joc == 1):
                break
        print("Echipa ", echipa_castigatoare, " a castigat!")
        # cumva ar trebui sa trimit inapoi la aplicatie
    """


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
