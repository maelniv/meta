import pandas as pd
import numpy as np
import random
import copy 

#On prend le mei+lleur parent et le meilleur enfant
#Ensuite on remplace dans la population de base les 50 nouveaux frérot en gardant les 3 meilleurs de l'ancienne génération (élitisme)

DATA = pd.read_csv("TSPDataset/gr17.2085.tsp",header=None,delim_whitespace=True)
SIZE_TOURNAMENT = 50
NUMBER_TOURNAMENT_FOR_ONE_GENERATION = 50
SIZE_POPULATION = 100
NUMBER_FINALIST = 3
NUMBER_CITIES = len(DATA)
NUMBER_MAX_GENERATION = 2

"""
Création d'un objet Solution pour stocker : 
- La liste des villes à visiter
- La distance totale du trajet
- Si la solution est à priorisé pour l'élitisme
"""
class Solution:
    def __init__(self, city_list):
        self.__city_list = city_list
        self.__distance = 0
        self.__priority = 0
    
    def presentation_solution(self):
        return "City List = {} | Distance = {}".format(self.get_city_list(), self.get_distance())

    def get_priority(self):
        return self.__priority
    
    def set_priority(self, new_priority):
        self.__priority = new_priority
    
    def get_city_list(self):
        return self.__city_list

    def get_distance(self):
        return self.__distance

    def add_city(self, city_list):
        self.__city_list += city_list
    
    def distance_calculation(self):
        distance = 0
        for city in self.get_city_list():
            index_next_city = self.get_city_list().index(city) + 1 if self.get_city_list().index(city) < (NUMBER_CITIES - 2) else 0
            distance += DATA[city][self.get_city_list()[index_next_city]]
        self.__distance = distance

class Family:
    def __init__(self, parent1, parent2):
        self.__parent1 = parent1
        self.__parent2 = parent2
        self.__children1 = Solution([])
        self.__children2 = Solution([])
    
    def presentation(self):
        print("Parent 1 : {}".format(self.get_parent1().presentation_solution()))
        print("Parent 2 : {}".format(self.get_parent2().presentation_solution()))
        print("Enfant 1 : {}".format(self.get_children1().presentation_solution()))
        print("Enfant 2 : {}".format(self.get_children2().presentation_solution()))

    def get_parent1(self):
        return self.__parent1

    def get_parent2(self):
        return self.__parent2

    def get_children1(self):
        return self.__children1

    def get_children2(self):
        return self.__children2
    
    def set_children1(self, city_list):
        self.__children1.add_city(city_list)
        self.__children1.distance_calculation()
    
    def set_children2(self, city_list):
        self.__children2.add_city(city_list)
        self.__children2.distance_calculation()
     
    def find(self,premiere_partie,deuxieme_partie):
        for i in range(1,NUMBER_CITIES):
            if i not in premiere_partie and i not in deuxieme_partie:
                return i
    
    def mutation(self, children):
        number1 = random.randint(0,100)
        if number1 < 5:
            number2 = random.randint(0, NUMBER_CITIES - 1)
            number3 = random.randint(0, NUMBER_CITIES - 1)
            children[number2], children[number3] = children[number3], children[number2]
        return children
    
    def crossover(self, children_city_list, parent_city_list, indice):
        for i in parent_city_list[indice:]: 
            if i in children_city_list:
               children_city_list.append(self.find(children_city_list,parent_city_list[indice:]))
            else:
                children_city_list.append(i)
        return children_city_list
        
    def reproduction(self):
        indice = 10
        children1_crossover = self.crossover(self.get_parent1().get_city_list()[:indice], self.get_parent2().get_city_list(), indice)
        children2_crossover = self.crossover(self.get_parent2().get_city_list()[:indice], self.get_parent1().get_city_list(), indice)
        self.set_children1(self.mutation(children1_crossover))
        self.set_children2(self.mutation(children2_crossover))
         
"""
Création d'un objet Génération permettant de stocker tous les individus
d'une génération.
"""
class Generation:
    def __init__(self, solution_list, generation_number):
        self.__solution_list = solution_list
        self.__generation_number = generation_number
        self.__best_solution = None
    
    def get_solution_list(self):
        return self.__solution_list

    def get_generation_number(self):
        return self.__generation_number
    
    def set_priority_three_best_solution(self):
        self.reset_priority()
        self.get_solution_list().sort(key=lambda x: x.get_distance(), reverse=True)
        self.get_solution_list()[0].set_priority(1)
        self.get_solution_list()[1].set_priority(1)
        self.get_solution_list()[2].set_priority(1)

    def reset_priority(self):
        for i in self.get_solution_list():
            i.set_priority(0)

"""
Instanciation des solutions avec leurs trajet et leurs distance calculé
"""
def new_random_solution():
    city_list = np.arange(1,NUMBER_CITIES)
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
    while len(population) != SIZE_POPULATION:
        population.append(new_random_solution())
    return population

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
    while actual_generation < NUMBER_MAX_GENERATION:
        generation = Generation(population, actual_generation)
        list_generation.append(generation)
        generation.set_priority_three_best_solution()
        list_of_winner=[]
        while len(list_of_winner) != NUMBER_TOURNAMENT_FOR_ONE_GENERATION:
            tournament_schedule = initialize_tournament(copy.deepcopy(population))
            list_of_winner.append(find_tournament_winner(tournament_schedule))
        family_list = createFamily(list_of_winner)
        family_list[0].reproduction()
        family_list[0].presentation()
        actual_generation+=1
        
if __name__ == '__main__':
    start_genetique()