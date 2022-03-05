import td.constants as const
##### Import files #####
import random
import matplotlib.pyplot as plt
import numpy as np


##### dataset functions #####
def load_data(file):
    data = []

    if 'random' in file:
        N_CITIES = int(file.split('_')[1])
        data = [[[] for _ in range(N_CITIES)] for _ in range(N_CITIES)]
        cities = []
        for i in range(N_CITIES):
            cities.append([random.randint(0, 100), random.randint(0, 100)])
        for i in range(N_CITIES):
            for j in range(N_CITIES):
                data[i][j] = distance(cities[i], cities[j])

    else:
        cities = None
        for line in open(file, 'r'):
            x = [float(i) for i in line.split()]
            if len(x) > 0:
                data.append(x)

    return data, cities


##### TSP functions #####
def distance(ville1, ville2):
    x = (ville1[0] - ville2[0]) ** 2
    y = (ville1[1] - ville2[1]) ** 2
    return (x + y) ** 0.5


def create_solution(N):
    individu = [i for i in range(N)]
    random.shuffle(individu)
    return individu


def get_fitness(individu, distances):
    length = 0
    for i in range(len(individu) - 1):
        length += distances[individu[i]][individu[i + 1]]
    length += distances[individu[0]][individu[-1]]
    return length


def get_neighbors(individu):
    # On permute une fois chaque ville
    neighbors = []
    for i in range(len(individu)):
        for j in range(len(individu)):
            if i != j:
                ind_bis = list(individu)
                ind_bis[i], ind_bis[j] = ind_bis[j], ind_bis[i]
                neighbors.append(ind_bis)
    return neighbors


def get_random_neighbor(individu):
    neighbors = []
    i = random.randint(0, len(individu) - 1)
    j = random.randint(0, len(individu) - 1)
    while i == j:
        j = random.randint(0, len(individu) - 1)
    ind_bis = list(individu)
    ind_bis[i], ind_bis[j] = ind_bis[j], ind_bis[i]
    return ind_bis


##### DIVERSIFICATION ET INTENSIFICATION #####


def update_intensification(matrix, s):
    matrix = matrix + 1
    mask = np.zeros((len(s), len(s)))
    for i in range(len(s)):
        mask[s[i], i] = 1
    # matrix = matrix + (mask-1)
    matrix = matrix * mask

    return matrix


def update_diversification(matrix, s):
    mask = np.zeros((len(s), len(s)))
    for i in range(len(s)):
        mask[s[i], i] = 1
    matrix = matrix + mask
    return matrix


def intensification(R, best_s, s, distances, treshold=0.3):
    # Get starting solution
    if R.sum() == 0:
        init_sol = best_s

    else:
        R_values = [R[s[i], i] for i in range(R.shape[0])]
        treshold = sorted(R_values, reverse=True)[int(treshold * R.shape[0])]
        available_cities = [i for i in range(R.shape[0])]
        init_sol = [-1 for _ in range(R.shape[0])]

        for i in range(R.shape[0]):
            for j in range(R.shape[1]):
                if R[i, j] >= treshold:
                    init_sol[j] = i
                    available_cities[i] = -1

        for i in range(len(init_sol)):
            if init_sol[i] == -1:
                c = random.choice(available_cities)
                while c in init_sol:
                    c = random.choice(available_cities)
                available_cities.remove(c)
                init_sol[i] = c

    # Start Local Search algo on init_sol
    new_sol = LocalSearch(init_sol, distances)
    if get_fitness(new_sol, distances) < get_fitness(best_s, distances):
        best_s = new_sol

    return best_s


def diversification(F, best_s, distances):
    # Get starting solution
    D = F.copy()
    init_sol = []
    max_coeff = D.max() + 1
    for col in range(D.shape[1]):
        min_indexs = np.where(D[:, col] == D[:, col].min())[0]
        index = random.choice(min_indexs)
        D[index, :] += max_coeff
        init_sol.append(index)

    # Start Simulated annealing algo on init_sol
    new_sol = SimulatedAnnealing(init_sol, distances, T0=500, n_iter_temp=200, n_iter=100)
    if get_fitness(new_sol, distances) < get_fitness(best_s, distances):
        best_s = new_sol

    return best_s


##### ALGORITHMES D'OPTIMISATION #####


def LocalSearch(s, distances):
    cond = True
    while cond:
        s_fit = get_fitness(s, distances)
        neighbors = get_neighbors(s)
        cond = False
        for neighbor in neighbors:
            f = get_fitness(neighbor, distances)
            if f < s_fit:
                cond = True
                s = list(neighbor)
                s_fit = f
    return s


def SimulatedAnnealing(s, distances, T0=500, n_iter_temp=200, n_iter=50):
    best_s = list(s)
    best_fit = get_fitness(best_s, distances)
    T = T0

    for temp_iter in range(n_iter_temp):
        for i in range(n_iter):
            s_new = get_random_neighbor(s)
            fs = get_fitness(s, distances)
            fnew = get_fitness(s_new, distances)

            if fnew < best_fit:
                best_fit = fnew
                best_s = s_new

            delta = fs - fnew
            if delta > 0:
                s = s_new
            else:
                prob = 2.71 ** (-abs(delta) / (T + 1e-5))
                if random.random() < prob:
                    s = s_new
        T = 0.9 * T

    return best_s


def TabuSearch(cities, distances, epochs=100, K=10):
    # Init values
    s = create_solution(len(distances))
    fit_s = get_fitness(s, distances)
    best_s = list(s)
    Tabulist = [best_s]
    hist_values = [best_s]

    # Init intens and divers
    F = np.zeros((len(distances), len(distances)))
    F = update_diversification(F, s)
    R = np.zeros((len(distances), len(distances)))
    R = update_intensification(R, s)

    # Loop over epochs
    for epoch in range(1, epochs + 1):
        # print ("******** ", get_fitness(best_s, distances))
        # Chose random neighbor
        neighbor = get_random_neighbor(s)

        fit_neighbor = get_fitness(neighbor, distances)
        fit_s = get_fitness(s, distances)

        if fit_neighbor < get_fitness(best_s, distances):
            best_s = list(neighbor)

        # On garde le voisin s'il est meilleur ou s'il n'est pas dans la liste taboue
        if fit_neighbor < fit_s or neighbor not in Tabulist:
            s = list(neighbor)
            Tabulist.append(s)
            if len(Tabulist) > K:
                Tabulist = Tabulist[1:]

        # Update diversification et intensification
        R = update_intensification(R, s)
        F = update_diversification(F, s)

        # Intensification : LSA
        if epoch % 1000 == 0:
            print('\ndans intensification')
            print('old fit : ', get_fitness(best_s, distances))
            best_s = intensification(R, best_s, s, distances, treshold=0.5)
            R = np.zeros((len(distances), len(distances)))
            print('new fit : ', get_fitness(best_s, distances))

        # Diversification : Recuit simulé
        if epoch % 1000 == 0:
            print('\ndans diversification')
            print('old fit : ', get_fitness(best_s, distances))
            best_s = diversification(F, best_s, distances)
            s = list(best_s)
            # F = np.zeros((len(distances), len(distances)))
            print('new fit : ', get_fitness(best_s, distances))

        hist_values.append(best_s)

    return best_s, hist_values, R, F


##### display function #####

def show_individual(individu, cities, lines=True):
    """ Show the road """

    if cities == None:
        return

    x = [cities[c][0] for c in individu]
    y = [cities[c][1] for c in individu]

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    if lines:
        ax.plot(x, y, color='black')
        ax.plot([x[0], x[-1]], [y[0], y[-1]], color='black')
    plt.show()
    return


##### Main #####

def mainTD5():
    ## file = './data/five.19.tsp'
    ## file = './data/br17.39.atsp'
    file = './data/gr17.2085.tsp'
    ## file = './data/p01.15.291.tsp'
    file = './data/att48.33523.tsp'

    distances, cities = load_data(file)

    # Parfois le best_s (sauvegardé dans l'historique) augmente au lieu de diminuer
    # C'est pas normal, je ne sais pas pourquoi il fait ça
    road, hist, intensification, diversification = TabuSearch(cities, distances, epochs=10000, K=20)
    plt.plot([i for i in range(len(hist))], [get_fitness(i, distances) for i in hist], label='tabu search')
    show_individual(road, cities)
    plt.show()

    print('best fitness : ', get_fitness(road, distances))






