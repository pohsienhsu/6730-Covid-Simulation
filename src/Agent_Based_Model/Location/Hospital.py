from ..Constant.constant import *
from .Cell import Cell

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
    def __init__(self, grid_location:tuple, patients:list=[], capacity:int=0):
        super().__init__(grid_location)
        self.capacity = capacity
        self.patients = patients

    def __repr__(self):
        return f"<Hospital: id={id(self)} loc={self.grid_location}>"

    ########################################
    # Methods
    ########################################



    ########################################
    # Getters & Setters
    ########################################

    def getMember(self):
        return self.patients

    def setMember(self, patients):
        self.patients = patients

    def getCapacity(self):
        return self.capacity
    
    def setCapacity(self, capacity):
        self.capacity = capacity