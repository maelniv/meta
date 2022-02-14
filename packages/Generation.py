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