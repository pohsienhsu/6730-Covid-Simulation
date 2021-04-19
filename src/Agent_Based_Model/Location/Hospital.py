from ..Constant.constant import *
from .Cell import Cell
import sys

class Hospital(Cell):
    """
    class Hospital:
        Serving as a hospitalcell within the grid topology in the ABM.

    @attrs: 
    (super)
    grid_location: tuple (ex. (x,y))
    (self)
    capacity: int
    patients: list (a list of Person class)
    """
    def __init__(self, grid_location:tuple, patients:list=[]):
        super().__init__(grid_location)
        self.capacity = sys.maxsize
        self.patients = patients

    def __repr__(self):
        return f"<Hospital: id={id(self)} loc={self.grid_location}>"

    ########################################
    # Methods
    ########################################



    ########################################
    # Getters & Setters
    ########################################
    def getPatients(self):
        return self.patients

    def setPatients(self, patients):
        self.patients = patients
    
    def checkIn(self, patient):
        self.patients.append(patient)
    
    def checkOut(self, patient):
        def filterCheckOut(p):
            if p.getID() == patient.getID():
                return False
            else:
                return True
        self.patients = list(filter(filterCheckOut, self.patients))

    def getCapacity(self):
        return self.capacity
    
    def setCapacity(self, capacity):
        self.capacity = capacity