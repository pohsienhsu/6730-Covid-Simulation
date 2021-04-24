from .CA import Person, Automata
from .constant import *

import random
import pylab as plt


'''

Model 101 <SEIR/Automata>

1. State:
-> Susceptible: 0
-> Exposed: 1
-> Infected: 2 (-> Death Rate: 0.05)
-> Recovered: 3


2. Infection Rate:
-> rate = 0.5 (default)

3. Pattern:
    How to decide whether a person will have a chance to get infected by neighbors?
    -> Top, down, left, right if infected then the person is exposed with a rate of 0.5

4. Analysis:
-> Print Matrix with imshow
-> Print SEIR curve

'''


class Person_SEIRS(Person):
    def __init__(self, chance=INIT_INFECTED):
        super().__init__()
        if random.random() <= chance:
            self.state = 2
            self.prevState = 2
        else:
            self.prevState = 0
            self.state = 0


########################################################


class Automata_SEIRS(Automata):
    def __init__(self, numcols, numrows):
        super().__init__(numcols, numrows)

        # Plotting Purposes
        self.s_arr = []
        self.e_arr = []
        self.i_arr = []
        self.r_arr = []
        self.days = []

    def accumulateData(self):
        '''
        Each Day:
        -> getS, getE, getI, getR => return integer S, E, I, R in the current day
        -> Store integer S E I R to self.s_arr, self.e_arr, self.i_arr, self.r_arr
        '''
        self.s_arr.append(self.getS())
        self.e_arr.append(self.getE())
        self.i_arr.append(self.getI())
        self.r_arr.append(self.getR())
        self.peopleStates_arr.append(self.getPeopleState())
        self.days.append(self.day)

    def plotCurve(self):
        fig, axes = plt.subplots()
        axes.plot(self.days, self.s_arr, '-', marker='.', color="b")
        axes.plot(self.days, self.e_arr, '-',
                  marker='.', color=(1.0, 0.7, 0.0))
        axes.plot(self.days, self.i_arr, '-', marker='.', color="r")
        axes.plot(self.days, self.r_arr, '-',
                  marker='.', color=(0.0, 1.0, 0.0))
        axes.set_xlabel("Days")
        axes.set_ylabel("Numbers of People")
        axes.set_title("SEIRS Curve")
        axes.legend(["Susceptible", "Exposed", "Infected", "Recovered"])

    def applyRulesOfInfection(self, person, infectedNeighbors):
        chance = random.random()

        # Susceptible: 0
        if person.prevState == 0:
            if infectedNeighbors >= 1:
                if (chance > (1-INFECTION_RATE)**infectedNeighbors):
                    person.setState(1)

        # Exposed: 1
        elif person.prevState == 1:
            if person.getIncubation() > 0:
                person.setIncubation(person.getIncubation() - 1)
            elif chance <= EXPOSED_RATE and person.getIncubation() == 0:
                person.setState(2)

            if chance <= RECOVERY_RATE:
                person.setState(3)

        # Infectious: 2
        elif person.prevState == 2:
            if chance <= RECOVERY_RATE:
                person.setState(3)

        # Recovered: 3
        elif person.prevState == 3:
            if chance <= SUSCEPTIBLE_RATE:
                person.setState(0)

    def getPerson(self):
        return Person_SEIRS()
