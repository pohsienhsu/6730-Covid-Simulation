from Agent_Based_Model.Constant.constant import *
from Agent_Based_Model.ABM import *
import sys
import time
    
world = ABM()
world.createWorld(num_people=1000)
day = 100
hour = day*24

for h in range(hour):
    world.nextGeneration()
    # sys.stdout.write("\r{0}>".format("="*(h%24)))
    # sys.stdout.flush()
    # time.sleep(0.5)

print(f"""
###########Constant################\n
INFECTION_RATE = {INFECTION_RATE}\n
EXPOSED_RATE = {EXPOSED_RATE}\n
RECOVERY_RATE = {RECOVERY_RATE}\n
DEATH_RATE = {DEATH_RATE}\n
HOUSE_SIZE = {HOUSE_SIZE}\n 
OFFICE_CAPACITY = {OFFICE_CAPACITY}\n
HOME_TIME = {HOME_TIME}\n
COMMUTE_TIME = {COMMUTE_TIME}\n
WORK_TIME = {WORK_TIME}\n
WEAR_MASK = {WEAR_MASK}\n
WEAR_MASK_POPULATION = {WEAR_MASK_POPULATION}\n
VACCINATED = {VACCINATED}\n
VACCINATED_POPULATION = {VACCINATED_POPULATION}\n
HOSPITALIZED = {HOSPITALIZED}\n
##################################\n\n
Total_Day = {day}\n
S = {world.getS_Arr()[-1]}\n
E = {world.getE_Arr()[-1]}\n
I = {world.getI_Arr()[-1]}\n
R = {world.getR_Arr()[-1]}\n
D = {world.getD_Arr()[-1]}\n
Masked_Population = {world.getMask_Arr()[-1]}\n
Vaccinated_Population = {world.getVaccinated_Arr()[-1]}\n
Hospital_Infected_Population = {len(world.getHospital()[0].getPatients())}
""")
world.plotCurve()