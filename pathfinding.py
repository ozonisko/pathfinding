from tkinter import *
import os, sys
import time
import copy

top = Tk()
wysokosc, szerokosc = 600, 1000
kratka = 25
skala = szerokosc // kratka
punkty = []
siatka = []
label = []
skos = False
algorytm = 1
krok = 0

# KLASA POINT
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 0
        self.f = 0
        self.all = self.f + self.h
        self.typ = 0  # 0-chodzenie, 1-sciana, 2-start, 3-koniec
        self.sasiady = []
        self.rodzic = None

# TWORZENIE TLA
C = Canvas(top, bg="white", height=wysokosc, width=szerokosc, bd=0)
for i in range(wysokosc // kratka):
    for j in range(skala):
        siatka.append(C.create_rectangle(j * kratka, i * kratka, (j + 1) * kratka, (i + 1) * kratka, fill="white",
                                         outline="black", width=2))
        punkty.append(Point(j, i))

def pomaluj_punkt2(i, kolor):
    C.itemconfig(siatka[i], fill=kolor)

def load():
    map = open("map.txt", 'r')
    mapa = []
    data = map.readline()
    for i in range(len(data)):
        mapa.append(int(data[i]))
    map.close()
    return mapa


mapa = load()
print(mapa)



def wyswietl_sasiadow():
    for i in opened:
        for i in i.sasiady:
            C.itemconfig(siatka[i.y * skala + i.x], fill="green")


def aktualizacja_tekstu():
    for i in opened:
        C.itemconfig(label[i.y * skala + i.x], text="f=" + str(i.f) + " h=" + str(i.h) + "\nAll = " + str(i.all))


def pomaluj_punkt(punkt, kolor):
    C.itemconfig(siatka[punkt.y * skala + punkt.x], fill=kolor)


def szukaj_sciezki(punkt):
    if punkt.typ is 0:
        pomaluj_punkt(punkt, "aqua")
    else:
        pomaluj_punkt(punkt, "aqua")
    if punkt.rodzic:
        szukaj_sciezki(punkt.rodzic)


def wyczysc_mape():
    for i in punkty:
        if C.itemcget(siatka[i.y * skala + i.x], "fill") in ["green", "red", "black"]:
            C.itemconfig(siatka[i.y * skala + i.x], fill="black")


# USTAWIANIE POZATKU I KONCA
for i in range(len(mapa)):
    if mapa[i] == 2:
        start = Point(i % skala, i // skala)
        pomaluj_punkt(start, "violet")
        punkty[i].typ = 2
    elif mapa[i] == 3:
        koniec = Point(i % skala, i // skala)
        pomaluj_punkt(koniec, "violet")
        punkty[i].typ = 3
    elif mapa[i] == 1:
        pomaluj_punkt(punkty[i], "black")


def dist(a, b):
    if skos:
        return min(abs(a.x - b.x), abs(a.y - b.y)) * 14 + abs(abs(a.x - b.x) - abs(a.y - b.y)) * 10
    else:
        return min(abs(a.x - b.x), abs(a.y - b.y)) * 20 + abs(abs(a.x - b.x) - abs(a.y - b.y)) * 10


# DODAWANIE SASIADOW I TYPU
def ustaw_sasiadow():
    for i in punkty:
        if i.x < skala - 1:  # prawa krawedz
            i.sasiady.append(punkty[i.y * skala + i.x + 1])
            if i.y > 0 and skos:  # gora
                i.sasiady.append(punkty[(i.y - 1) * skala + i.x + 1])
            if i.y < (wysokosc // kratka) - 1 and skos:  # dol
                i.sasiady.append(punkty[(i.y + 1) * skala + i.x + 1])
        if i.x > 0:  # lewa
            i.sasiady.append(punkty[i.y * skala + i.x - 1])
            if i.y > 0 and skos:  # gora
                i.sasiady.append(punkty[(i.y - 1) * skala + i.x - 1])
            if i.y < (wysokosc // kratka) - 1 and skos:  # dol
                i.sasiady.append(punkty[(i.y + 1) * skala + i.x - 1])
        if i.y > 0:  # gora
            i.sasiady.append(punkty[(i.y - 1) * skala + i.x])
        if i.y < (wysokosc // kratka) - 1:  # dol
            i.sasiady.append(punkty[(i.y + 1) * skala + i.x])

        if mapa[i.y * skala + i.x] == 1:
            i.typ = 1
        if algorytm:
            i.h = dist(i, koniec)


# DODANIE TEKSTU
# for i in range(len(punkty)):
#    label.append(C.create_text(punkty[i].x * kratka + kratka // 2, punkty[i].y * kratka + kratka // 2,
#                               text="f=" + str(punkty[i].f) + " h=" + str(punkty[i].h) + "\nAll = " + str(
#                                   punkty[i].all)))

########################################################################
########################################################################
########################################################################
# ALGORYTM#####################################################


opened = []
closed = []
opened.append(punkty[start.y * skala + start.x])  # Dodanie startu

current = start
time1 = 0
steps = 0




def start():
    change()
    step()

def clean():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def change():
    global time1, krok, algorytm, skos
    time1 = time.time()
    krok = w.get()
    algorytm = var.get()
    skos = var2.get()
    ustaw_sasiadow()


def step():
    global current, steps
    opened.sort(key=lambda x: (x.all, x.h))  # Wybierz best z sasiadow
    pomaluj_punkt(current, "green")
    if len(opened):
        current = opened.pop(0)
        closed.append(current)
    pomaluj_punkt(current, "blue")
    steps += 1

    if current.typ == 3:  # ostatni

        szukaj_sciezki(current)
        return

    stats.config(text = "Time: " + str(round(time.time() - time1, 2)) + "   Steps: " + str(steps))
    for sasiad in current.sasiady:
        if sasiad.typ == 1:
            pomaluj_punkt(sasiad, "black")
        if sasiad in closed:
            pomaluj_punkt(sasiad, "red")
        if sasiad in opened:
            if sasiad.f > current.f + dist(current, sasiad):
                sasiad.f = current.f + dist(current, sasiad)
                sasiad.all = sasiad.f + sasiad.h
                sasiad.rodzic = current
        if sasiad not in opened and sasiad not in closed and sasiad.typ is not 1:
            sasiad.f = current.f + dist(current, sasiad)
            sasiad.all = sasiad.f + sasiad.h
            sasiad.rodzic = current
            opened.append(sasiad)
            pomaluj_punkt(sasiad, "green")
            # print(current.f, current.h, current.all)

            # aktualizacja_tekstu()
            # wyczysc_mape()
    top.after(krok, step)

# Button frame
frame = Frame(top)
frame.pack()

# Start,Reset button
b = Button(frame, text='Start', command=start, width=30, height=2)
b.pack(side=LEFT)
b2 = Button(frame, text='Reset', command=clean, width=30, height=2)
b2.pack(side=LEFT)

# Dijkstra vs A*
var = IntVar()
R1 = Radiobutton(frame, text="Dijkstra", variable=var, value=0)
R2 = Radiobutton(frame, text="A*", variable=var, value=1)
R1.pack(side=RIGHT)
R2.pack(side=RIGHT)

# Skos vs prosta
var2 = IntVar()
R3 = Radiobutton(frame, text="Skos", variable=var2, value=1)
R4 = Radiobutton(frame, text="Prosto", variable=var2, value=0)
R3.pack(side=LEFT, fill=X)
R4.pack(side=LEFT, fill=X)

stats = Label(frame, text = "Time: " + str(0) + "   Steps: " + str(steps))
stats.pack(side=BOTTOM)

C.pack()
w = Scale(frame, from_=0, to=100, orient=HORIZONTAL)
w.pack()

top.mainloop()
