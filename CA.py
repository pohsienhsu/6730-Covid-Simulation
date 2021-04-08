import random
import pylab as plt
import numpy as np
import matplotlib.patches as mpatches


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
    def __init__(self):
        self.prevState = 0
        self.state = 0
        # if random.random() <= 0.01:
        #     self.state = 1
        # else:

    def __repr__(self):
        return f"<Person: state{self.state}>"

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

        self.people = []
        # Make a (column) list.

        # Create Patient 0
        # Location: Row & Col
        patient0Row = 4
        patient0Col = 5

        for i in range(numcols):
            column = []
            # Make a list of (row) cells for each column
            for j in range(numrows):
                # Create Patient 0
                if i == patient0Row and j == patient0Col:
                    # Got you
                    person = self.getPerson()
                    person.setState(1)
                    person.setPrevState(1)
                else:
                    person = self.getPerson()
                column.append(person)
            self.people.append(column)

    def __repr__(self):
        return f"<Automata: shape=({self.rows},{self.cols})>"

    def printMatrix(self):
        mat = []
        for i in range(self.rows):
            column = []
            for j in range(self.cols):
                column.append(self.people[i][j].getState())
            # print(f"Row: {i}, Column: {column}")
            mat.append(column)

        cmap = {0: [0.1, 0.1, 1.0, 1], 
                1: [1.0, 0.1, 0.1, 1], 
                2: [1.0, 0.5, 0.1, 1]}
                
        labels = {0: 'Susceptible', 1: 'Infected', 2: 'Recovered'}
        arrayShow = np.array([[cmap[i] for i in j] for j in mat])
        patches = [mpatches.Patch(color=cmap[i], label=labels[i])
                   for i in cmap]
        plt.imshow(arrayShow)
        plt.legend(handles=patches, title="Status",
                   loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax = plt.gca()
        # ax.set_xticks([x-0.5 for x in range(1, self.cols)], minor=True)
        # ax.set_yticks([y-0.5 for y in range(1, self.rows)], minor=True)
        ax.set_xticks(np.arange(-.5, 10, 1))
        ax.set_yticks(np.arange(-.5, 10, 1))
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        plt.grid(which="major",color='k', ls="-",lw=2)

    def getPerson(self):
        return Person()

    # Subclasses will override this method in order to
    # position the shapes that represent the cells.
    def initGraphics(self):
        print("Warning: Automata.initGraphics() is not implemented!")

    def getPeople(self):
        return self.people

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
                iprev = i - 1
                inext = i + 1
                jprev = j - 1
                jnext = j + 1

                """
                <Example>
                Current: 
                    Center(5, 5) -> (i, j)
                Neighbor: 
                    Top(5, 4) -> (i, j - 1) -> self.people[i][jprev]
                    Down(5, 6) -> (i, j + 1) -> self.people[i][jnext]
                    Left(4, 5) -> (i - 1, j) -> self.people[iprev][j]
                    Right(3, 5) -> (i + 1, j) -> self.people[inext][j]
                """
                if (jprev >= 0 and self.people[i][jprev].getPrevState() == 1):
                    infectedNeighbors += 1
                if (jnext < self.rows and self.people[i][jnext].getPrevState() == 1):
                    infectedNeighbors += 1
                if (iprev >= 0 and self.people[iprev][j].getPrevState() == 1):
                    infectedNeighbors += 1
                if (inext < self.cols and self.people[inext][j].getPrevState() == 1):
                    infectedNeighbors += 1

                # for i,neighbor in enumerate(neighborIndex):
                #     if neighbor < 0:
                #         continue
                #     elif (i==1 and i >= self.rows) or (i == 3 and i>= self.cols):
                #         continue
                #     else:
                #         infectedNeighbors += 1

                currPerson = self.people[i][j]
                Automata.applyRulesOfInfection(
                    self, currPerson, infectedNeighbors)

    def applyRulesOfInfection(self, person, infectedNeighbors):
        chance = random.random()

        if person.prevState == 0:
            if infectedNeighbors >= 1:
                if (chance > (1-INFECTION_RATE)**infectedNeighbors):
                    person.setState(1)
        elif person.prevState == 1:
            if chance <= RECOVERY_RATE:
                person.setState(2)


if __name__ == "__main__":
    automata = Automata(10, 10)
    for n in range(5):
        automata.nextGeneration()
    automata.printMatrix()
    plt.show()
