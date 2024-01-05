import random
import copy
import math
import time
import os


#
# WAFFE
#

class Waffe(object):
    def __init__(self, schaden, zeichen, name, taste):
        self.schaden = schaden
        self.zeichen = zeichen
        self.name = name
        self.taste = taste
        self.deepcpy = False
        
waffe_Dreizack = Waffe(20.0, "Ψ", "DREIZACK", "2")
waffe_Faeuste = Waffe(5.0, "☞", "FÄUSTE", "1")


#
# MONSTER
#

class Monster(object):
    def __init__(self, schaden, gesundheit, zeichen, name, ist_beweglich):
        self.schaden = schaden
        self.gesundheit = gesundheit
        self.max_gesundheit = gesundheit
        self.zeichen = zeichen
        self.name = name
        self.ist_beweglich = ist_beweglich
        self.deepcpy = True
        
monster_Klein = Monster(25.0, 40.0, "ö", "KLEINES MONSTER", False)
monster_Gross = Monster(40.0, 60.0, "Ö", "GROSSES MONSTER", True)
    
#
# INVENTAR
#

class Inventar(object):
    def __init__(self, elemente = dict()):
        self.inventar = elemente
        
    def anz_untersch_Elemente(self):
        n = 0
        for e in self.inventar:
            if self.inventar[e] > 0:
                n += 1
        return n
    
    def fuege_hinzu(self, element, anzahl):
        if not self.inventar.keys().__contains__(element):
            self.inventar[element] = 0
            
        self.inventar[element] += anzahl
        
    def entferne(self, element, anzahl):
        self.inventar[element] -= anzahl
        
    def ist_leer(self):
        return self.anz_untersch_Elemente() == 0
    
    def ausgabe(self):
        s = ""
        for key in self.inventar:
            if self.inventar[key] != 0:
                s += key.name + " (" + str(self.inventar[key]) + ") "
        return s
    
    def n_tes_nichtleeres_element(self, n):
        i = 1
        for key in self.inventar:
            if self.inventar[key] != 0:
                if i == n:
                    return key
                else:
                    i += 1
                    
    def schatzkiste_hinzufuegen(self, schatzkiste):
        for e in schatzkiste.inventar.inventar:
            if not self.inventar.keys().__contains__(e):
                self.inventar[e] = 0
                
            self.inventar[e] += schatzkiste.inventar.inventar[e]
    
#
# HELD
#

class Held(object):
    def __init__(self, zeichen, gesundheit, staerke):
        self.name = ""
        self.position = [0,0]
        
        self.waffen = [waffe_Faeuste]
        self.waffe_ausgeruestet = waffe_Faeuste
        self.zeichen = zeichen
        self.gesundheit = gesundheit
        self.max_gesundheit = gesundheit
        self.staerke = staerke
        self.inventar = Inventar()
        
    def konsumiere(self, konsumierbares):
        printc(f"Du hast {konsumierbares.name} konsumiert und fühlst dich etwas merkwürdig...")
        printc(konsumierbares.beschreibung)
        self.gesundheit = clamp(self.gesundheit + konsumierbares.gesundheit, 0, self.max_gesundheit)
        self.staerke += konsumierbares.staerke
        self.inventar.entferne(konsumierbares, 1)
        
HELD_1 = Held('O', 100.0, 1.2)
held = copy.deepcopy(HELD_1)

#
# KONSUMIERBAR
#

class Konsumierbar(object):
    def __init__(self, name, gesundheit, staerke, beschreibung):
        self.gesundheit = gesundheit
        self.staerke = staerke
        self.name = name
        self.beschreibung = beschreibung
        
apfel = Konsumierbar("APFEL", 20.0, 0.0, "Ein Apfel bringt 20 Gesundheit.")
gesundheitstrank = Konsumierbar("GESUNDHEITSTRANK", 50.0, 0.0, "Ein Gesundheitstrank bringt 50 Gesundheit.")
staerketrank = Konsumierbar("STÄRKETRANK", 0.0, 0.4, "Ein Stärketrank verleiht bis zum Ende des Kampfes 40% mehr Stärke.")

held.inventar.fuege_hinzu(staerketrank, 1)

#
# SCHATZKISTE
#

class Schatzkiste(object):
    def __init__(self, name, inventar, zeichen):
        self.inventar = inventar
        self.name = name
        self.zeichen = zeichen
        self.deepcpy = False
        
schatzkiste_1 = Schatzkiste("KLEINE SCHATZKISTE", Inventar({apfel:2}), "€")
schatzkiste_2 = Schatzkiste("MITTLERE SCHATZKISTE", Inventar({gesundheitstrank:1, staerketrank:2}), "$")
schatzkiste_3 = Schatzkiste("GROßE SCHATZKISTE", Inventar({apfel:3, gesundheitstrank:2, staerketrank:4}), "£")

#
# SPIELFELD
#

spielfeld_1_template = ["####################",
                        "## ##+ Ö $#######+##",
                        "#  ö€# #  ##+£     #",
                        "# ## # #   ö    Ö+ #",
                        "#Ψ #   #Öö##  Ö    #",
                        "##################Δ#"]

alle_moeglichen_felder = ["#", monster_Gross, monster_Klein, waffe_Dreizack, "+", ' ', schatzkiste_1, schatzkiste_2, schatzkiste_3, 'Δ']

spielfeld = []

def spielfeld_erzeugen(template):
    for z in range(0, len(template)):
        spielfeld.append([])
        for templ_feld in template[z]:
            for moegl_feld in alle_moeglichen_felder:
                if type(moegl_feld) == str:
                    if moegl_feld == templ_feld:
                        spielfeld[z].append(moegl_feld)
                elif moegl_feld.zeichen == templ_feld:
                    if moegl_feld.deepcpy:
                        spielfeld[z].append(copy.deepcopy(moegl_feld))
                    else:
                        spielfeld[z].append(moegl_feld)

spielfeld_erzeugen(spielfeld_1_template)

def printlr(l, r):
    s = "{0:<50}{2:>50}".format(l, "", r)
    print(s)
    return s + "\n"
    
def printlcr(l, c, r):
    s = "{0:<33}{1:^33}{2:>33}".format(l, c, r)
    print(s)
    return s + "\n"

def printl(l):
    s = l
    print(l)
    return s + "\n"



def schaden_berechnen(monster):
    global held
    
    history = ""

    kopfzeile = f"Du bist auf ein {monster.name} gestoßen! Möge der Kampf beginnen...".center(100) + "\n\n"\
                ""\
                "{0:<33}{1:^33}{2:>33}".format(held.name.upper() + " (" + held.waffe_ausgeruestet.zeichen + ")", "vs.", monster.name) + "\n"
    
    # wer ist an der Reihe? Der Spieler (False) oder das Monster (True)?
    an_der_reihe = bool(random.randint(0, 1))
    if not an_der_reihe:
        history += printl(held.name + " beginnt!")
    else:
        history += printl(monster.name + " beginnt!")
        
    def ausgabe():
        os.system('cls')
        print(kopfzeile, end='')
        printlr(gesundheitsbalken_erzeugen(round(held.gesundheit), held.max_gesundheit) + " (" + str(round(held.gesundheit)) + "/" + str(held.max_gesundheit) + ")",
            gesundheitsbalken_erzeugen(round(monster.gesundheit), monster.max_gesundheit) + " (" + str(round(monster.gesundheit)) + "/" + str(monster.max_gesundheit) + ")")
        print("")
        print(history)
        
    ausgabe()
    
    def frage_konsumieren():
        global held
        if held.inventar.ist_leer():
            return
        
        printc("In deinem Inventar befindet sich:")
        printc(held.inventar.ausgabe())
        printc("")
        printc("Möchtest du einen Gegenstand konsumieren?")
        
        while True:
            printc("Drücke Eingabetaste um fortzufahren, 1 für das erste Element im Inventar, 2 für das zweite Element usw.")
            wahl = input()
            if wahl == "":
                return
            elif wahl.isnumeric():
                if int(wahl) > 0 and int(wahl) <= held.inventar.anz_untersch_Elemente():
                    held.konsumiere(held.inventar.n_tes_nichtleeres_element(int(wahl)))
                    time.sleep(3)
                    return
                     
    time.sleep(1)
            
    while held.gesundheit > 0 and monster.gesundheit > 0:
        praezision = 0.3 + random.random() * 0.7 # Schaden von 30-100%
        if not an_der_reihe: # Spieler haut zu
            frage_konsumieren()
            schaden = held.waffe_ausgeruestet.schaden * praezision * held.staerke
            schaden = round(schaden)
            monster.gesundheit -= schaden
            if praezision >= 0.9:
                history += printl(f"{held.name} haut mit unglaublicher Zielgenauigkeit zu und verursacht {schaden} Schaden!")
            elif praezision >= 0.7:
                history += printl(f"{held.name} haut kräftig zu und verursacht {schaden} Schaden!")
            elif praezision >= 0.5:
                history += printl(f"{held.name} haut zu und verursacht {schaden} Schaden!")
            elif praezision >= 0.3:
                history += printl(f"{held.name} torkelt umher, haut dann zu und verursacht immerhin noch {schaden} Schaden!")
            elif praezision >= 0.1:
                history += printl(f"{held.name} rutscht auf einer Bananenschale aus, fällt auf das Monster und verursacht läppige {schaden} Schaden!")
        else:
            schaden = monster.schaden * praezision
            schaden = round(schaden)
            held.gesundheit -= schaden
            if praezision >= 0.9:
                history += printl(f"{monster.name} haut mit unglaublicher Zielgenauigkeit zu und verursacht {schaden} Schaden!")
            elif praezision >= 0.7:
                history += printl(f"{monster.name} haut kräftig zu und verursacht {schaden} Schaden!")
            elif praezision >= 0.5:
                history += printl(f"{monster.name} haut zu und verursacht {schaden} Schaden!")
            elif praezision >= 0.3:
                history += printl(f"{monster.name} torkelt umher, haut dann zu und verursacht immerhin noch {schaden} Schaden!")
            elif praezision >= 0.1:
                history += printl(f"{monster.name} rutscht auf einer Bananenschale aus, fällt auf das Monster und verursacht läppige {schaden} Schaden!")
        
        an_der_reihe = not an_der_reihe
        
        ausgabe()
        
        time.sleep(2)
        
        
    if held.gesundheit <= 0:
        print("Du bist leider tot.")
        quit()
    else:
        print("Du hast gesiegt! Das Monster ist tot!")

    time.sleep(5)
    os.system('cls')


def waffe_ausruesten(taste):
    global held
    for w in held.waffen:
        if w.taste == taste:
            held.waffe_ausgeruestet = w
            printc("Du hast " + w.name + " ausgeruestet.")
            printc("")

def waffen_ausgeben():
    print("Waffeninventar: ")
    for w in held.waffen:
        print(w.zeichen + " (" + w.taste + ") ", end='')
    print()
    print()
    print("Ausgerüstete Waffe: " + held.waffe_ausgeruestet.zeichen)
    print()
    
def alles_anzeigen():
    waffen_ausgeben()
    print()
    gesundheit_anzeigen()
    print()
    spielfeldAnzeigen()
    print()
    

def clamp(x,min,max):
    if x <= min:
        return 0
    elif x >= max:
        return max
    else:
        return x
    
# zeichnet das Spielfeld in der Konsole. Der Spieler bekommt ein Extra-Zeichen
def spielfeldAnzeigen():
    for z in range(0,len(spielfeld)):
        for s in range(0,len(spielfeld[z])):
            if z == held.position[0] and s == held.position[1]:
                print(held.zeichen, end='')
            else:
                if type(spielfeld[z][s]) == str:
                    print(spielfeld[z][s], end='')
                else:
                    print(spielfeld[z][s].zeichen, end='')
        print()
        
# zeichnet die Gesundheit des Spielers
def gesundheit_anzeigen():
    print("Gesundheit: ")
    print(gesundheitsbalken_erzeugen(held.gesundheit, 100))
    print()
    
def gesundheitsbalken_erzeugen(gesundheit, max_gesundheit):
    gesundheitsbalken = ""
    max_gesundheitsbalken = int(max_gesundheit / 10.0)
    gesundheit_int = int(math.ceil(gesundheit / 10.0))
    for i in range(0, gesundheit_int):
        gesundheitsbalken += "♥"
    if gesundheit_int < max_gesundheitsbalken:
        for i in range(0, max_gesundheitsbalken - gesundheit_int):
            gesundheitsbalken += "♡"
    return gesundheitsbalken
    
def gesundheit_veraendern(betrag):
    global held
    if held.gesundheit + betrag <= 0.0:
        held.gesundheit = 0.0
        print("Du bist gestorben.")
        quit()
    elif held.gesundheit + betrag > 100.0:
        held.gesundheit = 100.0
    else:
        held.gesundheit += betrag
        
def monster_bewegen():
    global spielfeld
    bewegte_felder = []
    for z in range(0,len(spielfeld)):
        for s in range(0,len(spielfeld[z])):
            if not (z, s) in bewegte_felder:
                if type(spielfeld[z][s]) == Monster:
                    if spielfeld[z][s].ist_beweglich:
                        l = []
                        if z-1 >= 0 and spielfeld[z-1][s] == ' ':
                            l.append((z-1,s))
                        if s-1 >= 0 and spielfeld[z][s-1] == ' ':
                            l.append((z,s-1))
                        if z+1 < len(spielfeld) and spielfeld[z+1][s] == ' ':
                            l.append((z+1,s))
                        if s+1 < len(spielfeld[z]) and spielfeld[z][s+1] == ' ':
                            l.append((z,s+1))
                            
                        if not len(l) == 0:
                            r = random.randint(0, len(l)-1)
                            
                            spielfeld[l[r][0]][l[r][1]] = spielfeld[z][s]
                            spielfeld[z][s] = ' '
                            bewegte_felder.append((l[r][0],l[r][1]))
    
def bewegen(richtung):
    global spielfeld
    global held
    
    neuePosition = copy.deepcopy(held.position)
    if richtung == 'S':
        neuePosition[0] += 1
    elif richtung == 'N':
        neuePosition[0] -= 1
    elif richtung == 'O':
        neuePosition[1] += 1
    elif richtung == 'W':
        neuePosition[1] -= 1
    else:
        waffe_ausruesten(richtung)
        return
    
        
    neuesSpielfeld = spielfeld[neuePosition[0]][neuePosition[1]]
    if neuesSpielfeld == '#':
        printc("Du kannst hier nicht lang. Das ist eine Wand!\n")
        return
    
    held.position = copy.deepcopy(neuePosition)
    
    if neuesSpielfeld == '+':
        printc("Du hast einen Zauberpilz gefunden! Deine Gesundheit erhöht sich um 20.\n")
        gesundheit_veraendern(20)
        spielfeld[neuePosition[0]][neuePosition[1]] = ' '
    elif type(neuesSpielfeld) == Waffe:
        printc("Du hast " + neuesSpielfeld.name + " gefunden!\n")
        held.waffen.append(neuesSpielfeld)
        spielfeld[neuePosition[0]][neuePosition[1]] = ' '
    elif type(neuesSpielfeld) == Monster:
        schaden_berechnen(neuesSpielfeld)
        spielfeld[neuePosition[0]][neuePosition[1]] = ' '
    elif type(neuesSpielfeld) == Schatzkiste:
        printc("Du hast " + neuesSpielfeld.name + " gefunden!\n")
        printc("Die Schatzkiste enthält:")
        printc(neuesSpielfeld.inventar.ausgabe())
        printc("")
        held.inventar.schatzkiste_hinzufuegen(neuesSpielfeld)
        spielfeld[neuePosition[0]][neuePosition[1]] = ' '
    elif neuesSpielfeld == 'Δ':
        print("Du hast den Ausgang gefunden! Herzlichen Glückwunsch!")
        quit()
    else:
        printc(f"{held.name} ist einen Schritt weiter in die Dunkelheit gegangen...\n")
        
    monster_bewegen()
    
def printc(s):
    st = s.center(100)
    print(st)
    return st + "\n"
        
held.name = input("Hallo! Nenne bitte deinen Namen: ")
os.system('cls')
held.position = [1,2]
print()
printc("Willkommen auf der Schlangen-Insel, " + held.name + "!")
printc("Du befindest Dich im Dschungel vor dem Eingang einer Höhle - hinter Dir liegt der Strand.")
printc("Du kannst deine Figur mit (w), (a), (s), (d) steuern und die Waffe mit (1), (2) usw. wechseln.")
printc("Viel Spaß!")

print()

alles_anzeigen()
print()
while True:
    richtung = input("Du kannst nach (N)orden, (O)sten, (S)üden, (W)esten gehen. Was möchtest Du tun?").upper()
    os.system('cls')
    print()
    bewegen(richtung)
    alles_anzeigen()
    
