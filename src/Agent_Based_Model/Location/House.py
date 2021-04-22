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
    def __init__(self, id:int, grid_location:tuple, members:list=[]):
        super().__init__(grid_location)
        self.id = id
        self.capacity = HOUSE_SIZE
        self.guests = []
        self.members = members #[...<person>]

    def __repr__(self):
        return f"<House: id={self.id} loc={self.grid_location}>"

    ########################################
    # Methods
    ########################################
    def leaveHouse(self, person):
        def filterLeave(p):
            if p.getID() == person.getID():
                return False
            else:
                return True
        self.members = list(filter(filterLeave, self.members))


    ########################################
    # Getters & Setters
    ########################################

    def getMembers(self):
        return self.members

    def setMembers(self, members):
        self.members = members

    def getCapacity(self):
        return self.capacity
    
    def setCapacity(self, capacity):
        self.capacity = capacity