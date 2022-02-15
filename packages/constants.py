import pandas as pd

#DATA = pd.read_csv("data/p01.15.291.tsp",header=None,delim_whitespace=True)
DATA = pd.read_csv("data/gr17.2085.tsp",header=None,delim_whitespace=True)
#DATA = pd.read_csv("data/five.19.tsp",header=None,delim_whitespace=True)
#DATA = pd.read_csv("data/br17.39.atsp",header=None,delim_whitespace=True)

SIZE_TOURNAMENT = 6
NUMBER_TOURNAMENT_FOR_ONE_GENERATION = 6
NUMBER_FAMILY = int(NUMBER_TOURNAMENT_FOR_ONE_GENERATION/2)
SIZE_POPULATION = 100
NUMBER_FINALIST = 3
NUMBER_CITIES = len(DATA)
NUMBER_MAX_GENERATION = 2000
MUTATION = 10
INDICE_CROSSOVER = 10
ELITISM = 3

# REPLACEMENT_STRATEGIE = "Generational"
#REPLACEMENT_STRATEGIE = "Steady_State"
REPLACEMENT_STRATEGIE = "Mixte"
