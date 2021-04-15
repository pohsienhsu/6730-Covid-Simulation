from ..Constant.constant import *

class Person:
    """
    class Person:
        Serving as an agent in the ABM. 
        Each Person would represent each individuals within our simulation.

    @attrs: 
    state: int (0: susceptible, 1: exposed, 2: infectious, 3: recovered, 4: dead)
    prevState: int
    grid_location: tuple (ex. (x,y))
    medical: dict (ex. {mask: False, vaccinated: False, hospitalized: False, incubation: 0})
    """
    def __init__(self, id:int, state:int, prevState:int, medical:dict={}):
        self.id = id
        self.state = state
        self.prevState = prevState
        self.grid_location = None
        self.association = {"office": None, "house": None}
        if (medical):
            self.medical = {
                "mask": False,
                "vaccinated": False,
                "hospitalized": False,
                "incubation": 7
            }
        else:
            self.medical = medical

    def __repr__(self):
        return f"<Person: id={id(self)} state={self.state} loc={self.grid_location}>"

    ########################################
    # Methods
    ########################################
    def getID_default(self) -> int:
        return id(self)

    def copyState(self) -> None:
        """
        Forwarding an agent's (Person):
        previous state to current state
        """
        self.prevState = self.state


    ########################################
    # Getters & Setters
    ########################################

    def getID(self):
        return self.id

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getPrevState(self):
        return self.prevState

    def setPrevState(self, state):
        self.prevState = state
    
    def getGridLocation(self):
        return self.grid_location
    
    def setGridLocation(self, grid_location):
        self.grid_location = grid_location

    
    def getMedical(self):
        return self.medical
    
    def setMedical(self, medical):
        self.medical = medical
    
    def getHouse(self):
        return self.association["house"]
    
    def setHouse(self, house):
        self.association["house"] = house

    def getOffice(self):
        return self.association["office"]

    def setOffice(self, office):
        self.association["office"] = office