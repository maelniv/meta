import pandas as pd

DATA = pd.read_csv("data/gr17.2085.tsp",header=None,delim_whitespace=True)
SIZE_TOURNAMENT = 50
NUMBER_TOURNAMENT_FOR_ONE_GENERATION = 50
NUMBER_FAMILY = int(NUMBER_TOURNAMENT_FOR_ONE_GENERATION/2)
SIZE_POPULATION = 100
NUMBER_FINALIST = 3
NUMBER_CITIES = len(DATA)
NUMBER_MAX_GENERATION = 2