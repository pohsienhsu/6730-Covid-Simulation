import random
import pylab as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.colors as colors




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
###############################
# Constant
INIT_INFECTED = 0.01
INFECTION_RATE = 0.5
RECOVERY_RATE = 0.1
DEATH_RATE = 0.05
###############################


class Person:
    def __init__(self, chance=INIT_INFECTED):
        if random.random() <= chance:
            self.state = 1
            self.prevState = 1
        else:
            self.prevState = 0
            self.state = 0

    def __repr__(self):
        return f"<Person: state={self.state}>"

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getPrevState(self):
        return self.prevState

    def setPrevState(self, state):
        self.prevState = state

    def copyState(self):
        self.prevState = self.state

########################################################


class Automata:
    def __init__(self, numcols, numrows):
        self.rows = numrows
        self.cols = numcols
        self.numpeople = numrows * numcols
        self.day = 0

        # Plotting Purposes
        self.s_arr = []
        self.i_arr = []
        self.r_arr = []
        self.days = []

        self.people = []

        for i in range(numcols):
            column = []
            # Make a list of (row) cells for each column
            for j in range(numrows):
                person = self.getPerson()
                
                column.append(person)
            self.people.append(column)

    def __repr__(self):
        return f"<Automata: shape=({self.rows},{self.cols})>"

    def getPeopleState(self):
        mat = []
        for i in range(self.rows):
            column = []
            for j in range(self.cols):
                column.append(self.people[i][j].getState())
            # print(f"Row: {i}, Column: {column}")
            mat.append(column)
        return np.array(mat)


    def printMatrix(self):
        mat = self.getPeopleState()

        # cmap = color map
        cmap = {0: [0.0, 0.0, 1.0, 1], 
                1: [1.0, 0.0, 0.0, 1], 
                2: [0.0, 1.0, 0.0, 1]}
                
        labels = {0: 'Susceptible', 1: 'Infected', 2: 'Recovered'}
        arrayShow = np.array([[cmap[i] for i in j] for j in mat])
        patches = [mpatches.Patch(color=cmap[i], label=labels[i])
                   for i in cmap]
        plt.imshow(arrayShow)
        plt.legend(handles=patches, title="Status",
                   loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax = plt.gca()
        ax.set_xticks(np.arange(-.5, self.rows, 1))
        ax.set_yticks(np.arange(-.5, self.cols, 1))
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        plt.grid(which="major",color='k', ls="-",lw=(200/(self.rows * self.cols)))
        plt.title(f"Covid-19 Spread Situation - SIR\n Day: {self.day}")


    def accumulateSIR(self):
        '''
        Each Day:
        -> getS, getI, getR => return integer S, I, R in the current day
        -> Store integer S I R to self.s_arr, self.i_arr, self.r_arr
        '''
        self.s_arr.append(self.getS())
        self.i_arr.append(self.getI())
        self.r_arr.append(self.getR())
        self.days.append(self.day)

    def printSIR(self):
        fig, axes = plt.subplots()
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
        return Person()

    def getPeople(self):
        return self.people

    def getS(self):
        s = np.count_nonzero(self.getPeopleState() == 0)
        # print("S: ", s)
        return s

    def getI(self):
        i = np.count_nonzero(self.getPeopleState() == 1)
        # print(f"I: {i}")
        return i

    def getR(self):
        r = np.count_nonzero(self.getPeopleState() == 2)
        # print("R: ", r)
        return r

if __name__ == "__main__":
    automata = Automata(100, 100)
    automata.printMatrix()
    print(f"Total People: {automata.numpeople}")
    print(f"Initial Patient Number: {automata.getI()}")
    automata.accumulateSIR()
    for n in range(50):
        automata.nextGeneration()
        automata.accumulateSIR()
    # automata.printMatrix()
    automata.printSIR()
    plt.show()