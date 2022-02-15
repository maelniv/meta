from operator import ge
import numpy as np
import random
import copy

import packages.constants as const
from packages.Family import Family
from packages.Generation import Generation
from packages.Solution import Solution

#On prend le mei+lleur parent et le meilleur enfant
#Ensuite on remplace dans la population de base les 50 nouveaux frérot en gardant les 3 meilleurs de l'ancienne génération (élitisme)

"""
Instanciation des solutions avec leurs trajet et leurs distance calculé
"""
def new_random_solution():
    city_list = np.arange(0, const.NUMBER_CITIES)
    np.random.shuffle(city_list)
    city_list = city_list.tolist()
    solution = Solution(city_list)
    solution.distance_calculation()
    return solution

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
    population = build_random_population()
    list_generation = []
    actual_generation = 1
    
    while actual_generation < const.NUMBER_MAX_GENERATION:
        generation = Generation(copy.deepcopy(population), actual_generation)
        list_generation.append(generation)
        generation.start_tournament()
        generation.createFamily()
        generation.start_reproduction()
        generation.replacement()
        generation.set_best_solution()
        
        print("best : {} mean : {}".format(generation.get_best_solution(), generation.mean_distance()))
        actual_generation += 1
        population = generation.get_solution_list()
    
    generation.presentation_generation()
if __name__ == '__main__':
    start_genetique()