from tkinter import *
import time
from tkinter import messagebox
from tkinter import filedialog as fd

top = Tk()
field = Frame(top)
wysokosc, szerokosc = 600, 1000
kratka = 25
skala = szerokosc // kratka
punkty = []
siatka = []
label = []
skos = False
algorytm = 1
krok = 0
mapa = []
start = None
koniec = None
opened = []
closed = []

current = start
time1 = 0
steps = 0
cost = 0


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
C = Canvas(field, bg="white", height=wysokosc, width=szerokosc, bd=0)
for i in range(wysokosc // kratka):
    for j in range(skala):
        siatka.append(C.create_rectangle(j * kratka, i * kratka, (j + 1) * kratka, (i + 1) * kratka, fill="white",
                                         outline="black", width=2))
        punkty.append(Point(j, i))
        mapa.append(0)


def load():
    map = open("map.txt", 'r')
    mapa = []
    data = map.readline()
    for i in range(len(data)):
        mapa.append(int(data[i]))
    map.close()
    return mapa


def click(event):
    global start, koniec
    i = (event.x // kratka) + (event.y // kratka) * skala
    if i < szerokosc/kratka * wysokosc/kratka:
        if var3.get() == 0:
            mapa[i] = 0
            pomaluj_punkt(punkty[i], "white")
        elif var3.get() == 1:
            mapa[i] = 1
            pomaluj_punkt(punkty[i], "black")
        elif var3.get() == 2:
            mapa[i] = 2
            start = punkty[i]
            pomaluj_punkt(punkty[i], "aqua")
        elif var3.get() == 3:
            mapa[i] = 3
            koniec = punkty[i]
            pomaluj_punkt(punkty[i], "navy")


########### OPTIONAL
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

def save():
    name = fd.asksaveasfilename()
    output = open(name, mode='w')
    for item in mapa:
        output.write(str(item))
    output.close()


def change_map():
    global mapa, start, koniec
    file = fd.askopenfilename()
    map = open(file, 'r')
    new_map = []
    data = map.readline()
    for i in range(len(data)):
        new_map.append(int(data[i]))
    map.close()
    mapa = new_map
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
        i.sasiady = []
        i.rodzic = None
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
        else:
            i.h = 0


# DODANIE TEKSTU
# for i in range(len(punkty)):
#    label.append(C.create_text(punkty[i].x * kratka + kratka // 2, punkty[i].y * kratka + kratka // 2,
#                               text="f=" + str(punkty[i].f) + " h=" + str(punkty[i].h) + "\nAll = " + str(
#                                   punkty[i].all)))


def run():
    clean()
    change()
    step()


def clean():
    global opened, closed, start, time1, steps, current
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
            punkty[i].typ = 1
        elif mapa[i] == 0:
            pomaluj_punkt(punkty[i], "white")
            punkty[i].typ = 0

        opened = [start]
        closed = []
        opened.append(punkty[start.y * skala + start.x])  # Dodanie startu

        current = None
        time1 = 0
        steps = 0


def change():
    global time1, krok, algorytm, skos
    krok = w.get()
    algorytm = var.get()
    skos = var2.get()
    ustaw_sasiadow()
    time1 = time.time()


def step():
    global current, steps, cost
    opened.sort(key=lambda x: (x.all, x.h))  # Wybierz best z sasiadow
    if current:
        pomaluj_punkt(current, "green")
    if len(opened):
        current = opened.pop(0)
        closed.append(current)
    else:
        messagebox.showinfo("Koniec", "Brak drogi do celu")
        return
    pomaluj_punkt(current, "lime")

    cost = current.f
    stats.config(text="Time: " + str(round(time.time() - time1, 2)) + "  Visited: " + str(steps) + "  Cost: " + str(cost))
    steps += 1

    if current.typ == 3:  # ostatni
        szukaj_sciezki(current)
        return


    for sasiad in current.sasiady:
        if sasiad.typ == 1:
            pomaluj_punkt(sasiad, "black")
        if sasiad in closed:
            pomaluj_punkt(sasiad, "green")
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
            pomaluj_punkt(sasiad, "lime")

            # aktualizacja_tekstu()
    top.after(krok, step)


# Button menu
menu = Frame(top)
menu.pack()
field.pack()


# Start,Reset button
b = Button(menu, text='Start', command=run, width=20, height=2).grid(row=0, column=0)
b2 = Button(menu, text='Reset', command=clean, width=20, height=2).grid(row=0, column=1)
b3 = Button(menu, text='Choose map', command=change_map, width=20, height=2).grid(row=0, column=2)
b4 = Button(menu, text='Save map', command=save, width=20, height=2).grid(row=0, column=3)

# Dijkstra vs A*
var = IntVar()
R1 = Radiobutton(menu, text="Dijkstra", variable=var, value=0).grid(row=0, column=4, sticky='w')
R2 = Radiobutton(menu, text="A*", variable=var, value=1).grid(row=1, column=4, sticky='w')

# Straight vs Diagonally
var2 = IntVar()
R3 = Radiobutton(menu, text="Straight", variable=var2, value=1).grid(row=0, column=5, sticky='w')
R4 = Radiobutton(menu, text="Diagonally", variable=var2, value=0).grid(row=1, column=5, sticky='w')

var3 = IntVar()
M1 = Radiobutton(menu, text="Walkable", variable=var3, value=0).grid(row=0, column=6, sticky='w')
M2 = Radiobutton(menu, text="Block", variable=var3, value=1).grid(row=1, column=6, sticky='w')
M3 = Radiobutton(menu, text="Start", variable=var3, value=2).grid(row=0, column=7, sticky='w')
M4 = Radiobutton(menu, text="Finish", variable=var3, value=3).grid(row=1, column=7, sticky='w')


stats = Label(menu, text="Time: " + str(0) + "   Visited: " + str(steps) + "   Cost: " + str(cost))
stats.grid(row=1, column=0, sticky='w')

C.pack()
C.bind("<B1-Motion>", click)
delay = Label(menu, text="Delay between steps(ms): ").grid(row=1, column=2, sticky='e')
w = Scale(menu, from_=0, to=100, orient=HORIZONTAL)
w.grid(row=1, column=3)

top.mainloop()

