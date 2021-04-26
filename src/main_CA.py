from Cellular_Automata.SIR import Person_SIR, Automata_SIR
from Cellular_Automata.SEIR import Person_SEIR, Automata_SEIR
from Cellular_Automata.SEIRD import Person_SEIRD, Automata_SEIRD
from Cellular_Automata.constant import *
from Visualization.Plotting_CA import *


import random
import pylab as plt
import numpy as np
plt.show()


seir = Automata_SEIR(100, 100)
print(f"Total People: {seir.numpeople}")
print(f"Initial Patient Number: {seir.getI()}")
for n in range(50):
    seir.nextGeneration()

mat_arr = []
days = [0, 4, 9, 14, 24, 49]
for i in days:
    mat_arr.append(seir.getPeopleStates_Arr()[i])

printMatrix_multi_CA(mat_arr=mat_arr, model="SEIR", day=days)
seir.plotCurve()