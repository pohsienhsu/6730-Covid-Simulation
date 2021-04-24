from .CA import Person, Automata
from .constant import *

import random
import pylab as plt
import numpy as np


'''

Model 101 <SIR/Automata>

1. State:
-> Susceptible: 0
-> Infected: 1 (-> Death Rate: 0.05)
-> Recovered: 2

2. Infection Rate:
-> rate = 0.5 (default)

3. Pattern:
    How to decide whether a person will have a chance to get infected by neighbors?
    -> Top, down, left, right if infected then the person is exposed with a rate of 0.5

4. Analysis:
-> Print Matrix with imshow
-> Print SIR curve

'''
if __name__ == "__main__":
    sir = Automata_SIR()
    days = 20
    for i in range(days):
        sir.nextGeneration()

    sir.printMatrix_multi()


class Person_SIR(Person):
    def __init__(self, chance=INIT_INFECTED):
        super().__init__()
        if random.random() <= chance:
            self.state = 1
            self.prevState = 1


########################################################


class Automata_SIR(Automata):
    def __init__(self, numcols, numrows):
        super().__init__(numcols, numrows)

        # Plotting Purposes
        self.s_arr = []
        self.i_arr = []
        self.r_arr = []
        self.days = []


    def accumulateData(self):
        '''
        Each Day:
        -> getS, getI, getR => return integer S, I, R in the current day
        -> Store integer S I R to self.s_arr, self.i_arr, self.r_arr
        '''
        self.s_arr.append(self.getS())
        self.i_arr.append(self.getI())
        self.r_arr.append(self.getR())
        self.days.append(self.day)
        self.peopleStates_arr.append(self.getPeopleState())


    def plotCurve(self):
        fig, axes = plt.subplots(figsize=(4.5, 2.3), dpi=150)
        axes.plot(self.days, self.s_arr, '-', marker='.', color="b")
        axes.plot(self.days, self.i_arr, '-', marker='.', color="r")
        axes.plot(self.days, self.r_arr, '-', marker='.', color=(0.0,1.0,0.0))
        axes.set_xlabel("Days")
        axes.set_ylabel("Numbers of People")
        axes.set_title("SIR Curve")
        axes.legend(["Susceptible", "Infected", "Recovered"])

    
    def nextGeneration(self):
        # Move to the "next" generation
        for i in range(self.cols):
            for j in range(self.rows):
                self.people[i][j].copyState()

        """
        if Top, down, left, right is infected 
            -> the center person will be infected by a chance of INFECTION_RATE
        """
        for i in range(self.cols):
            for j in range(self.rows):
                infectedNeighbors = 0
                iprev, inext, jprev, jnext = i - 1, i + 1, j - 1, j + 1

                if (jprev >= 0 and self.people[i][jprev].getPrevState() == 1):
                    infectedNeighbors += 1
                if (jnext < self.rows and self.people[i][jnext].getPrevState() == 1):
                    infectedNeighbors += 1
                if (iprev >= 0 and self.people[iprev][j].getPrevState() == 1):
                    infectedNeighbors += 1
                if (inext < self.cols and self.people[inext][j].getPrevState() == 1):
                    infectedNeighbors += 1

                currPerson = self.people[i][j]
                self.applyRulesOfInfection(currPerson, infectedNeighbors)
        
        self.accumulateData()
        self.day += 1

    
    def applyRulesOfInfection(self, person, infectedNeighbors):
        chance = random.random()

        if person.prevState == 0:
            if infectedNeighbors >= 1:
                if (chance > (1-INFECTION_RATE)**infectedNeighbors):
                    person.setState(1)
        elif person.prevState == 1:
            if chance <= RECOVERY_RATE:
                person.setState(2)
    
    def getPerson(self):
        return Person_SIR()


    def getI(self):
        i = np.count_nonzero(self.getPeopleState() == 1)
        # print(f"I: {i}")
        return i

    def getR(self):
        r = np.count_nonzero(self.getPeopleState() == 2)
        # print("R: ", r)
        return r
