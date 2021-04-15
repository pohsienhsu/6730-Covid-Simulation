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
    def __init__(self, grid_location:tuple, employees:list=[], capacity:int=0):
        super().__init__(grid_location)
        self.employees = employees
        self.capacity = capacity

    ########################################
    # Methods
    ########################################



    ########################################
    # Getters & Setters
    ########################################