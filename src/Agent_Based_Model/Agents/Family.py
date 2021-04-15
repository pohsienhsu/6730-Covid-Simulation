class Family:
    """
    class Family:
        Serving as a collection agents in the ABM. 
        Each Family would have multiple Person's within our simulation.

    @attrs: 
    members: list (a list of Person class)
    grid_location: tuple (ex. (x,y))
    size: int (default: 4)
    """
    def __init__(self, members:list, grid_location:tuple, size:int = 4):
        self.members = members
        self.grid_location = grid_location
        self.size = size

    ########################################
    # Methods
    ########################################
    
        
    ########################################
    # Getters & Setters
    ########################################
    def getMember(self):
        return self.members

    def setMember(self, members):
        self.members = members 
    
    def getGridLocation(self):
        return self.grid_location

    def setGridLocation(self, grid_location):
        self.grid_location = grid_location

    def getSize(self):
        return self.size
    
    def setSize(self, size):
        self.size = size