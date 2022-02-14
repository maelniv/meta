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
    city_list = np.arange(1, const.NUMBER_CITIES)
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
Initialisation du tournoi avec une partie de la population (SIZE_TOURNAMENT)
"""
def initialize_tournament(population):
    tournament_schedule = get_new_list_from_other_list_with_alea(population, const.SIZE_TOURNAMENT)
    return tournament_schedule

"""
Récupération du gagnant du tournoi parmis 3 finalistes tiré aléatoirement
"""
def find_tournament_winner(tournament_schedule):
    picked_solution = get_new_list_from_other_list_with_alea(tournament_schedule, const.NUMBER_FINALIST)
    picked_solution.sort(key=lambda x: x.get_distance(), reverse=False)
    return picked_solution[0]

"""
Fonction pour créer une nouvelle liste aléatoirement d'une taille voulue en partant d'une liste définie
La nouvelle liste générée est sans doublon
"""
def get_new_list_from_other_list_with_alea(list, size_new_population):
    new_list = []
    while len(new_list) != size_new_population:
        size_population_remaining = len(list)
        index_chosen_solution = random.randint(0,size_population_remaining - 1)
        new_list.append(list[index_chosen_solution])
        list.pop(index_chosen_solution)
    return new_list

def createFamily(list_of_parent):
    family_list = []
    for i in range(int(len(list_of_parent)/2)):
        family = Family(list_of_parent[2*i], list_of_parent[2*i+1])
        family_list.append(family)
    return family_list
    
"""
MAIN
"""
def start_genetique():
    population = build_random_population()
    list_generation = []
    actual_generation = 1
    
    while actual_generation < const.NUMBER_MAX_GENERATION:
        generation = Generation(population, actual_generation)
        list_generation.append(generation)
        generation.set_priority_three_best_solution()
        list_of_winner=[]
        
        while len(list_of_winner) != const.NUMBER_TOURNAMENT_FOR_ONE_GENERATION:
            tournament_schedule = initialize_tournament(copy.deepcopy(population))
            list_of_winner.append(find_tournament_winner(tournament_schedule))
            
        family_list = createFamily(list_of_winner)
        family_list[0].reproduction()
        family_list[0].presentation()
        actual_generation += 1
        
if __name__ == '__main__':
    start_genetique()