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
    def __init__(self, numcols: int = 100, numrows: int = 100, zombieMode: bool = False, INIT_INFECTED=INIT_INFECTED, \
                 INFECTION_RATE=INFECTION_RATE, INCUBATION_DAYS=INCUBATION_DAYS, EXPOSED_RATE=EXPOSED_RATE, \
                 RECOVERY_RATE=RECOVERY_RATE, DEATH_RATE=DEATH_RATE, WEAR_MASK=WEAR_MASK, WEAR_MASK_POPULATION=WEAR_MASK_POPULATION, \
                 VACCINATED=VACCINATED, VACCINATED_POPULATION=VACCINATED_POPULATION, HOSPITALIZED=HOSPITALIZED, BEFORE_HOSPITAL=BEFORE_HOSPITAL):
        self.world = []
        self.rows = numrows
        self.cols = numcols
        self.time = 0
        self.people = []
        self.dead = []
        self.offices = []
        self.houses = []
        self.hospitals = []
        self.paths = []

        # Zombie Mode
        self.zombies = []
        self.zombieMode = zombieMode
        self.zombies_arr = []

        # Plotting Purposes - Keep Record of the number of SEIRD in every hour
        self.s_arr = []
        self.e_arr = []
        self.i_arr = []
        self.r_arr = []
        self.d_arr = []
        self.days = []
        self.mask_arr = []
        self.vaccinated_arr = []
        self.hospitalized_arr = []

        # Constants
        self.INIT_INFECTED = INIT_INFECTED
        self.INFECTION_RATE = INFECTION_RATE
        self.INCUBATION_DAYS = INCUBATION_DAYS
        self.EXPOSED_RATE = EXPOSED_RATE
        self.RECOVERY_RATE = RECOVERY_RATE
        self.DEATH_RATE = DEATH_RATE
        self.WEAR_MASK = WEAR_MASK
        self.WEAR_MASK_POPULATION = WEAR_MASK_POPULATION
        self.VACCINATED = VACCINATED
        self.VACCINATED_POPULATION = VACCINATED_POPULATION
        self.HOSPITALIZED = HOSPITALIZED
        self.BEFORE_HOSPITAL = BEFORE_HOSPITAL


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
        count = 0
        for i in range(num_people):
            chance = random.random()
            if chance <= self.INIT_INFECTED:
                # Infected -> State=2
                self.people.append(Person(id=i, state=2, prevState=2))
                count += 1
            else:
                # Susceptible -> State=0
                self.people.append(Person(id=i, state=0, prevState=0))
        if count == 0:
            self.people[0].setState(2)
            self.people[0].setPrevState(2)
        # print("Number of People: ", len(self.people))

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
                    self.world[randomRow][randomCol].init_CA(self.INFECTION_RATE, self.WEAR_MASK, self.VACCINATED)

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
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.world[i][j]:
                    self.world[i][j] = Path((i, j))
                    self.paths.append(self.world[i][j])

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

    def randomWalk(self):
        """
        All person walks from different starting point during each commute period
        - self.grid_location update
        """
        for p in self.people:
            # Check if the person is hospitalized. If yes, then the person doesn't walk
            if not p.getHospitalized():
                currX, currY = p.getGridLocation()
                newX, newY = currX + random.randint(-1, 1), currY + random.randint(-1, 1)
                while True:
                    if (currX, currY) != (newX, newY) and newX < self.rows and newX >= 0 and newY < self.cols and newY >= 0:
                        break
                    newX, newY = currX + random.randint(-1, 1), currY + random.randint(-1, 1)
                p.setGridLocation((newX, newY))

    def wearMask(self, currentDay:int):
        """
        Implement random portion of the people to wear mask
        Time: COMMUTE hours and OFFICE hours
        @rtn
        count: int (number of people wore mask)
        """
        # wear_rate = 0.01
        # new_wear_rate = 0.01 + 0.01*currentday
        total = 0
        if self.WEAR_MASK_POPULATION == 0:
            return
        percent = self.WEAR_MASK_POPULATION+(currentDay*0.01)
        for p in self.people:
            if not (p.getState() in [4,5]):
                chance = random.random()
                if chance <= percent:
                    p.setMask(True)
                if p.getMask():
                    total += 1
        self.mask_arr.append(total)
        # print(f"Mask Population: {total}")
        
    def takeDownMask(self):
        """
        Implement all people take dowm mask when returning their home
        Time: HOME hours
        """
        for p in self.people:
            p.setMask(False)

    def vaccinated(self):
        """
        Implement random portion of the people to get vaccinated
        @rtn
        count: int (number of people got vaccinated)
        """
        total = 0
        def filterVaccine(person):
            if (not person.getVaccinated() and person.getState() not in [3, 4, 5]):
                return True
            else:
                return False  
        new_people = list(filter(filterVaccine, self.people))

        for p in new_people:
            chance = random.random()
            if chance <= self.VACCINATED_POPULATION:
                p.setVaccinated(True)
                total += 1
        
        prev = 0 if len(self.vaccinated_arr) == 0 else self.vaccinated_arr[-1]
        self.vaccinated_arr.append(prev+total)
        # print("Vaccinated Population: ", total)

    def hospitalized(self):
        """
        Implement function to put infected population into hospital, hospitalized
        Time: HOME hour
        """
        def filterInfected(person):
            if person.getState() == 2:
                return True
            else:
                return False

        infected_pp = list(filter(filterInfected, self.people))
        
        for p in infected_pp:
            chance = random.random()
            if chance <= self.HOSPITALIZED:
                p.setHospitalized(True)
                p.setGridLocation(self.hospitals[0].getGridLocation())
                self.hospitals[0].checkIn(p)

    def checkOutHospital(self, currentHour, currentDay):
        """
        Implement people that are hospitalized can recover and return back home
        Time: HOME hour
        """
        patients = self.hospitals[0].getPatients()
        
        for p in patients:
            self.applyRules(p, currentHour, currentDay)
            # Check out recovered people from the hospital
            if (p.getState() == 3):
                house_loc = p.getHouse().getGridLocation()
                p.setGridLocation(house_loc)
                p.setHospitalized(False)
                self.hospitals[0].checkOut(p)
    
    def removeDead(self):
        """
        Removes dead people from associated locations
        including houses, offices, and hosptials
        """
        # inner function for filtering people in state 4 (Dead)
        def filterDead(person):
            if person.getState() == 4:
                return False
            else:
                return True
        # remove dead people
        for p in self.people:
            if p.getState() == 4:
                # Check if there are zombies in this world lol
                if self.zombieMode:
                    self.zombies.append(p)
                    self.checkOutZombie(p)
                else:
                    self.dead.append(p)
            self.people = list(filter(filterDead, self.people))
        # remove dead people from houses
        for h in self.houses:
            h_removed = list(filter(filterDead, h.getMembers()))
            h.setMembers(h_removed)
        # remove dead people from offices
        for o in self.offices:
            o_removed = list(filter(filterDead, o.getEmployees()))
            o.setEmployees(o_removed)
        # remove dead people from hospitals
        for hos in self.hospitals:
            hos_removed = list(filter(filterDead, hos.getPatients()))
            hos.setPatients(hos_removed)

    def nextGeneration(self):
        """
        1. Move to the "next" generation
        2. Time Check - Actions vary in differnt hour
            - 1900 - 0659 -> Home
            - 0700 - 0859 -> Commute (Random Walk)
            - 0900 - 1659 -> Work
            - 1700 - 1859 -> Commute / Happy (Random Walk)
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

        # 3. Update at 00:00
        if currentHour == 0:
            self.removeDead()
            if currentDay >= self.BEFORE_HOSPITAL: 
                self.hospitalized()
                self.checkOutHospital(currentHour, currentDay)
            self.accumulateData()
        
        # zombie walks around all the time
        if self.zombieMode:
            self.walkingDead()

        # Home
        if currentHour in HOME_TIME:
            # 1. Check current location:
            # Check time: 19:00 & the initial time (first hour of the first day)
            if currentHour == 19 or (currentHour == 0 and currentDay == 0):
                for person in self.people:
                    # Only Check People not in hospital from self.people
                    if not person.getHospitalized():
                        person.setGridLocation(person.getHouse().getGridLocation())

            # 2. Speard of virus at 00:00 per day
            if (currentHour%24) == 0:
                # print(f"Day: {currentDay}")
                for house in self.houses:
                    # Get healthy and infected people
                    healthyPeople = []
                    patients_mask = 0
                    patients_no_mask = 0
                    zombies = self.locatingZombies(house.getGridLocation(), currentHour)
                    for person in house.getMembers():
                        # Only Check People not in hospital from self.people
                        if not person.getHospitalized():
                            if person.getState() == 0 or person.getState() == 3:
                                healthyPeople.append(person)
                            elif person.getState() == 1 or person.getState() == 2:
                                if person.getMask():
                                    patients_mask += 1
                                else:
                                    patients_no_mask += 1
                                # Exposed or Infected Person could turn infected/recoverd/death
                                self.applyRules(person, currentHour, currentDay)

                    # Infect healthy people
                    for person in healthyPeople:
                        if self.zombieMode:
                            self.applyRules(person, currentHour, currentDay, patients_mask, patients_no_mask, zombies)
                        else:
                            self.applyRules(person, currentHour, currentDay, patients_mask, patients_no_mask)
            
            # 3. Wear mask before going to work
            if currentHour == 6:
                self.wearMask(currentDay)
            elif currentHour == 19:
                self.takeDownMask()
                self.vaccinated()

        # Commute
        elif currentHour in COMMUTE_TIME:
            # 1. Check current location
            self.randomWalk()
            # Let the walking dead rise
            if self.zombieMode:
                self.walkingDead()

            # 2. Spread of virus
            '''
            InfectedGrid (dict) store the
                key: location (tuple) 
                value: total number of infected people on that location
            If there is an exposed or infected person on that location, the value will plus 1.
            '''
            infectedGrid = {}
            for person in self.people:
                # Only Check People not in hospital from self.people
                if person.getState() in [1,2] and not person.getHospitalized():
                    if person.getGridLocation() not in infectedGrid.keys():
                        infectedGrid[person.getGridLocation()] = {"mask": 0, "no_mask": 0, "zombie": 0}
                    if person.getMask():
                        infectedGrid[person.getGridLocation()]["mask"] += 1
                    else:
                        infectedGrid[person.getGridLocation()]["no_mask"] += 1
            
            if self.zombieMode:
                infectedGrid = self.locatingZombies(infectedGrid, currentHour)

            '''
            Loop through each person. If the person is susceptible 
            and stand on same location with infected or exposed people, we applied the applyRules function
            '''
            for person in self.people:
                # Only Check People not in hospital from self.people
                if person.getState() in [0,3] and person.getGridLocation() in infectedGrid.keys() and not person.getHospitalized():
                    num_mask = infectedGrid[person.getGridLocation()]['mask']
                    num_no_mask = infectedGrid[person.getGridLocation()]['no_mask']
                    if self.zombieMode:
                        num_zombie = infectedGrid[person.getGridLocation()]['zombie']
                        if person.getState() == 3:
                            self.applyRules(person, currentHour, currentDay, num_Contact_zombie=num_zombie)
                        else:
                            self.applyRules(person, currentHour, currentDay, num_mask, num_no_mask, num_zombie)               
                    else:
                        self.applyRules(person, currentHour, currentDay, num_mask, num_no_mask)

        # Work
        elif currentHour in WORK_TIME:
            # 1. Check current location
            if currentHour == 9:
                for person in self.people:
                    # Only Check People not in hospital from self.people
                    if not person.getHospitalized():
                        person.setGridLocation(person.getOffice().getGridLocation())
            # 2. Spread of virus
            for office in self.offices:
                # CA Version
                if (currentHour%12)==0:
                    if (self.zombieMode):
                        num_zombies = self.locatingZombies(office.getGridLocation(), currentHour)
                        office.appendZombies(num_zombies)
                    else:
                        office.appendDummies()
                    office.getCA().updateGrid(office.getEmployees())
                    office.getCA().nextGeneration()
                    office.clearDummies()

        # 4. Time Progression (hourly)
        self.time += 1

    def applyRules(self, person:Person, currentHour:int, currentDay:int, num_Contact_withMask:int=0, num_Contact_noMask:int=0, num_Contact_zombie:int=0):
        """
        Rules of SEIRD model to apply for ABM
        @params:
        person: Person (individuals)
        currentHour: int (the current hour time)
        """
        chance = random.random()
        # Susceptible: 0
        if person.getPrevState() == 0:
            infected_rate = self.INFECTION_RATE
            if person.getMask():
                infected_rate *= self.WEAR_MASK
            if person.getVaccinated():
                infected_rate *= self.VACCINATED
            if chance > (1 - infected_rate*self.WEAR_MASK)**num_Contact_withMask * (1 - infected_rate)**(num_Contact_noMask + num_Contact_zombie):
                person.setState(1)
                # print("Exposed: S->E, Person: ", person.getID())
        
        elif currentHour == 0 and currentDay != 0:
            # Exposed: 1
            if person.getPrevState() == 1:
                if person.getIncubation() > 0:
                    person.decreaseIncubation()
                elif chance <= self.EXPOSED_RATE and person.getIncubation() == 0:
                    person.setState(2)
                    # print("Infected: E->I, Person: ", person.getID())

            # Infectious: 2
            elif person.getPrevState() == 2:
                # Version 1 
                if chance <= self.RECOVERY_RATE:
                    # Recovered: 3
                    person.setState(3)
                elif chance <= self.DEATH_RATE + self.RECOVERY_RATE:
                    # Dead: 4
                    person.setState(4)
                    if (self.zombieMode):
                        person.setZombie(True)
            
            # Recovered: 3 (Only effected in zombie mode)
            elif person.getPrevState() == 3 and self.zombieMode:
                infected_rate = self.INFECTION_RATE
                if person.getMask():
                    infected_rate *= self.WEAR_MASK
                if person.getVaccinated():
                    infected_rate *= self.VACCINATED
                if chance > (1 - infected_rate*self.WEAR_MASK)**num_Contact_withMask * (1 - infected_rate)**(num_Contact_noMask + num_Contact_zombie):
                    person.setState(1)
                # Version 2
                # if chance <= self.DEATH_RATE:
                #     # Dead: 4
                #     person.setState(4)
                # elif chance <= self.RECOVERY_RATE + self.DEATH_RATE:
                #     # Recovered: 3
                #     person.setState(3)


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
        if self.zombieMode:
            self.zombies_arr.append(self.getZ())

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

    def modelOutput(self, model_name: str) -> tuple:
        arr_dict = {}
        arr_dict["Susceptible"] = np.array(self.s_arr)
        arr_dict["Exposed"] = np.array(self.e_arr)
        arr_dict["Infected"] = np.array(self.i_arr)
        arr_dict["Recovered"] = np.array(self.r_arr)
        arr_dict["Dead"] = np.array(self.d_arr)
        arr_dict["Days"] = np.array(self.days)
        arr_dict["Mask"] = np.array(self.mask_arr)
        arr_dict["Vaccinated"] = np.array(self.vaccinated_arr)
        arr_dict["Hospitalized"] = np.array(self.hospitalized_arr)
        if self.zombieMode:
            arr_dict["Zombies"] = np.array(self.zombies_arr)
        return model_name, arr_dict

    def analysis(self, name):
        print(f"""
        {name}
        Highest Exposed Popluation: {max(self.getE_Arr())} at Day: {
             self.getE_Arr().index(max(self.getE_Arr()))}
        Highest Infected Popluation: {max(self.getI_Arr())} at Day: {
            self.getI_Arr().index(max(self.getI_Arr()))}
        Ratio of Susceptible Population: %.2f
        """ % ((self.getS_Arr()[-1]/1000)))


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
    
    def getHospital(self):
        return self.hospitals

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

    def getMask_Arr(self):
        if len(self.mask_arr) == 0:
            return [0]
        return self.mask_arr
    
    def getVaccinated_Arr(self):
        if len(self.vaccinated_arr) == 0:
            return [0]
        return self.vaccinated_arr
    
    def getHospitalized_Arr(self):
        if len(self.hospitalized_arr) == 0:
            return [0]
        return self.hospitalized_arr

    ########################################
    # Methods for Zombie Mode
    ########################################

    # For the walking deads
    def walkingDead(self):
        """
        There would be zombies walking around :)
        """
        for z in self.zombies:
            currX, currY = z.getGridLocation()
            newX, newY = currX + random.randint(-5, 5), currY + random.randint(-5, 5)
            while True:
                if (currX, currY) != (newX, newY) and newX < self.rows and newX >= 0 and newY < self.cols and newY >= 0:
                    break
                newX, newY = currX + random.randint(-1, 1), currY + random.randint(-1, 1)
            z.setGridLocation((newX, newY))


    def checkOutZombie(self, zombie:Person):
        """
        Checking zombie out of the hospital or home
        """
        def filterZombie(person):
            if person.getZombie():
                return False
            else:
                return True
        num_paths = len(self.paths)
        selected_path = random.randint(0, num_paths-1)
        zombie.setGridLocation(self.paths[selected_path].getGridLocation())
        if (zombie.getHospitalized()):
            zombie.setHospitalized(False)
            self.hospitals[0].checkOut(zombie)
        else:
            h_members = zombie.getHouse().getMembers()
            zombie.getHouse().leaveHouse(zombie)

    def locatingZombies(self, data, currentHour):
        if currentHour in COMMUTE_TIME:
            for zombie in self.zombies:
                if zombie.getGridLocation() not in data.keys():
                    data[zombie.getGridLocation()] = {"mask": 0, "no_mask": 0, "zombie": 1}
                else:
                    data[zombie.getGridLocation()]["zombie"] += 1
            return data
        elif currentHour in HOME_TIME:
            count = 0
            for z in self.zombies:
                if z.getHouse().getGridLocation() == data:
                    count += 1
            return count
        elif currentHour in WORK_TIME:
            count = 0
            for z in self.zombies:
                if z.getOffice().getGridLocation() == data:
                    count += 1
            return count

    def getZombies(self):
        return self.zombies

    def getZombies_Arr(self):
        return self.zombies_arr

    def getZ(self):
        return len(self.zombies)
