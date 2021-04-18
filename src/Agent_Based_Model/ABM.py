import pylab as plt
import numpy as np
import matplotlib.patches as mpatches
import random

from .Constant.constant import *
from .Agents.Person import Person
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
    def __init__(self, numcols: int = 100, numrows: int = 100):
        self.world = []
        self.rows = numrows
        self.cols = numcols
        self.time = 0
        self.people = []
        self.dead = []
        self.offices = []
        self.houses = []
        self.hospitals = []

        # Plotting Purposes - Keep Record of the number of SEIRD in every hour
        self.s_arr = []
        self.e_arr = []
        self.i_arr = []
        self.r_arr = []
        self.d_arr = []
        self.days = []

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
    def generate_coord(self) -> tuple:
        """
        generate random coordintates according to the rows and cols of the grid
        """
        return random.randint(0, self.rows-1), random.randint(0, self.cols-1)

    def createPeople(self, num_people: int):
        """
        Randomlize create people for ABM according to the params
        @params:
        num_people: int
        """
        for i in range(num_people):
            chance = random.random()
            if chance <= INIT_INFECTED:
                # Infected -> State=2
                self.people.append(Person(id=i, state=2, prevState=2))
            else:
                # Susceptible -> State=0
                self.people.append(Person(id=i, state=0, prevState=0))
        print("Number of People: ", len(self.people))

    def createHouse(self, num_people):
        """
        Randomlize create house for ABM according to the params
        @params:
        num_people: int
        (num_house = num_people/4)
        """
        for i in range(int(num_people/HOUSE_SIZE)):
            while True:
                randomRow, randomCol = self.generate_coord()
                if not self.world[randomRow][randomCol]:
                    # print(f"House: {i}, ({randomRow}, {randomCol})")
                    self.world[randomRow][randomCol] = House(i, (randomRow, randomCol))
                    self.houses.append(self.world[randomRow][randomCol])
                    self.world[randomRow][randomCol].setMembers(self.people[i*HOUSE_SIZE: HOUSE_SIZE*(i+1)])
                    for person in self.people[i*HOUSE_SIZE: HOUSE_SIZE*(i+1)]:
                        person.setHouse(self.world[randomRow][randomCol])
                    break

    def createOffice(self, num_people):
        """
        Randomlize create office for ABM according to the params
        @params:
        num_people: int
        (num_house = num_people/40)
        """
        arr = self.people.copy()
        random.shuffle(arr)
        for i in range(int(num_people/OFFICE_CAPACITY)):
            while True:
                randomRow, randomCol = self.generate_coord()
                if not self.world[randomRow][randomCol]:
                    # print(f"Office: {i}, ({randomRow}, {randomCol})")
                    self.world[randomRow][randomCol] = Office(id=i,grid_location=(randomRow, randomCol))
                    self.offices.append(self.world[randomRow][randomCol])
                    # 1. Fill in employees
                    self.world[randomRow][randomCol].setEmployees(arr[i*OFFICE_CAPACITY: OFFICE_CAPACITY*(i+1)])
                    # 2. Create CA in Office
                    self.world[randomRow][randomCol].init_CA()

                    for person in arr[i*OFFICE_CAPACITY: OFFICE_CAPACITY*(i+1)]:
                        person.setOffice(self.world[randomRow][randomCol])
                    break

    def createHospital(self, num_hospital=1):
        """
        Randomlize create hospital for ABM according to the params
        @params:
        num_hospital: int
        """
        for i in range(num_hospital):
            while True:
                randomRow, randomCol = self.generate_coord()
                if not self.world[randomRow][randomCol]:
                    # print(f"Hospital: {i}, ({randomRow}, {randomCol})")
                    self.world[randomRow][randomCol] = Hospital((randomRow, randomCol))
                    self.hospitals.append(self.world[randomRow][randomCol])
                    break

    def createPath(self):
        """
        Randomlize create path for ABM according to the params
        Fills in the rest of the empty cells on the grid
        """
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
        - Generate random Location Object (House, Office, Path)
            - Each object should cannot locate in the same cell.
            - House contains a fixed number (default=4) of Person as a family
            - Office contains a fixed number (default=40) of Person as a Company
        - Generate a fixed number (default=1000) of Person in the world
            - A part of the people are infected with COVID-19 in the first day
            - The number of the initial patients are decided by a rate in the constant, thus, the number varies in each simulation
        """
        self.createPeople(num_people)
        self.createHouse(num_people)
        self.createOffice(num_people)
        self.createHospital()
        self.createPath()


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

    def randomWalk(self):
        """
        All person walks from different starting point during each commute period
        - self.grid_location update
        """
        for p in self.people:
            currX, currY = p.getGridLocation()
            newX, newY = currX + random.randint(-1, 1), currY + random.randint(-1, 1)
            while True:
                if (currX, currY) != (newX, newY) and newX < self.rows and newX >= 0 and newY < self.cols and newY >= 0:
                    break
                newX, newY = currX + random.randint(-1, 1), currY + random.randint(-1, 1)
            p.setGridLocation((newX, newY))

    def timeAdvance(self):
        pass

    def wearMask(self):
        pass
    
    def getVaccinated(self):
        pass

    def removeDead(self, zombieMode=False):
        """
        Removes dead people from associated locations
        including houses, offices, and hosptials
        """
        # inner function for filtering people in state 4 (Dead)
        def findDead(person):
            if person.getState() == 4:
                return False
            else:
                return True
        # remove dead people
        if not zombieMode:
            for p in self.people:
                if p.getState() == 4:
                    self.dead.append(p)
                self.people = list(filter(findDead, self.people))
        # remove dead people from houses
        for h in self.houses:
            h_removed = list(filter(findDead, h.getMembers()))
            h.setMembers(h_removed)
        # remove dead people from offices
        for o in self.offices:
            o_removed = list(filter(findDead, o.getEmployees()))
            o.setEmployees(o_removed)
        # remove dead people from hospitals
        for hos in self.hospitals:
            hos_removed = list(filter(findDead, hos.getPatients()))
            hos.setPatients(hos_removed)


    def nextGeneration(self):
        """
        1. Move to the "next" generation
        2. Time Check - Actions vary in differnt hour
            - 1900 - 0700 -> Home
            - 0700 - 0900 -> Commute (Random Walk)
            - 0900 - 1700 -> Work
            - 1700 - 1900 -> Commute / Happy (Random Walk)
        3. Update at 00:00
            - Remove dead people
            - Get daily SEIRD data
            - Wear Mask/Get Vaccinated/Hospitalized
            - Recovery (Implemented in applyRules)
        4. Time Progression (hourly)
        """
        # 1. Move to the "next" generation
        for i in range(len(self.people)):
            self.people[i].copyState()
    
        # 2. Time Check - Actions vary in differnt hour
        currentDay = self.getDay()
        currentHour = self.getHour()
        print(f"Day{currentDay} at {currentHour}:00")

        # 3. Update at 00:00
        if currentHour == 0:
            self.removeDead()
            self.accumulateData()

        # Home
        if currentHour in HOME_TIME:
            # 1. Check current location:
            # Check time: 19:00 & the initial time (first hour of the first day)
            if currentHour == 19 or (currentHour == 0 and currentDay == 0):
                for person in self.people:
                    person.setGridLocation(person.getHouse().getGridLocation())

            # 2. Speard of virus
            if (currentHour%23) == 0:
                for house in self.houses:
                    # Get healthy and infected people
                    healthyPeople = []
                    patients = []
                    for person in house.getMembers():
                        if person.getState() == 0 or person.getState() == 3:
                            healthyPeople.append(person)
                        elif person.getState() == 1 or person.getState() == 2:
                            patients.append(person)
                            ABM.applyRules(person, currentHour, currentDay)
                    
                    # Infect healthy people
                    for person in healthyPeople:
                        ABM.applyRules(person, currentHour, currentDay, len(patients))
        
        # Commute
        elif currentHour in COMMUTE_TIME:
            # 1. Check current location
            self.randomWalk()

            # 2. Spread of virus
            '''
            InfectedGrid (dict) store the
                key: location (tuple) 
                value: total number of infected people on that location
            If there is an exposed or infected person on that location, the value will plus 1.
            '''
            infectedGrid = {}
            for person in self.people:
                if person.getState() == 1 or person.getState() == 2:
                    if person.getGridLocation() not in infectedGrid.keys():
                        infectedGrid[person.getGridLocation()] = 1
                    else:
                        infectedGrid[person.getGridLocation()] += 1
            '''
            Loop through each person. If the person is susceptible 
            and stand on same location with infected or exposed people, we applied the applyRules function
            '''
            for person in self.people:
                if person.getState() == 0 and person.getGridLocation() in infectedGrid.keys():
                    ABM.applyRules(person, currentHour, currentDay, infectedGrid[person.getGridLocation()])

        # Work
        elif currentHour in WORK_TIME:
            # 1. Check current location
            if currentHour == 9:
                for person in self.people:
                    person.setGridLocation(person.getOffice().getGridLocation())

            # 2. Spread of virus
            for office in self.offices:
                # Original Version
                # Get healthy and infected people
                # healthyPeople = []
                # patients = []
                # for person in office.getEmployees():
                #     if person.getState() == 0 or person.getState() == 3:
                #         healthyPeople.append(person)
                #     elif person.getState() == 1 or person.getState() == 2:
                #         patients.append(person)
                
                # # Infect healthy people
                # for person in healthyPeople:
                #     ABM.applyRules(person, currentHour, currentDay, len(patients))

                # CA Version
                if (currentHour%12)==0:
                    office.getCA().nextGeneration()
                # pass

        # 4. Time Progression (hourly)
        self.time += 1

    def applyRules(person:Person, currentHour:int, currentDay:int, num_Contact:int=0):
        """
        Rules of SEIRD model to apply for ABM
        @params:
        person: Person (individuals)
        currentHour: int (the current hour time)
        """
        chance = random.random()
        # Susceptible: 0
        if person.getPrevState() == 0:
            if chance > (1 - INFECTION_RATE)**num_Contact:
                person.setState(1)
                # print("Exposed: S->E, Person: ", person.getID())
        
        elif currentHour == 0 and currentDay != 0:
            # Exposed: 1
            if person.getPrevState() == 1:
                if person.getIncubation() > 0:
                    person.decreaseIncubation()
                elif chance <= EXPOSED_RATE and person.getIncubation() == 0:
                    person.setState(2)
                    print("Infected: E->I, Person: ", person.getID())

            # Infectious: 2
            elif person.getPrevState() == 2:
                if chance <= RECOVERY_RATE:
                    # Recovered: 3
                    person.setState(3)
                else:
                    chanceDeath = random.random()
                    if chanceDeath <= DEATH_RATE:
                        # Dead: 4
                        person.setState(4)


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
        self.days.append(self.getDay())

    def plotCurve(self):
        fig, axes = plt.subplots(figsize=(4.5, 2.3), dpi=150)
        axes.plot(self.days, self.s_arr, '-', marker='.', color="b")
        axes.plot(self.days, self.e_arr, '-', marker='.', color=(1.0, 0.7, 0.0))
        axes.plot(self.days, self.i_arr, '-', marker='.', color="r")
        axes.plot(self.days, self.r_arr, '-', marker='.', color=(0.0, 1.0, 0.0))
        axes.plot(self.days, self.d_arr, '-', marker='.', color=(0.5, 0, 0.5, 1))
        axes.set_xlabel("Days")
        axes.set_ylabel("Numbers of People")
        axes.set_title("SEIRD Curve")
        axes.legend(["Susceptible", "Exposed", "Infected", "Recovered", "Dead"])
        plt.show()


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

    def getPeopleState(self):
        peopleState = []
        for person in self.people:
             peopleState.append(person.getState())
        return np.array(peopleState)

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
        d = len(self.dead)
        # print("R: ", r)
        return d

    def getS_Arr(self):
        return self.s_arr

    def getE_Arr(self):
        return self.e_arr
    
    def getI_Arr(self):
        return self.i_arr

    def getR_Arr(self):
        return self.r_arr

    def getD_Arr(self):
        return self.d_arr
    
    def getDays_Arr(self):
        return self.days