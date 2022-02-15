"""
Création d'un objet Solution pour stocker : 
- La liste des villes à visiter
- La distance totale du trajet
"""

import packages.constants as const


class Solution:
    def __init__(self, city_list):
        self.__city_list = city_list
        self.__distance = 0
    
    def presentation_solution(self):
        return "City List = {} | Distance = {}".format(self.get_city_list(), self.get_distance())
    
    def get_city_list(self):
        return self.__city_list

    def get_distance(self):
        return self.__distance

    def add_city(self, city_list):
        self.__city_list += city_list
    
    def distance_calculation(self):
        distance = 0
        for city in self.get_city_list()[:-1]:
            index_next_city = self.get_city_list().index(city) + 1
            distance += const.DATA[city][self.get_city_list()[index_next_city]]
        distance += const.DATA[self.get_city_list()[-1]][self.get_city_list()[0]]
        self.__distance = distance