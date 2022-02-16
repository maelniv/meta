"""
Création d'un objet Solution pour stocker : 
- La liste des villes à visiter
- La distance totale du trajet
"""

import packages.constants as const


class Solution:
    def __init__(self, individu_list):
        self.__individu_list = individu_list
        self.__distance = 0

    def presentation_solution(self):
        return "Individu List = {} | Distance = {}".format(self.get_individu_list(), self.get_distance())
    
    def get_individu_list(self):
        return self.__individu_list

    def get_distance(self):
        return self.__distance

    def set_individu_list(self, individu_list):
        self.__individu_list = individu_list
    
    def set_distance(self, distance):
        self.__distance = distance
        
    def distance_calculation(self):
        if const.PROBLEM == "TSP":
            distance = 0
            for city in self.get_individu_list()[:-1]:
                index_next_city = self.get_individu_list().index(city) + 1
                distance += const.DATA[city][self.get_individu_list()[index_next_city]]
            distance += const.DATA[self.get_individu_list()[-1]][self.get_individu_list()[0]]
            self.set_distance(distance)
            
        elif const.PROBLEM == "MAX_ONE":
            sum = 0
            for bit in self.get_individu_list():
                sum += bit
            self.set_distance(sum)
            
        else:
            raise Exception("Aucun problème n'a été défini")
