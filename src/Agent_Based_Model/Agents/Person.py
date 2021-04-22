from ..Constant.constant import *

class Person:
    """
    class Person:
        Serving as an agent in the ABM. 
        Each Person would represent each individuals within our simulation.

    @attrs: 
    state: int (0: susceptible, 1: exposed, 2: infectious, 3: recovered, 4: dead, 5: dummy)
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
        if (not medical):
            self.medical = {
                "mask": False,
                "vaccinated": False,
                "hospitalized": False,
                "incubation": 7,
                "zombie": False
            }
        else:
            self.medical = medical

    def __repr__(self):
        vaccinated = self.medical["vaccinated"]
        return f"<Person: id={self.id} vaccinated={vaccinated} state={self.state}>"
        # return f"<Person: id={id(self)} state={self.state} loc={self.grid_location}>"

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

    def getMask(self):
        return self.medical["mask"]
    
    def setMask(self, mask):
        self.medical["mask"] = mask

    def getVaccinated(self):
        return self.medical["vaccinated"]

    def setVaccinated(self, vaccinated):
        self.medical["vaccinated"] = vaccinated

    def getHospitalized(self):
        return self.medical["hospitalized"]
    
    def setHospitalized(self, hospitalized):
        self.medical["hospitalized"] = hospitalized
    
    def getIncubation(self):
        return self.medical["incubation"]

    def setIncubation(self, day):
        self.medical["incubation"] = day

    def getZombie(self):
        return self.medical["zombie"]
    
    def setZombie(self, isZombie:bool):
        self.medical["zombie"] = isZombie

    def decreaseIncubation(self):
        self.medical["incubation"] -= 1

    def getHouse(self):
        return self.association["house"]
    
    def setHouse(self, house):
        self.association["house"] = house

    def getOffice(self):
        return self.association["office"]

    def setOffice(self, office):
        self.association["office"] = office