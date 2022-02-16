"""
Création d'un objet Génération permettant de stocker tous les individus
d'une génération.
"""
from pickle import TRUE
import random
from typing import List

import numpy as np

from packages.Family import Family
import packages.constants as const


class Generation:
    def __init__(self, solution_list, generation_number):
        self.__solution_list = solution_list
        self.__generation_number = generation_number
        self.__selection_list = []
        self.__list_of_winner = []
        self.__family_list = []
        self.__number_mutation = 0
        self.__best_solution = None
    
    def get_best_solution(self):
        return self.__best_solution
    
    def get_solution_list(self):
        return self.__solution_list

    def get_generation_number(self):
        return self.__generation_number
    
    def get_selection_list(self):
        return self.__selection_list
    
    def del_selection_list(self):
        self.__selection_list = []

    def get_list_of_winner(self):
        return self.__list_of_winner
    
    def get_family_list(self):
        return self.__family_list
    
    def get_number_mutation(self):
        return self.__number_mutation
    
    def mean_distance(self):
        mean = 0
        for i in self.get_solution_list():
            mean += i.get_distance()
        return mean / const.SIZE_POPULATION

    def set_best_solution(self):
        if const.PROBLEM == "TSP":
            self.get_solution_list().sort(key=lambda x: x.get_distance(), reverse=False)
            self.__best_solution = self.get_solution_list()[0]
        elif const.PROBLEM == "MAX_ONE":
            self.get_solution_list().sort(key=lambda x: x.get_distance(), reverse=True)
            self.__best_solution = self.get_solution_list()[0]
        else:
            raise Exception("Aucun problème n'a été défini")
              
    def presentation_generation(self):
        for i in self.get_solution_list():
            print(i.presentation_solution())
            
    def presentation_winner(self):
        for i in self.get_list_of_winner():
            print(i.presentation_solution())
    
    def presentation_family(self):
        for i in self.get_family_list():
            i.presentation_family()
    
    def selection(self):
        if const.SELECTION == "Tournament":
            self.start_tournament()
        elif const.SELECTION == "Roulette_Wheel":
            self.roulette_wheel()
            print("temp")
        elif const.SELECTION == "Rank_Based":
            print("temp")
        else:
            raise Exception("Aucune méthode de selection n'est définie")
    
    '''
    Tournament
    '''
    
    def start_tournament(self):
        if len(self.get_list_of_winner()) == const.NUMBER_SOLUTION_REPLACE:
            raise Exception("Les {} gagnant ont déjà été trouvés".format(const.NUMBER_SOLUTION_REPLACE))
        
        while len(self.get_list_of_winner()) != const.NUMBER_SOLUTION_REPLACE:
            self.set_tournament_schedule()
            self.find_tournament_winner()

    def set_tournament_schedule(self):
        if len(self.get_solution_list()) != const.SIZE_POPULATION:
            raise Exception("solution_list : {} != SIZE_POPULATION : {}".format(len(self.get_solution_list()), const.SIZE_POPULATION))
        if len(self.get_selection_list()) == const.NUMBER_SOLUTION_REPLACE:
            raise Exception("Le tournoi est déjà initialisé")
        
        tournament_schedule = random.sample(self.get_solution_list(), const.NUMBER_SOLUTION_REPLACE)
        self.__selection_list = tournament_schedule
            
    def find_tournament_winner(self):
        if len(self.get_selection_list()) != const.NUMBER_SOLUTION_REPLACE:
            raise Exception("Le tournoi n'a pas été initialisé")
        if len(self.get_list_of_winner()) == const.NUMBER_SOLUTION_REPLACE:
            raise Exception("Les {} gagnant ont déjà été trouvés".format(const.NUMBER_SOLUTION_REPLACE))

        picked_solution = random.sample(self.get_selection_list(), const.NUMBER_FINALIST) 
        
        if const.PROBLEM == "TSP":   
            picked_solution.sort(key=lambda x: x.get_distance(), reverse=False)
        if const.PROBLEM == "MAX_ONE":
            picked_solution.sort(key=lambda x: x.get_distance(), reverse=True)
            
        self.__list_of_winner.append(picked_solution[0])
        self.del_selection_list()
    
    """
    Roulette
    """
            
    def roulette_wheel(self):
        random.choices(population=[1,2,3,4,5,6,7],weights=[1,1,1,1.5,1.5,3,3])
        print("temp")
            
            
            
    """"
    Reproduction
    """   
    
    def createFamily(self):
        if len(self.get_list_of_winner()) != const.NUMBER_SOLUTION_REPLACE:
            raise Exception("Les {} gagnant n'ont pas encore été trouvés".format(const.NUMBER_SOLUTION_REPLACE))
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
    
    """
    Replacement
    """
    
    def replacement(self):
        if const.REPLACEMENT_STRATEGIE == "Steady_State":
            self.steady_state_replacement()
        elif const.REPLACEMENT_STRATEGIE == "Generational":
            self.generationnal_replacement()
        elif const.REPLACEMENT_STRATEGIE == "Mixte":
            if self.get_generation_number() % 2 == 0:
                self.steady_state_replacement()
            else:
                self.generationnal_replacement()
        else:
            raise Exception ("Aucune stratégie de remplacement n'a été définie")
           
    def steady_state_replacement(self):
        for i in self.get_family_list():
            worst_parent = i.find_worst_parent()
            best_children = i.find_best_children()
            if worst_parent in self.get_solution_list():
                index_worst_parent = self.get_solution_list().index(worst_parent)
                self.get_solution_list()[index_worst_parent] = best_children
            else:
                self.get_solution_list().sort(key=lambda x: x.get_distance(), reverse=False)
                num = random.randint(const.ELITISM, const.SIZE_POPULATION - 1)
                self.get_solution_list()[num] = best_children
                   
    def generationnal_replacement(self):
        list_children = []
        self.get_solution_list().sort(key=lambda x: x.get_distance(), reverse=False)
        list_number = np.arange(const.ELITISM, const.SIZE_POPULATION)
        np.random.shuffle(list_number)
        list_number = list_number.tolist()
        for i in self.get_family_list():
            children1 = i.get_children1()
            children2 = i.get_children2()
            list_children.append(children1)
            list_children.append(children2)
        for i in range(const.NUMBER_SOLUTION_REPLACE):
            self.get_solution_list()[list_number[i]] = list_children[i]