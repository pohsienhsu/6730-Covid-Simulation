from ..Constant.constant import *
from .Cell import Cell

class House(Cell):
    """
    class House:
        Serving as a house cell within the grid topology in the ABM.

    @attrs: 
    (super)
    grid_location: tuple (ex. (x,y))
    (self)
    capacity: int
    members: list (a list of Person class)
    """
    def __init__(self, grid_location:tuple, members:list=[], capacity:int=0):
        super().__init__(grid_location)
        self.capacity = capacity
        self.members = members #[...<person>]

    ########################################
    # Methods
    ########################################



    ########################################
    # Getters & Setters
    ########################################

    def getMember(self):
        return self.members

    def setMember(self, passengers):
        self.members = members

    def getCapacity(self):
        return self.capacity
    
    def setCapacity(self, capacity):
        self.capacity = capacity