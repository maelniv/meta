import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import copy
import random


def aleatoire():
    s = []
    x = []
    for i in range(5):
        for i in range(5):
            s.append(random.randint(0, 1))
        x.append(s)
        s = []
    return x


def voisin(x):
    result = []
    for i in range(len(x)):
        result.append(copy.deepcopy(x))
        result[i][i] = (result[i][i] + 1) % 2
    return result


def binaire(x):
    s = []
    while x != 0:
        quotient = x // 2
        reste = x % 2
        if reste == 0:
            s.append(0)
        else:
            s.append(1)
        x = quotient
    s.reverse()
    return s


def voisin_new(x):
    result = []
    for i in range(len(x)):
        result.append(copy.deepcopy(x))
        result[i][i] = (result[i][i] + 1) % 2
    nombre = dec(x)
    bin = binaire(nombre - 1)
    result.append(bin)
    bin = binaire(nombre + 1)
    result.append(bin)
    return result


def dec(x):
    valeur = 0
    for i in range(len(x)):
        valeur = valeur + x[i] * 2 ** (len(x) - i - 1)
    return valeur


def resultat_dec(x):
    result = []
    for i in x:
        result.append(h(i))
    return result


def h(x):
    x = dec(x)
    return x ** 3 - 60 * (x ** 2) + 900 * x


def best(x_bin, x_resultdec):
    Max = max(x_resultdec)
    index = x_resultdec.index(Max)
    bin = x_bin[index]
    return bin


def mainTD2():
    x = []
    y = []
    cmp = 0
    Resultat_dec = resultat_dec(aleatoire())
    S = best(aleatoire(), Resultat_dec)
    y.append(h(S))
    x.append(dec(S))
    while True:
        Voisin = voisin_new(S)
        Resultat_dec = resultat_dec(Voisin)
        Best = best(Voisin, Resultat_dec)

        if (h(S) < h(Best)):
            S = Best
        else:
            break
        y.append(h(Best))
        x.append(dec(Best))
    plt.scatter(x, y)
    plt.show()
    print(dec(S))
    print(S)
    print(h(S))