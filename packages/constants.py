import pandas as pd

'''
DATA
'''
#DATA = pd.read_csv("data/p01.15.291.tsp",header=None,delim_whitespace=True)
DATA = pd.read_csv("data/gr17.2085.tsp",header=None,delim_whitespace=True)
#DATA = pd.read_csv("data/five.19.tsp",header=None,delim_whitespace=True)
#DATA = pd.read_csv("data/br17.39.atsp",header=None,delim_whitespace=True)
NUMBER_INDIVIDU = len(DATA)

'''
PROBLEME
'''
# PROBLEM = "MAX_ONE"
PROBLEM = "TSP"

'''
Selection
'''
# SELECTION = "Tournament"
# SELECTION = "Roulette_Wheel"
SELECTION = "Rank_Based"

'''
REPLACEMENT
'''
# REPLACEMENT_STRATEGIE = "Generational"
REPLACEMENT_STRATEGIE = "Steady_State"
# REPLACEMENT_STRATEGIE = "Mixte"
#18.240
'''
CONSTANT - GLOBAL
'''
SIZE_POPULATION = 300
NUMBER_SOLUTION_REPLACE = 50
NUMBER_FAMILY = int(NUMBER_SOLUTION_REPLACE / 2)
NUMBER_MAX_GENERATION = 1000
MUTATION = 50
ELITISM = 3
INDICE_CROSSOVER = 10
PROCESSEUR = 2

'''
CONSTANT - TOURNAMENT
'''
NUMBER_FINALIST = 3

'''
CONSTANT - RANK_BASED
'''
SELECTION_PRESSURE = 1

'''
CONSTANT - MAX_ONE
'''
SIZE_BINARY = 500
