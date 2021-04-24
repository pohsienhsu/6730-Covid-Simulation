from Agent_Based_Model.Constant.constant import *
from Agent_Based_Model.ABM import *
from Visualization.Plotting_ABM import plotCurves_main

"""
To-Do List:
1. Logical Flow Chart Update (Matt, Po)
2. Literature Review (Andy)
    - discuss explicitly the methods and results used in your references
3. Update Methods(Paragraph) - ABM (Matt, Po)
4. Rusult Analysis
    * CA
    -> SIR/SEIR/SEIRD Comparsion

    * ABM/CA
    -> Mask/Vaccine/Hospital(Isolation) Influence on the spread of COVID-19
        * Confirmed Positive (Matt)
    -> Initial Patients vs Recovery Curve
        * 
    -> Modeling vs Real-World (Andy)
        * 

6. SEIRD Stats Curve (Optional)
7. Abstract (Andy)
"""

"""
ABM constant parameter adjustment

<Default>
INIT_INFECTED=0.005, INFECTION_RATE=0.1, EXPOSED_RATE=0.5, RECOVERY_RATE=0.75, \
    SUSCEPTIBLE_RATE=0.1, DEATH_RATE=0.02, WEAR_MASK=0.5, WEAR_MASK_POPULATION=0.5, \
        VACCINATED=0.1, VACCINATED_POPULATION=0.5, HOSPITALIZED=0.5, BEFORE_HOSPITAL=14
"""

day = 100
hour = (day+1)*24

world1 = ABM(INFECTION_RATE=0.1, EXPOSED_RATE=0.5, DEATH_RATE=0.02, RECOVERY_RATE=0.75, WEAR_MASK_POPULATION=0, VACCINATED_POPULATION=0, HOSPITALIZED=0)
world1.createWorld(num_people=1000)

world2 = ABM(INFECTION_RATE=0.1, EXPOSED_RATE=0.5, DEATH_RATE=0.02, RECOVERY_RATE=0.75, BEFORE_HOSPITAL=14, VACCINATED_POPULATION=0, WEAR_MASK_POPULATION=0)
world2.createWorld(num_people=1000)

world3 = ABM(INFECTION_RATE=0.1, EXPOSED_RATE=0.5, DEATH_RATE=0.02, RECOVERY_RATE=0.75, BEFORE_HOSPITAL=14, VACCINATED_POPULATION=0)
world3.createWorld(num_people=1000)

world4 = ABM(INFECTION_RATE=0.1, EXPOSED_RATE=0.5, DEATH_RATE=0.02, RECOVERY_RATE=0.75, BEFORE_HOSPITAL=14, WEAR_MASK_POPULATION=0.9, VACCINATED_POPULATION=0.1)
world4.createWorld(num_people=1000)

worldZ = ABM(zombieMode=True)
worldZ.createWorld(num_people=1000)

for h in range(hour):
    if h%24==0: print(f"Day {h//24}")
    world1.nextGeneration()
    world2.nextGeneration()
    world3.nextGeneration()
    world4.nextGeneration()
    worldZ.nextGeneration()
    
plotCurves_main([world1.modelOutput("No Mask & Vaccine & Hospital"), world2.modelOutput("Hospitalization"), world3.modelOutput("Hospitalization & Mask"), world4.modelOutput("Good Anti-Virus Protection"), worldZ.modelOutput("Zombie Mode")])

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