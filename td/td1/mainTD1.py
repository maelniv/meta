import numpy as np
import pandas as pd
import itertools
import td.constants as const


def mainTD1():
    print(const.DATA)
    inp_list = []
    shape = const.DATA.shape[0]
    print(shape)
    for i in range(shape):
        inp_list.append(i)
    permutations = list(itertools.permutations(inp_list))
    print(permutations)
    time = 1000000
    past = 0
    for cityList in permutations:
        temp = 0
        cityList = np.array(cityList)
        for city in cityList:
            if city != cityList[-1]:
                temp += const.DATA[city][cityList[list(cityList).index(city) + 1]]
            else:
                temp += const.DATA[city][cityList[0]]
        if temp < time:
            time = temp
            past = cityList

    print(time)
    print(past)
