import numpy as np
import random
import copy
import time

import packages.constants as const
from packages.Generation import Generation
from packages.Solution import Solution

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
    population = build_random_population()
    list_generation = []
    actual_generation = 1
    start_time = time.time()
    while actual_generation < const.NUMBER_MAX_GENERATION:
        generation = Generation(copy.deepcopy(population), actual_generation)
        list_generation.append(generation)
        generation.start_tournament()
        generation.createFamily()
        generation.start_reproduction()
        generation.replacement()
        generation.set_best_solution()
        
        print("Generation : {0} | Best : {1} | Mean : {2:.2f}".format(generation.get_generation_number(), generation.get_best_solution().get_distance(), generation.mean_distance()))
        actual_generation += 1
        population = generation.get_solution_list()
        
        if const.PROBLEM == "MAX_ONE" and generation.get_best_solution().get_distance() == const.SIZE_BINARY:
            print("--- {0:.3f} seconds ---".format(time.time() - start_time))
            print("Generation : {}".format(generation.get_generation_number()))
            break
                
    # print("best : {} mean : {}".format(generation.get_best_solution().get_distance(), generation.mean_distance()))

'''
Verification crossover < size individu
'''    
    
if __name__ == '__main__':
    start_genetique()