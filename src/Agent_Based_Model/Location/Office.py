from ..Constant.constant import *
from .Cell import Cell
from ..CA_ABM import *

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
    def __init__(self, id:int ,grid_location:tuple):
        super().__init__(grid_location)
        self.id = id
        self.CA = []
        self.employees = []
        self.guests = []
        self.capacity = OFFICE_CAPACITY
    
    def __repr__(self):
        return f"<Office: id={self.id} loc={self.grid_location}>"

    ########################################
    # Methods
    ########################################
    def init_CA(self):
        """
        Initialize the Cellular Automata model within each cell of our ABM grid.
        Serving as an inner grid within each cells.
        """
        # (8, 5) -> Hard Code
        self.CA = Automata(8, 5, self.employees)

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

    def getCA(self):
        return self.CA

    def setCA(self, CA):
        self.CA = CA