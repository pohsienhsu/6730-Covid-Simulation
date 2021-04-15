import pylab as plt
import numpy as np
import matplotlib.patches as mpatches
import random

from .Constant.constant import *
from .Agents.Person import Person
from .Agents.Company import Company
from .Agents.Family import Family
from .Location.Path import Path
from .Location.Hospital import Hospital
from .Location.House import House
from .Location.Office import Office

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

class ABM:
    def __init__(self, numcols:int = 100, numrows:int = 100):
        self.world = []
        self.rows = numrows
        self.cols = numcols
        self.time = 0
        self.people = []
        self.companies = []
        self.families = []

        # Plotting Purposes - Keep Record of the number of SEIRD in every hour
        self.s_arr = []
        self.e_arr = []
        self.i_arr = []
        self.r_arr = []
        self.d_arr = []

        for i in range(self.rows):
            column = []
            for j in range(self.cols):
                column.append(None)
            self.world.append(column)

    def __repr__(self):
        return f"<ABM: shape=({self.rows},{self.cols})>"

    ########################################
    # Methods
    ########################################
    def createPeople(self, num_people):
        for i in range(num_people):
            chance = random.random()
            if chance <= INIT_INFECTED:
                # Infected -> State=2
                self.people.append(Person(id=i, state=2, prevState=2))
            else:
                # Susceptible -> State=0
                self.people.append(Person(id=i, state=0, prevState=0))
        # print("Number of People: ", len(self.people))

    def createHouse(self, num_people):
        for i in range(int(num_people/HOUSE_SIZE)):
            while True:
                randomRow = random.randint(0, self.rows-1)
                randomCol = random.randint(0, self.cols-1)
                if not self.world[randomRow][randomCol]:
                    # print(f"House: {i}, ({randomRow}, {randomCol})")
                    self.world[randomRow][randomCol] = House(i, (randomRow, randomCol))
                    self.world[randomRow][randomCol].setMembers(self.people[i*HOUSE_SIZE: HOUSE_SIZE*(i+1)])
                    for person in self.people[i*HOUSE_SIZE: HOUSE_SIZE*(i+1)]:
                        person.setHouse(self.world[randomRow][randomCol])
                    break
    
    def createOffice(self, num_people):
        arr = self.people.copy()
        random.shuffle(arr)
        for i in range(int(num_people/OFFICE_CAPACITY)):
            while True:
                randomRow = random.randint(0, self.rows-1)
                randomCol = random.randint(0, self.cols-1)
                if not self.world[randomRow][randomCol]:
                    # print(f"Office: {i}, ({randomRow}, {randomCol})")
                    self.world[randomRow][randomCol] = Office(i, (randomRow, randomCol))
                    self.world[randomRow][randomCol].setEmployees(arr[i*OFFICE_CAPACITY: OFFICE_CAPACITY*(i+1)])
                    for person in arr[i*OFFICE_CAPACITY: OFFICE_CAPACITY*(i+1)]:
                        person.setOffice(self.world[randomRow][randomCol])
                    break

    def createHospital(self, num_hospital=1):
        for i in range(num_hospital):
            while True:
                randomRow = random.randint(0, self.rows-1)
                randomCol = random.randint(0, self.cols-1)
                if not self.world[randomRow][randomCol]:
                    # print(f"Hospital: {i}, ({randomRow}, {randomCol})")
                    self.world[randomRow][randomCol] = Hospital((randomRow, randomCol))
                    return
    
    def createPath(self):
        count = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.world[i][j]:
                    # print(f"Path: {count}, ({i}, {j})")
                    self.world[i][j] = Path((i, j))
                    count += 1
    
    def createWorld(self, num_people):
        """
        Hello World!
        * Generate random Location Object (House, Office, Path)
            - Each object should cannot locate in the same cell.
            - House contains a fixed number (default=4) of Person as a family
            - Office contains a fixed number (default=40) of Person as a Company
        * Generate a fixed number (default=1000) of Person in the world
            - A part of the people are infected with COVID-19 in the first day
            - The number of the initial patients are decided by a rate in the constant, thus, the number varies in each simulation
        """
        self.createPeople(num_people)
        self.createHouse(num_people)
        self.createOffice(num_people)
        self.createHospital(num_people)
        self.createPath()

    def getPeopleState(self):
        mat = []
        for i in range(self.rows):
            column = []
            for j in range(self.cols):
                column.append(self.people[i][j].getState())
            # print(f"Row: {i}, Column: {column}")
            mat.append(column)
        return np.array(mat)

    # def printMatrix(self, cmap, labels, model="SIR"):
    #     mat = self.getPeopleState()

    #     arrayShow = np.array([[cmap[i] for i in j] for j in mat])
    #     patches = [mpatches.Patch(color=cmap[i], label=labels[i])
    #                for i in cmap]
    #     plt.imshow(arrayShow)
    #     plt.legend(handles=patches, title="Status",
    #                loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    #     ax = plt.gca()
    #     ax.set_xticks(np.arange(-.5, self.rows, 1))
    #     ax.set_yticks(np.arange(-.5, self.cols, 1))
    #     ax.xaxis.set_ticklabels([])
    #     ax.yaxis.set_ticklabels([])
    #     plt.grid(which="major",color='k', ls="-",lw=(200/(self.rows * self.cols)))
    #     plt.title(f"Covid-19 Spread Situation - {model}\n Day: {self.day}")

    def accumulateData(self):
        '''
        Each Day:
        -> getS, getE, getI, getR, getD => return integer S, E, I, R, D in the current day
        -> Store integer S E I R D to self.s_arr, self.e_arr, self.i_arr, self.r_arr, self.d_arr
        '''
        self.s_arr.append(self.getS())
        self.e_arr.append(self.getE())
        self.i_arr.append(self.getI())
        self.r_arr.append(self.getR())
        self.d_arr.append(self.getD())
        self.days.append(self.day)

    def plotCurve(self):
        fig, axes = plt.subplots(figsize=(4.5, 2.3), dpi=150)
        axes.plot(self.days, self.s_arr, '-', marker='.', color="b")
        axes.plot(self.days, self.e_arr, '-', marker='.', color=(1.0, 0.7, 0.0))
        axes.plot(self.days, self.i_arr, '-', marker='.', color="r")
        axes.plot(self.days, self.r_arr, '-', marker='.', color=(0.0,1.0,0.0))
        axes.plot(self.days, self.d_arr, '-', marker='.', color=(0.5, 0, 0.5, 1))
        axes.set_xlabel("Days")
        axes.set_ylabel("Numbers of People")
        axes.set_title("SEIRD Curve")
        axes.legend(["Susceptible", "Exposed", "Infected", "Recovered", "Dead"])

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
    
    ########################################
    # Getters & Setters
    ########################################

    def getWorld(self):
        return self.world

    def getDay(self):
        return self.time//24

    def getHour(self):
        return self.time%24
    
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
    