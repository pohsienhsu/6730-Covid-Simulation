from ..Constant.constant import *
from .Cell import Cell

class Office(Cell):
    """
    class Office:
        Serving as an office cell within the grid topology in the ABM.

    @attrs: 
    (super)
    grid_location: tuple (ex. (x,y))
    (self)
    capacity: int
    employees: list (a list of Person class)
    """
    def __init__(self, id:int ,grid_location:tuple, employees:list=[], capacity:int=40):
        super().__init__(grid_location)
        self.id = id
        self.employees = employees
        self.guests = []
        self.capacity = capacity
    
    def __repr__(self):
        return f"<Office: id={self.id} loc={self.grid_location}>"

    ########################################
    # Methods
    ########################################



    ########################################
    # Getters & Setters
    ########################################

    def getEmployees(self):
        return self.employees

    def setEmployees(self, employees):
        self.employees = employees

    def getCapacity(self):
        return self.capacity
    
    def setCapacity(self, capacity):
        self.capacity = capacity