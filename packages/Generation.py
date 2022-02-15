"""
Création d'un objet Génération permettant de stocker tous les individus
d'une génération.
"""
import random
from typing import List

from packages.Family import Family
import packages.constants as const


class Generation:
    def __init__(self, solution_list, generation_number):
        self.__solution_list = solution_list
        self.__generation_number = generation_number
        self.__tournament_schedule = []
        self.__list_of_winner = []
        self.__family_list = []
        self.__number_mutation = 0
        
        self.__best_solution = None
    
    def get_solution_list(self):
        return self.__solution_list

    def get_generation_number(self):
        return self.__generation_number
    
    def get_tournament_schedule(self):
        return self.__tournament_schedule
    
    def get_list_of_winner(self):
        return self.__list_of_winner
    
    def get_family_list(self):
        return self.__family_list
    
    def get_number_mutation(self):
        return self.__number_mutation
    
    def presentation_generation(self):
        for i in self.get_solution_list():
            print(i.presentation_solution())
            
    def presentation_winner(self):
        for i in self.get_list_of_winner():
            print(i.presentation_solution())
    
    def presentation_family(self):
        for i in self.get_family_list():
            i.presentation_family()
    
    def set_priority_three_best_solution(self):
        self.reset_priority()
        self.get_solution_list().sort(key=lambda x: x.get_distance(), reverse=True)
        self.get_solution_list()[0].set_priority(1)
        self.get_solution_list()[1].set_priority(1)
        self.get_solution_list()[2].set_priority(1)

    def reset_priority(self):
        for i in self.get_solution_list():
            i.set_priority(0)
            
    def set_tournament_schedule(self):
        if len(self.get_solution_list()) != const.SIZE_POPULATION:
            raise Exception("solution_list : {} != SIZE_POPULATION : {}".format(len(self.get_solution_list()), const.SIZE_POPULATION))
        if len(self.get_tournament_schedule()) == const.SIZE_TOURNAMENT:
            raise Exception("Le tournoi est déjà initialisé")
        
        tournament_schedule = random.sample(self.get_solution_list(), const.SIZE_TOURNAMENT)
        self.__tournament_schedule = tournament_schedule
    
    def del_tournament_schedule(self):
        self.__tournament_schedule = []
        
    def find_tournament_winner(self):
        if len(self.get_tournament_schedule()) != const.SIZE_TOURNAMENT:
            raise Exception("Le tournoi n'a pas été initialisé")
        if len(self.get_list_of_winner()) == const.NUMBER_TOURNAMENT_FOR_ONE_GENERATION:
            raise Exception("Les {} gagnant ont déjà été trouvés".format(const.NUMBER_TOURNAMENT_FOR_ONE_GENERATION))

        picked_solution = random.sample(self.get_tournament_schedule(), const.NUMBER_FINALIST)    
        picked_solution.sort(key=lambda x: x.get_distance(), reverse=False)
        self.__list_of_winner.append(picked_solution[0])
        self.del_tournament_schedule()

    def start_tournament(self):
        if len(self.get_list_of_winner()) == const.NUMBER_TOURNAMENT_FOR_ONE_GENERATION:
            raise Exception("Les {} gagnant ont déjà été trouvés".format(const.NUMBER_TOURNAMENT_FOR_ONE_GENERATION))
        
        while len(self.get_list_of_winner()) != const.NUMBER_TOURNAMENT_FOR_ONE_GENERATION:
            self.set_tournament_schedule()
            self.find_tournament_winner()
            
    def createFamily(self):
        if len(self.get_list_of_winner()) != const.NUMBER_TOURNAMENT_FOR_ONE_GENERATION:
            raise Exception("Les {} gagnant n'ont pas encore été trouvés".format(const.NUMBER_TOURNAMENT_FOR_ONE_GENERATION))
        if len(self.get_family_list()) == const.NUMBER_FAMILY:
            raise Exception("Les {} familles ont déjà été crées".format(const.NUMBER_FAMILY))
        
        for i in range(int(len(self.get_list_of_winner())/2)):
            family = Family(self.get_list_of_winner()[2*i], self.get_list_of_winner()[2*i+1])
            self.__family_list.append(family)
            
    def start_reproduction(self):
        if len(self.get_family_list()) != const.NUMBER_FAMILY:
            raise Exception("Les {} familles n'ont pas encore été crées".format(const.NUMBER_FAMILY))
        
        for i in self.get_family_list():
            self.__number_mutation += i.reproduction()
            
    def steady_state(self):
        for i in self.get_solution_list():
            tournois = self.get_tournament_schedule()
            tournois.index(i)
        
        
        
        
        
        
        self.set_priority_three_best_solution()
        for i in self.get_family_list():
            worst_parent = i.find_best_children_and_worst_parent()["worst_parent"]
            best_children = i.find_best_children_and_worst_parent()["best_children"]
            print(worst_parent)
            print(worst_parent.get_city_list())
            index_worst_parent = self.get_solution_list().index(worst_parent)
            self.get_solution_list()[index_worst_parent] = best_children
    
    def mean_distance(self):
        mean = 0
        for i in self.get_solution_list():
            mean += i.get_distance()
        return mean / const.SIZE_POPULATION