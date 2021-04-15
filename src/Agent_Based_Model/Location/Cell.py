from ..Constant.constant import *

class Cell:
    """
    class Cell:
        Serving as a cell within the grid topology in the ABM.

    @attrs: 
    grid_location: tuple (ex. (x,y))
    """
    def __init__(self, grid_location:tuple):
        self.grid_location = grid_location

    def __repr__(self):
        return f"<Cell: id={id(self)} loc={self.grid_location}>"

    ########################################
    # Methods
    ########################################
    def getID_default(self) -> int:
        return id(self)


    ########################################
    # Getters & Setters
    ########################################

    def getGridLocation(self):
        return self.grid_location
    
    def setGridLocation(self, grid_location):
        self.grid_location = grid_location