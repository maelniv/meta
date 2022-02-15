import random
import packages.constants as const

from packages.Solution import Solution

class Family:
    def __init__(self, parent1, parent2):
        self.__parent1 = parent1
        self.__parent2 = parent2
        self.__children1 = Solution([])
        self.__children2 = Solution([])
    
    def presentation_family(self):
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
    
    def mutation(self, children):
        number1 = random.randint(0,100)
        mutation = 0
        if number1 < 5:
            number2 = random.randint(0, const.NUMBER_CITIES - 1)
            number3 = random.randint(0, const.NUMBER_CITIES - 1)
            children[number2], children[number3] = children[number3], children[number2]
            mutation = 1
        return {"city_list": children, "mutation": mutation}
    
    def find(self,premiere_partie,deuxieme_partie):
        for i in range(0, const.NUMBER_CITIES):
            if i not in premiere_partie and i not in deuxieme_partie:
                return i
            
    def crossover(self, children_city_list, parent_city_list, indice):
        for i in parent_city_list[indice:]: 
            if i in children_city_list:
               children_city_list.append(self.find(children_city_list,parent_city_list[indice:]))
            else:
                children_city_list.append(i)
        return children_city_list
        
    def reproduction(self):
        indice = 10
        
        city_list_children1_crossover = self.crossover(self.get_parent1().get_city_list()[:indice], self.get_parent2().get_city_list(), indice)
        children1_mutation = self.mutation(city_list_children1_crossover)
        city_list_children1_mutation = children1_mutation["city_list"]
        self.set_children1(city_list_children1_mutation)
        
        city_list_children2_crossover = self.crossover(self.get_parent2().get_city_list()[:indice], self.get_parent1().get_city_list(), indice)
        children2_mutation = self.mutation(city_list_children2_crossover)
        city_list_children2_mutation = children2_mutation["city_list"]
        self.set_children2(city_list_children2_mutation)
        
        return children1_mutation["mutation"] + children2_mutation["mutation"]