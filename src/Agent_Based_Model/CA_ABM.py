import random

from Agent_Based_Model.Agents.Person import Person
from .Constant.constant import *

class Automata:
    def __init__(self, rows:int, cols:int, employees:list):
        self.rows = rows
        self.cols = cols
        self.numpeople = rows * cols
        self.people = []

        for i in range(rows):
            row = []
            for j in range(cols):
                person = employees[i*cols + j]    
                row.append(person) 
            self.people.append(row)
        
    def __repr__(self):
        return f"<Automata: shape=({self.rows},{self.cols})>"

    ########################################
    # Methods
    ########################################
    def updateGrid(self, employees):
        new_grid = []
        # Only Check People not in hospital from self.people
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                person = employees[i*self.cols + j]
                if not person.getHospitalized():
                    row.append(person)
                else:
                    # Append a dummy person instead
                    row.append(Person(-1, 5, 5))
                new_grid.append(row)

        self.people = new_grid

    def nextGeneration(self):
        """
        if Top, down, left, right is infected 
            -> the center person will be infected by a chance of INFECTION_RATE
        """
        for i in range(self.rows):
            for j in range(self.cols):
                infectedNeighbors_mask, infectedNeighbors_no_mask = 0, 0
                iprev, inext, jprev, jnext = i - 1, i + 1, j - 1, j + 1

                if (jprev >= 0 and (self.people[i][jprev].getPrevState() == 1 or self.people[i][jprev].getPrevState() == 2)):
                    if (self.people[i][jprev].getMask()):
                        infectedNeighbors_mask += 1
                    else:
                        infectedNeighbors_no_mask += 1
                if (jnext < self.cols and ( self.people[i][jnext].getPrevState() == 2 or self.people[i][jnext].getPrevState() == 1)):
                    if (self.people[i][jnext].getMask()):
                        infectedNeighbors_mask += 1
                    else:
                        infectedNeighbors_no_mask += 1
                if (iprev >= 0 and ( self.people[iprev][j].getPrevState() == 2 or self.people[iprev][j].getPrevState() == 1)):
                    if (self.people[iprev][j].getMask()):
                        infectedNeighbors_mask += 1
                    else:
                        infectedNeighbors_no_mask += 1
                if (inext < self.rows and ( self.people[inext][j].getPrevState() == 2 or self.people[inext][j].getPrevState() == 1)):
                    if (self.people[inext][j].getMask()):
                        infectedNeighbors_mask += 1
                    else:
                        infectedNeighbors_no_mask += 1

                currPerson = self.people[i][j]
                self.applyRulesOfInfection(currPerson, infectedNeighbors_mask, infectedNeighbors_no_mask)

        # self.day += 1

    def applyRulesOfInfection(self, person:Person, infectedNeighbors_mask:int=0, infectedNeighbors_no_mask:int=0):
        chance = random.random()

        # Susceptible: 0
        if person.prevState == 0:
            if infectedNeighbors_mask > 0 or infectedNeighbors_no_mask > 0:
                infected_rate = INFECTION_RATE
                if person.getMask():
                    infected_rate *= WEAR_MASK
                if person.getVaccinated():
                    infected_rate *= VACCINATED
                if chance > (1 - infected_rate*WEAR_MASK)**infectedNeighbors_mask * (1 - infected_rate)**infectedNeighbors_no_mask:
                    person.setState(1)
    