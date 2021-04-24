from Cellular_Automata.SIR import Person_SIR, Automata_SIR
from Cellular_Automata.constant import *


import random
import pylab as plt
import numpy as np


if __name__ == "__main__":
    sir = Automata_SIR(10,10)
    days = 20
    for i in range(days):
        sir.nextGeneration()

    sir.printMatrix_multi()