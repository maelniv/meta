import numpy as np
import random
import copy
import time

import matplotlib.pyplot as plt

import packages.constants as const
from packages.Generation import Generation 
from packages.Solution import Solution
from Plotable import Plotable

#On prend le mei+lleur parent et le meilleur enfant
#Ensuite on remplace dans la population de base les 50 nouveaux frérot en gardant les 3 meilleurs de l'ancienne génération (élitisme)

"""
Instanciation des solutions avec leurs trajet et leurs distance calculé
"""
def new_random_solution():
    if const.PROBLEM == "TSP":
        city_list = np.arange(0, const.NUMBER_INDIVIDU)
        np.random.shuffle(city_list)
        city_list = city_list.tolist()
        solution = Solution(city_list)
        solution.distance_calculation()
        return solution
    elif const.PROBLEM == "MAX_ONE":
        binaire = []
        for i in range(const.SIZE_BINARY):
            binaire.append(random.randint(0,1))
        solution = Solution(binaire)
        solution.distance_calculation()
        return solution
    else:
        raise Exception("Aucun problème n'a été défini")



"""
Création de la première génération de 100 individus
"""
def build_random_population():
    population = []
    while len(population) != const.SIZE_POPULATION:
        population.append(new_random_solution())
    return population    
    
"""
MAIN
"""
def start_genetique():
    start_time = time.time()
    
    list_generation = []
    actual_generation = 1  
    
    population = build_random_population()
    plot = Plotable()

    while actual_generation < const.NUMBER_MAX_GENERATION:
        generation = Generation(copy.deepcopy(population), actual_generation)
        list_generation.append(generation)
        
        generation.selection()
        generation.createFamily()
        generation.start_reproduction()        
        generation.replacement()
        generation.set_best_solution()
        
        plot.append_x_vals(actual_generation)
        plot.append_y_vals(generation.get_best_solution().get_distance())
        
        print("Generation : {0} | Best : {1} | Mean : {2:.2f}".format(generation.get_generation_number(), generation.get_best_solution().get_distance(), generation.mean_distance()))

        actual_generation += 1
        population = generation.get_solution_list()
        
        if const.PROBLEM == "MAX_ONE" and generation.get_best_solution().get_distance() == const.SIZE_BINARY:
            break
        
        if const.PROBLEM == "TSP" and generation.get_best_solution().get_distance() == const.TARGET:
            break
    
    duration = time.time() - start_time
    print("--- {0:.3f} seconds ---".format(duration))
    print("Best solution : {}".format(generation.get_best_solution().get_individu_list()))
    
    ax1.plot(plot.get_x_vals(),plot.get_y_vals())
    ax1.text(0.99,0.99,"{0:.3f} seconds".format(duration),
        verticalalignment='top', horizontalalignment='right',
        transform=ax1.transAxes,
        color='blue', fontsize=15)
    plt.show()

'''
Verification crossover < size individu
'''    
    
if __name__ == '__main__':
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    start_genetique()