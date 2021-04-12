import random
import pylab as plt
import numpy as np
import matplotlib.patches as mpatches
from constant import *

'''
<Agent Based Model - Cellular Automata/SEIRD>

Time: Hour-Based
1900 - 0700 -> Home
0700 - 0900 -> Commute (Random Walk)
0900 - 1700 -> Work 
1700 - 1900 -> Commute / Happy (Random Walk)

<Agent>
# Random Walk Reference
self.x
self.y

# Location (Maybe not related to the grid geo)
self.home
self.work
self.hospital<Not infectious>

# State(SIR)
self.state
(Infectious: Asym, Hospitalized)
self.age_group(child, adult, elder)

# PPE
self.mask
self.vaccinated

'''

class Person:
    def __init__(self):
        self.incubation = INCUBATION_DAYS
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

    def getIncubation(self):
        return self.incubation

    def setIncubation(self, incubation):
        self.incubation = incubation

        
########################################################

'''
<Model>
1. SIR
2. SEIR
3. SEIRS
4. SEIRD
5. SEIRSD
'''
class Automata:
    def __init__(self, numcols, numrows):
        self.rows = numrows
        self.cols = numcols
        self.numpeople = numrows * numcols
        self.day = 0

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


    def printMatrix(self, cmap, labels, model="SIR"):
        mat = self.getPeopleState()

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
        plt.title(f"Covid-19 Spread Situation - {model}\n Day: {self.day}")


    def accumulateData(self):
        pass

    def plotCurve(self):
        pass

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

                if (jprev >= 0 and (self.people[i][jprev].getPrevState() == 1 or self.people[i][jprev].getPrevState() == 2)):
                    infectedNeighbors += 1
                if (jnext < self.rows and ( self.people[i][jnext].getPrevState() == 2 or self.people[i][jnext].getPrevState() == 1)):
                    infectedNeighbors += 1
                if (iprev >= 0 and ( self.people[iprev][j].getPrevState() == 2 or self.people[iprev][j].getPrevState() == 1)):
                    infectedNeighbors += 1
                if (inext < self.cols and ( self.people[inext][j].getPrevState() == 2 or self.people[inext][j].getPrevState() == 1)):
                    infectedNeighbors += 1

                currPerson = self.people[i][j]
                self.applyRulesOfInfection(currPerson, infectedNeighbors)

        self.day += 1


    def applyRulesOfInfection(self, person, infectedNeighbors):
        pass
    
    def getPerson(self):
        return Person()

    def getPeople(self):
        return self.people

    def getS(self):
        s = np.count_nonzero(self.getPeopleState() == 0)
        # print("S: ", s)
        return s
    
    def getE(self):
        e = np.count_nonzero(self.getPeopleState() == 1)
        # print("E: ", e)
        return e

    def getI(self):
        i = np.count_nonzero(self.getPeopleState() == 2)
        # print(f"I: {i}")
        return i

    def getR(self):
        r = np.count_nonzero(self.getPeopleState() == 3)
        # print("R: ", r)
        return r

    def getD(self):
        d = np.count_nonzero(self.getPeopleState() == 4)
        # print("R: ", r)
        return d
    