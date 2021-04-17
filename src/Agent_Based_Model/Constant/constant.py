# Constant
###############################
INIT_INFECTED = 0.01
# S -> E
INFECTION_RATE = 0.9
# Incubation days
INCUBATION_DAYS = 7
# E -> I
EXPOSED_RATE = 0.9
# I -> R
RECOVERY_RATE = 0.1
# R -> S
SUSCEPTIBLE_RATE = 0.1
# I -> D
DEATH_RATE = 0.05

HOUSE_SIZE = 4

OFFICE_CAPACITY = 40

HOME_TIME = [0, 1, 2, 3, 4, 5, 6, 19, 20, 21, 22, 23]

COMMUTE_TIME = [7, 8, 17, 18]

WORK_TIME = [9, 10, 11, 12, 13, 14, 15, 16]

WEAR_MASK = 0.5

VACCINATED = 0.9
###############################

cmaps = {
    "SIR": {0: [0.0, 0.0, 1.0, 1],
            1: [1.0, 0.0, 0.0, 1],
            2: [0.0, 1.0, 0.0, 1]},
    "SEIR": {0: [0.0, 0.0, 1.0, 1],
             1: [1.0, 0.7, 0.0, 1],
             2: [1.0, 0.0, 0.0, 1],
             3: [0.0, 1.0, 0.0, 1]},
    "SEIRS": {0: [0.0, 0.0, 1.0, 1],
              1: [1.0, 0.7, 0.0, 1], 
              2: [1.0, 0.0, 0.0, 1], 
              3: [0.0, 1.0, 0.0, 1]},
    "SEIRD": {0: [0.0, 0.0, 1.0, 1],
              1: [1.0, 0.7, 0.0, 1],
              2: [1.0, 0.0, 0.0, 1],
              3: [0.0, 1.0, 0.0, 1],
              4: [0.5, 0.0, 0.5, 1]},
    "SEIRSD": {0: [0.0, 0.0, 1.0, 1],
               1: [1.0, 0.7, 0.0, 1], 
               2: [1.0, 0.0, 0.0, 1], 
               3: [0.0, 1.0, 0.0, 1],
               4: [0.5, 0.0, 0.5, 1]}
}

labels = {
    "SIR": {0: 'Susceptible', 1: 'Infected', 2: 'Recovered'},
    "SEIR": {0: 'Susceptible', 1: "Exposed", 2: 'Infected', 3: 'Recovered'},
    "SEIRS": {0: 'Susceptible', 1: "Exposed", 2: 'Infected', 3: 'Recovered'},
    "SEIRD": {0: 'Susceptible', 1: "Exposed", 2: 'Infected', 3: 'Recovered', 4: "Dead"},
    "SEIRSD": {0: 'Susceptible', 1: "Exposed", 2: 'Infected', 3: 'Recovered', 4: "Dead"}
}
