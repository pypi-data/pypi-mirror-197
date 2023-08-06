wydrukuj = print
def czypuste(*args):
    if args == ():
        return True
    else:
        return False
wszystkosc_prawdziwa = all
smietnik = bin
szesciokat = hex
osmiornica = oct
dodaj_listem = sum 
dywizjonuj_modyfikacje = divmod
odszyfruj = lambda x, y:x.decode(y)
typiarz = type
bardziej_okrongly = round
super_duper = super
duzie_literki = lambda x:x.upper()
malutenkie_literki = lambda x:x.lower()
kapitalizuj = lambda x:x.capitalize()
negatyw_literek = lambda x:x.swapcase()
znajdz = lambda x, y:x.find(y)
licz = lambda x, y:x.count(y)
prawdziwosc = True
nie_prawdziwosc = False
otworz = open
dlugosc = len
zamknij = lambda x:x.close()
przeczytaj_linie = lambda x:x.readline()
przeczytaj_tekst = lambda x:x.read()
napisz = lambda x,y:x.write(y)
napisz_pare_wersow = lambda x, y: x.writelines(y)
przedluz = lambda x, y: x.append(y)
segreguj = lambda x: x.sort()
odwrotnosc = lambda x:x.reverse()
def rozszczep(*x):
    try:
        return x[0].split(x[1])
    except:
        return x[0].split()
wejdz = input
startuje_z = lambda x, y:x.startswith(y)
wyliczac = enumerate
znak_z_liczby = chr
liczba_ze_znaku = ord
formatuj_ktore_nwm_co_robi = format
formatuj = lambda x, y: x.format(y)
nowka_sztuka_linijka = "\n"
slownik = dict()
gowno_lista = tuple()
ustaw = set()
cyferki_i_literki = list()
mapa_wedrownika = map
nic = str
unosic_sie = float
calosc = int
zasieg = range
szesciopak = abs
najmniej = min
najwiencej = max
to_samo = lambda x,y: x == y
inne = lambda x,y: x != y
wieksze_niz = lambda x,y: x > y
mniejsze_niz = lambda x,y: x < y
rowne_lub_wieksze_niz = lambda x,y: x >= y
rowne_lub_mniejsze_niz = lambda x,y: x <= y
lub = lambda x,y: x or y
oraz = lambda x,y: x and y
jest_w = lambda x,y: x in y
drobne_z_dywizji_rowne = lambda x,y,z:x % y == z
def potega(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik ** i
    return wynik
def drobne(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik % i
    return wynik
def dodaj(*zmienne):
    if type(zmienne[0]) == str:
        wynik = ""
    else:
        wynik = 0
    for i in zmienne:
        wynik = wynik + i
    return wynik
def odejmij(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik - i
    return wynik
def dywizjuj(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik / i
    return wynik
def dywizjuj_calosc(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik // i
    return wynik
wykonaj_dzialanie = eval
konwersja_na_fj_z_kg = lambda x:x / 2137
konwersja_na_kg_z_fj = lambda x:x*2137

