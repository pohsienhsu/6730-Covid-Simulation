from Agent_Based_Model.Constant.constant import *
from Agent_Based_Model.ABM import *
from Visualization.Plotting import *
"""
ABM constant parameter adjustment

INIT_INFECTED=0.005, INFECTION_RATE=0.5, EXPOSED_RATE=0.16, RECOVERY_RATE=0.1, \
    SUSCEPTIBLE_RATE=0.1, DEATH_RATE=0.02, WEAR_MASK=0.5, WEAR_MASK_POPULATION=0.5, \
        VACCINATED=0.1, VACCINATED_POPULATION=0.5, HOSPITALIZED=0.5
"""

day = 7
hour = day*24

world1 = ABM()
world1.createWorld(num_people=1000)
world2 = ABM(DEATH_RATE=0.2)
world2.createWorld(num_people=1000)
world3 = ABM(WEAR_MASK_POPULATION=0, VACCINATED_POPULATION=0)
world3.createWorld(num_people=1000)

for h in range(hour):
    if h%24==0: print(f"Day {h//24}")
    world1.nextGeneration()
    world2.nextGeneration()
    world3.nextGeneration()

# print(f"""
# ###########Constant################
# INFECTION_RATE = {INFECTION_RATE}
# EXPOSED_RATE = {EXPOSED_RATE}
# RECOVERY_RATE = {RECOVERY_RATE}
# DEATH_RATE = {DEATH_RATE}
# HOUSE_SIZE = {HOUSE_SIZE} 
# OFFICE_CAPACITY = {OFFICE_CAPACITY}
# HOME_TIME = {HOME_TIME}
# COMMUTE_TIME = {COMMUTE_TIME}
# WORK_TIME = {WORK_TIME}
# WEAR_MASK = {WEAR_MASK}
# WEAR_MASK_POPULATION = {WEAR_MASK_POPULATION}
# VACCINATED = {VACCINATED}
# VACCINATED_POPULATION = {VACCINATED_POPULATION}
# HOSPITALIZED = {HOSPITALIZED}
# ##################################\n
# Total_Day = {day}
# S = {world1.getS_Arr()[-1]}
# E = {world1.getE_Arr()[-1]}
# I = {world1.getI_Arr()[-1]}
# R = {world1.getR_Arr()[-1]}
# D = {world1.getD_Arr()[-1]}
# Masked_Population = {world1.getMask_Arr()[-1]}
# Vaccinated_Population = {world1.getVaccinated_Arr()[-1]}
# Hospital_Infected_Population = {len(world1.getHospital()[0].getPatients())}
# """)
# world1.plotCurve()
plotCurves_main([world1.modelOutput("Default"), world2.modelOutput("High Death Rate"), world3.modelOutput("No Mask & Vaccine")])