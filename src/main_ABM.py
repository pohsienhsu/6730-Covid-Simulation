from Agent_Based_Model.Constant.constant import *
from Agent_Based_Model.ABM import *

world = ABM()
world.createWorld(num_people=1000)
day = 20
hour = 20*24

for h in range(hour):
    world.nextGeneration()

# print(len(world.getPeopleState()))
print("S: ", world.getS_Arr())
print("E: ", world.getE_Arr())
print("I: ", world.getI_Arr())
print("R: ", world.getR_Arr())
print("D: ", world.getDays_Arr())
print("Days: ", world.getDays_Arr())
world.plotCurve()