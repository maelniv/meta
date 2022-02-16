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
PROBLEM = "MAX_ONE"
# PROBLEM = "TSP"

'''
Selection
'''
SELECTION = "Tournament"
# SELECTION = "Roulette_Wheel"
# SELECTION = "Rank_Based"

'''
REPLACEMENT
'''
# REPLACEMENT_STRATEGIE = "Generational"
REPLACEMENT_STRATEGIE = "Steady_State"
# REPLACEMENT_STRATEGIE = "Mixte"

'''
CONSTANT - GLOBAL
'''
SIZE_POPULATION = 200
NUMBER_SOLUTION_REPLACE = 100
NUMBER_FAMILY = int(NUMBER_SOLUTION_REPLACE / 2)
NUMBER_MAX_GENERATION = 2000
MUTATION = 10
ELITISM = 10
INDICE_CROSSOVER = 5


'''
CONSTANT - TOURNAMENT
'''
NUMBER_FINALIST = 10

'''
CONSTANT - RANK_BASED
'''
SELECTION_PRESSURE = 2

'''
CONSTANT - MAX_ONE
'''
SIZE_BINARY = 500
