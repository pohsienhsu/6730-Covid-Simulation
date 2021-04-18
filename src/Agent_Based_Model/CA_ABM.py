import random

from Agent_Based_Model.Agents.Person import Person
from .Constant.constant import *

class Automata:
    def __init__(self, rows:int, cols:int, employees:list):
        self.rows = rows
        self.cols = cols
        self.numpeople = rows * cols

        self.people = []
        print("Employees Length: ", len(employees))
        for i in range(rows):
            row = []
            for j in range(cols):
                print(f"Location ({i}, {j})")
                person = employees[i*cols + j]
                row.append(person)
            self.people.append(row)
        
    def __repr__(self):
        return f"<Automata: shape=({self.rows},{self.cols})>"

    ########################################
    # Methods
    ########################################
    def nextGeneration(self):
        # Move to the "next" generation
        # for i in range(self.cols):
        #     for j in range(self.rows):
        #         self.people[i][j].copyState()
        """
        if Top, down, left, right is infected 
            -> the center person will be infected by a chance of INFECTION_RATE
        """
        for i in range(self.rows):
            for j in range(self.cols):
                infectedNeighbors = 0
                iprev, inext, jprev, jnext = i - 1, i + 1, j - 1, j + 1

                if (jprev >= 0 and (self.people[i][jprev].getPrevState() == 1 or self.people[i][jprev].getPrevState() == 2)):
                    infectedNeighbors += 1
                if (jnext < self.cols and ( self.people[i][jnext].getPrevState() == 2 or self.people[i][jnext].getPrevState() == 1)):
                    infectedNeighbors += 1
                if (iprev >= 0 and ( self.people[iprev][j].getPrevState() == 2 or self.people[iprev][j].getPrevState() == 1)):
                    infectedNeighbors += 1
                if (inext < self.rows and ( self.people[inext][j].getPrevState() == 2 or self.people[inext][j].getPrevState() == 1)):
                    infectedNeighbors += 1

                currPerson = self.people[i][j]
                self.applyRulesOfInfection(currPerson, infectedNeighbors)

        # self.day += 1

    def applyRulesOfInfection(self, person:Person, infectedNeighbors:int):
        chance = random.random()

        # Susceptible: 0
        if person.prevState == 0:
            if infectedNeighbors >= 1:
                if (chance > (1-INFECTION_RATE)**infectedNeighbors):
                    # print("Exposed: S->E, Person: ", person.getID())
                    person.setState(1)
    