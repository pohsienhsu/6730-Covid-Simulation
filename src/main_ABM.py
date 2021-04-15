from Agent_Based_Model.Constant.constant import *
from Agent_Based_Model.ABM import *

world = ABM()
world.createWorld(num_people=1000)
# for i in range(20):
#     for j in range(20):
#         print(f"Location({i}, {j}), {world.getWorld()[i][j]}")
for person in world.getPeople():
    print(f"Person {person.getID()}: {person.getHouse()} | {person.getOffice()}")