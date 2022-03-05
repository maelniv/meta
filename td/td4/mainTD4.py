import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import copy

import td.constants as const

print(const.DATA)
taille_tabu = 3


def generate_number():
    s = np.arange(0, const.NUMBER_INDIVIDU)
    np.random.shuffle(s)
    return s.tolist()


def voisin(x):
    neighbors = []
    for i in range(len(x)):
        for j in range(i, len(x)):
            if j > i:
                neighbors.append(copy.deepcopy(x))
                neighbors[-1][j], neighbors[-1][i] = neighbors[-1][i], neighbors[-1][j]
    return neighbors


def distance(x):
    sum = 0
    for j in x[:-1]:
        sum = sum + const.DATA[j][x[x.index(j) + 1]]
    sum += const.DATA[x[-1]][x[0]]
    return sum


def indice(last, new):
    result = []
    for i in range(len(new)):
        if last[i] != new[i]:
            result.append(i)
    return result


def add_tabu(last, new, tabu_list):
    attribut = indice(last, new)
    print(f" last : {last} new : {new} attribut : {attribut}")
    if len(tabu_list) == taille_tabu:
        for i in range(taille_tabu - 1):
            tabu_list[i] = tabu_list[i + 1]
        tabu_list[taille_tabu - 1] = attribut
    else:
        tabu_list.append(attribut)


def is_in_tabu(last, new, tabu_list):
    changement = indice(last, new)
    for i in range(len(tabu_list)):
        if tabu_list[i] == changement:
            return True
    return False


def chose_neighbors(neighbors_list):
    return neighbors_list[random.randint(0, len(neighbors_list) - 1)]


def mainTD4():
    inp_list = generate_number()
    tabu_list = []
    best = inp_list
    solution_s = inp_list
    do = True

    for i in range(2000):
        if do:
            neighbors_list = voisin(solution_s)
        chosen_neighbors = chose_neighbors(neighbors_list)
        chosen_neighbors_distance = distance(chosen_neighbors)

        # si dans tabu list mais nieghboor<last alors on remplace sinon on prend un nv voisin
        # si pas dans tabu list alors neighboor devient last et si meilleur que bestN on remplace
        # on met a jour la tabu list

        if is_in_tabu(solution_s, chosen_neighbors, tabu_list):
            if chosen_neighbors_distance < distance(solution_s):
                solution_s = chosen_neighbors
                do = True
            else:
                do = False
                neighbors_list.remove(chosen_neighbors)
                # Suppr chosen_neighbors
        else:
            do = True
            add_tabu(solution_s, chosen_neighbors, tabu_list)
            solution_s = chosen_neighbors

        if chosen_neighbors_distance < distance(best):
            best = chosen_neighbors

    print(best)
    print(distance(best))
    print(tabu_list)
