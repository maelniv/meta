import pandas as pd
import numpy as np
import random
import copy 

#Deux parents -> Deux enfants
#On prend le meilleur parent et le meilleur enfant
#Ensuite on remplace dans la population de base les 50 nouveaux frérot en gardant les 3 meilleurs de l'ancienne génération (élitisme)

DATA = pd.read_csv("TSPDataset/gr17.2085.tsp",header=None,delim_whitespace=True)
SIZE_TOURNAMENT = 50
NUMBER_TOURNAMENT_FOR_ONE_GENERATION = 50
SIZE_POPULATION = 100
NUMBER_FINALIST = 3
NUMBER_CITIES = len(DATA)

"""
Création d'un objet Solution pour stocker : 
- La liste des villes à visiter
- La distance totale du trajet
- Si la solution est à priorisé pour l'élitisme
"""
class Solution:
    def __init__(self, city_list, distance):
        self.__city_list = city_list
        self.__distance = distance
        self.__priority = 0

    def get_priority(self):
        return self.__priority
    
    def get_city_list(self):
        return self.__city_list

    def get_distance(self):
        return self.__distance
    
    def set_priority(self, new_priority):
        self.__priority = new_priority

"""
Création d'un objet Génération permettant de stocker tous les individus
d'une génération.
"""
class Generation:
    def __init__(self, solution_list, generation_number):
        self.__solution_list = solution_list
        self.__generation_number = generation_number
    
    def get_solution_list(self):
        return self.__solution_list

    def get_generation_number(self):
        return self.__generation_number
    
    def find_three_best_solution(self):
        self.get_solution_list().sort(key=lambda x: x.get_distance(), reverse=True)
        print(self.get_solution_list()[0].get_distance())
        print(self.get_solution_list()[1].get_distance())
        print(self.get_solution_list()[2].get_distance())

    def reset_priority(self):
        for i in self.get_solution_list:
            i.set_priority(0)

"""
Instanciation des solutions avec leurs trajet et leurs distance calculé
"""
def new_random_solution():
    city_list = np.arange(1,NUMBER_CITIES)
    np.random.shuffle(city_list)
    city_list = city_list.tolist()
    solution = Solution(city_list, find_distance_for_one_solution(city_list))
    return solution

"""
Création de la première génération de 100 individus
"""
def build_random_population():
    population = []
    while len(population) != SIZE_POPULATION:
        population.append(new_random_solution())
    return population

"""
Calculer la fonction distance d'une solution
"""
def find_distance_for_one_solution(city_list):
    distance = 0
    for city in city_list:
        index_next_city = city_list.index(city) + 1 if city_list.index(city) < (NUMBER_CITIES - 2) else 0
        distance += DATA[city][city_list[index_next_city]]
    return distance

"""
Initialisation du tournoi avec une partie de la population (SIZE_TOURNAMENT)
"""
def initialize_tournament(population):
    tournament_schedule = get_new_list_from_other_list_with_alea(population, SIZE_TOURNAMENT)
    return tournament_schedule

"""
Récupération du gagnant du tournoi parmis 3 finalistes tiré aléatoirement
"""
def find_tournament_winner(tournament_schedule):
    picked_solution = get_new_list_from_other_list_with_alea(tournament_schedule, NUMBER_FINALIST)
    picked_solution.sort(key=lambda x: x.get_distance(), reverse=True)
    return picked_solution[0]

"""
Fonction pour créer une nouvelle liste aléatoirement en partant d'une liste définie
La nouvelle liste générée est sans doublon
"""
def get_new_list_from_other_list_with_alea(list, size_new_population):
    new_list = []
    while len(list) != size_new_population:
        size_population_remaining = len(list)
        index_chosen_solution = random.randint(0,size_population_remaining - 1)
        new_list.append(list[index_chosen_solution])
        list.pop(index_chosen_solution)
    return new_list

"""
MAIN
"""
def start_genetique():
    population = build_random_population()
    list_generation = []
    generation = Generation(population, 1)
    generation.find_three_best_solution()
    list_generation.append(generation)
    list_of_winner=[]
    while len(list_of_winner) != NUMBER_TOURNAMENT_FOR_ONE_GENERATION:
        tournament_schedule = initialize_tournament(copy.deepcopy(population))
        list_of_winner.append(find_tournament_winner(tournament_schedule))
    print(len(list_of_winner))
    
if __name__ == '__main__':
    start_genetique()