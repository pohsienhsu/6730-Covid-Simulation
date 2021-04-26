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

class Person_SEIR(Person):
    def __init__(self, chance=INIT_INFECTED):
        super().__init__()
        if random.random() <= chance:
            self.state = 2
            self.prevState = 2
        else:
            self.prevState = 0
            self.state = 0

        
########################################################


class Automata_SEIR(Automata):
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
        -> getS, getI, getR => return integer S, I, R in the current day
        -> Store integer S I R to self.s_arr, self.i_arr, self.r_arr
        '''
        self.s_arr.append(self.getS())
        self.e_arr.append(self.getE())
        self.i_arr.append(self.getI())
        self.r_arr.append(self.getR())
        self.peopleStates_arr.append(self.getPeopleState())
        self.days.append(self.day)

    def plotCurve(self):
        fig, axes = plt.subplots(figsize=(4.5, 2.3), dpi=150)
        axes.plot(self.days, self.s_arr, '-', marker='.', color="b")
        axes.plot(self.days, self.e_arr, '-', marker='.', color=(1.0, 0.7, 0.0))
        axes.plot(self.days, self.i_arr, '-', marker='.', color="r")
        axes.plot(self.days, self.r_arr, '-', marker='.', color=(0.0,1.0,0.0))
        axes.set_xlabel("Days")
        axes.set_ylabel("Numbers of People")
        axes.set_title("SEIR Curve")
        axes.legend(["Susceptible", "Exposed", "Infected", "Recovered"])

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
                # iprevState = self.people[iprev][j].getPrevState()
                # inextState = self.people[inext][j].getPrevState()
                # jprevState = self.people[i][jprev].getPrevState()
                # jnextState = self.people[i][jnext].getPrevState()

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
        self.accumulateData()
        self.day += 1


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
                return
        
            # chanceRecovery = random.random()
            # if chanceRecovery <= RECOVERY_RATE:
            #     person.setState(3)
        
        # Infectious: 2
        elif person.prevState == 2:
            if chance <= RECOVERY_RATE:
                person.setState(3)
        
        # Recovered: 3
    
    def getPerson(self):
        return Person_SEIR()
