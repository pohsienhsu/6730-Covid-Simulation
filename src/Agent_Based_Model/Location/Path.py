from ..Constant.constant import *
from .Cell import Cell

class Path(Cell):
    """
    class Path:
        Serving as a path cell within the grid topology in the ABM.

    @attrs: 
    (super)
    grid_location: tuple (ex. (x,y))
    (self)
    capacity: int
    passengers: list (a list of Person class)
    """
    def __init__(self, grid_location:tuple, passengers:list=[], capacity:int=0):
        super().__init__(grid_location)
        self.capacity = capacity
        self.passengers = passengers #[...<person>]
        
    def __repr__(self):
        return f"<Path: id={id(self)} loc={self.grid_location}>"
    ########################################
    # Methods
    ########################################



    ########################################
    # Getters & Setters
    ########################################

    def getPassengers(self):
        return self.passengers

    def setPassengers(self, passengers):
        self.passengers = passengers

    def getCapacity(self):
        return self.capacity
    
    def setCapacity(self, capacity):
        self.capacity = capacity