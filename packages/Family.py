import random
import packages.constants as const

from packages.Solution import Solution

class Family:
    def __init__(self, parent1: Solution, parent2: Solution):
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
        self.__children1.set_individu_list(city_list)
        self.__children1.distance_calculation()
    
    def set_children2(self, city_list):
        self.__children2.set_individu_list(city_list)
        self.__children2.distance_calculation()
    
    def mutation(self, children):
        number_alea = random.randint(0,100)
        mutation = 0
        if number_alea < const.MUTATION:
            
            #Permutation
            if const.PROBLEM == "TSP":
                index1 = random.randint(0, const.NUMBER_INDIVIDU - 1)
                index2 = random.randint(0, const.NUMBER_INDIVIDU - 1)
                children[index1], children[index2] = children[index2], children[index1]
            
            #0 -> 1
            elif const.PROBLEM == "MAX_ONE":
                index_alea = random.randint(0, const.SIZE_BINARY - 1)
                children[index_alea] = (children[index_alea] + 1) % 2
            else:
                raise Exception("Aucun problème n'a été défini")
            mutation = 1
        return {"individu_list": children, "mutation": mutation}
    
    def find(self, part_one, part_two):
        for i in range(0, const.NUMBER_INDIVIDU):
            if i not in part_one and i not in part_two:
                return i
            
    def crossover(self, children_individu_list, parent_individu_list, indice):
        if const.PROBLEM == "TSP":
            for i in parent_individu_list[indice:]: 
                if i in children_individu_list:
                    children_individu_list.append(self.find(children_individu_list, parent_individu_list[indice:]))
                else:
                    children_individu_list.append(i)
            return children_individu_list
        elif const.PROBLEM == "MAX_ONE":
            return children_individu_list + parent_individu_list[indice:]
        else:
            raise Exception("Aucun problème n'a été défini")

    def reproduction(self):
        indice = const.INDICE_CROSSOVER
        
        city_list_children1_crossover = self.crossover(self.get_parent1().get_individu_list()[:indice], self.get_parent2().get_individu_list(), indice)
        children1_mutation = self.mutation(city_list_children1_crossover)
        city_list_children1_mutation = children1_mutation["individu_list"]
        self.set_children1(city_list_children1_mutation)
        
        city_list_children2_crossover = self.crossover(self.get_parent2().get_individu_list()[:indice], self.get_parent1().get_individu_list(), indice)
        children2_mutation = self.mutation(city_list_children2_crossover)
        city_list_children2_mutation = children2_mutation["individu_list"]
        self.set_children2(city_list_children2_mutation)
        
        return children1_mutation["mutation"] + children2_mutation["mutation"]
    
    def find_best_children(self):
        if const.PROBLEM == "TSP":
            best_children = self.get_children1() if self.get_children1().get_distance() < self.get_children2().get_distance() else self.get_children2()
            return best_children
        elif const.PROBLEM == "MAX_ONE":
            best_children = self.get_children1() if self.get_children1().get_distance() > self.get_children2().get_distance() else self.get_children2()
            return best_children
        else:
            raise Exception("Aucun problème n'a été défini")

            
    def find_worst_parent(self):
        if const.PROBLEM == "TSP":
            worst_parent = self.get_parent1() if self.get_parent1().get_distance() > self.get_parent2().get_distance() else self.get_parent2()
            return worst_parent
        elif const.PROBLEM == "MAX_ONE":
            worst_parent = self.get_parent1() if self.get_parent1().get_distance() < self.get_parent2().get_distance() else self.get_parent2()
            return worst_parent
        else:
            raise Exception("Aucun problème n'a été défini")