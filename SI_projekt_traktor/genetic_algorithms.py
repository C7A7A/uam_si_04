import numpy as np
import math
from geneticalgorithm import geneticalgorithm as ga

def manhattan(src, dest):
    return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

def twodimensional(X):
    ind = 0
    for x in range(SIZE):
        for y in range(SIZE):
            tab[x][y] = X[ind]
            ind += 1

SIZE = 10
tab = [[0 for i in range(SIZE)] for j in range(SIZE)]

def f(X):
    pen = 0
    suma = 0
    twodimensional(X)
    if not (math.ceil((SIZE*SIZE*0.2)) <= sum(X) <= math.ceil((SIZE*SIZE*0.25))) or X[0] == 1:
        pen = SIZE*SIZE
    for x, row in enumerate(tab):
        for y, col in enumerate(row):
            if col == 1:
                suma -= manhattan((SIZE // 2 - 1, SIZE // 2 - 1), (x, y))
    return suma + pen*(10**6)


algorithm_param = {'max_num_iteration': 10000,
                   'population_size':1000,
                   'mutation_probability':0.35,
                   'elit_ratio': 0.01,
                   'crossover_probability': 0.5,
                   'parents_portion': 0.3,
                   'crossover_type':'uniform',
                   'max_iteration_without_improv':None}
model=ga(function=f,dimension=SIZE*SIZE, variable_type='bool', algorithm_parameters=algorithm_param)

model.run()
print(model.output_dict)
print(model.report)
with open("map.txt", 'w') as file:
    file.write(" ".join([str(int(x)) for x in np.ndarray.tolist(model.output_dict['variable'])]))