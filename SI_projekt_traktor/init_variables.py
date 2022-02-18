import random
import global_variables as gb
import numpy as np
from Plants.plant import *
from Plants.carrot import Carrot
from Plants.potato import Potato
from Plants.tomato import Tomato
from Plants.wheat import Wheat
from Plants.fallow import Fallow
from tractor import Tractor
from Buildings.building import Building
from Buildings.fertilizer import Fertilizer
from Buildings.seeds import Seeds
from Buildings.water import Water
from Buildings.crops import Crops
from Obstacles.obstacle import Obstacle
from Obstacles.stone import Stone

def twodimensional(X):
    ind = 0
    for x in range(gb.WIDTH):
        for y in range(gb.HEIGHT):
            moles[x][y] = X[ind]
            ind += 1

field = [[Fallow() for i in range(WIDTH)] for j in range(HEIGHT)]
plants = [Carrot, Potato, Tomato, Wheat]
tractor = Tractor(plants)
moles = [[0 for i in range(gb.WIDTH)] for j in range(gb.HEIGHT)]
print(moles)
for counter in range(len(plants)):
    stats[plants[counter].plant_type] = 0

with open('map.txt', 'r') as f:
    for line in f:
        twodimensional(line.split())
for x, row in enumerate(moles):
    for y, col in enumerate(row):
        if int(col) == 1:
            field[x][y] = Stone()

field[WIDTH // 2 - 1][WIDTH // 2] = Water()
field[WIDTH // 2][WIDTH // 2 - 1] = Fertilizer()
field[WIDTH // 2][WIDTH // 2] = Crops()
field[WIDTH // 2 - 1][WIDTH // 2 - 1] = Seeds()

# for i in range(WIDTH//2 + 3):
#     x = random.randrange(WIDTH - 1)
#     y = random.randrange(HEIGHT - 1)
#     if isinstance(field[x][y], Fallow):
#         field[x][y] = Stone()
#field[WIDTH // 2][WIDTH // 2 + 1] = Stone()

for height in range(HEIGHT):
    for width in range(WIDTH):
        if isinstance(field[height][width], Fallow):
            field[height][width] = random.choice(plants)()
