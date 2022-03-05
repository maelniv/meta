import copy
import random
import math


# PROBLEME DE MAXIMISATION


def mainTD3():
    s = [0, 0, 0, 1, 1]
    best_s = s
    temperature = 500
    init_temperature = 500
    i = 2
    while temperature > 150:
        condition = 0
        while condition < 5:
            rnd_voisin = voisin(s)
            deltaE = function(s) - function(rnd_voisin)
            if deltaE <= 0:
                s = rnd_voisin
                if function(s) > function(best_s):
                    best_s = s
            else:
                boltzman = math.exp(-(abs(deltaE) / temperature))
                choix = random.random()
                if boltzman < choix:
                    s = rnd_voisin
            condition += 1
        temperature = logarithmic(init_temperature, i)
        i += 1

    print(best_s)
    print(binaire_decimal(best_s))
    return best_s


def logarithmic(x, i):
    return x / math.log10(i)


def voisin(x):
    result = []
    for i in range(len(x)):
        result.append(copy.deepcopy(x))
        result[i][i] = (result[i][i] + 1) % 2
    return result[random.randint(0, len(result) - 1)]


def binaire_decimal(x):
    valeur = 0
    for i in range(len(x)):
        valeur = valeur + x[i] * 2 ** (len(x) - i - 1)
    return valeur


def decimal_binaire(x):
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


def function(x):
    return binaire_decimal(x) ** 3 - 60 * binaire_decimal(x) ** 2 + 900 * binaire_decimal(x) + 100
