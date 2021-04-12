# COVID-19 Simulation
### Checkpoint Requirements
Submission: A single PDF document. 

There are three components for the submission for the checkpoint: 

* A clear and detailed description of your project (~ 2 - 4 pages, excluding references). 

* At this stage, you should have a clearer idea of the project and the details that you expect would be part of the final submission. 

* Some things to include: 

  a) An abstract summarizing the system and the goals of the project 

  b) Description of the system being studied 

  c) A conceptual model of the system 

  d) Platform(s) of development 

  e) Literature review (if possible) 

  

2. An update of the current state of the project and initial results, if any (max 2 pages) 

Some things to include: 

A “show of progress” via some working code, analysis, or initial modeling attempts 

If there have been any major changes in direction or “course-corrections” since your original proposal, you can describe them here. 

Division of labor: How will you divide up the remaining work among your team? In particular, we will be looking to see that you’ve given thought to how to ensure your project justifies a multi-person (2 or 3, depending on team size) effort. 

### To-Do List
1. Find reference coefficient from papers
    - INIT_INFECTED (Initial Patients)
    - INFECTION_RATE (S->E or S->I)
    - INCUBATION_DAYS (Days before E -> I)
    - EXPOSED_RATE (E -> I)
    - RECOVERY_RATE (I -> R)
    - SUSCEPTIBLE_RATE (R -> S)
    - DEATH_RATE (I -> D)

2. Case Study
    - Initial patients to overall death rate
    - Incubation days to Infection spread speed
    - Number of dead population per specific day:
      - https://www.frontiersin.org/articles/10.3389/fpubh.2020.00230/full
    - Comparing our model to current Georgia's epidemic situation
  
3. Study Agent-Based Model (Future Work)
In other words, how could we implement the behavior of wearing masks/being isolated/getting vaccinated to our existing models
    - mask
    - quarantine
    - short term travel
      - https://pubmed.ncbi.nlm.nih.gov/33481956/
    - vaccine
    - social distance 
      - https://www.nature.com/articles/s41598-021-83540-2

## Draft
### Motivation
COVID-19 has been drastically changing the world during the past year. Throughout all the counties suffering from the pandemics, some countries were dealing with it well by enforcing people wearing masks and social distancing, starting from the early stage of the pandemic. Therefore, we would like to model the pandemic to understand the behavior of the virus on human beings through compartmental models such as SIR/SEIR/SEIRD with the topolocial interaction via Cellular Automata (CA) [9] and then to study the influence of masks/vaccine/social distancing on controlling the outbreak with Agent-Based Model (ABM) [1] [3].

### Introduction
To simulate models in epidemiology, compartmental models were commonly implemented to represent how individuals in different state in a population interaction [5]. 
1. SIR \
   The SIR model divides the total population size at time t denoted as P(t) into Susceptible S(t), Infectious I(t) and Recovered R(t). Hence, for the total population we can get P(t) = S(t) + I(t) + R(t).

2. SEIR \
   The SEIR model considers an additional factor, Exposed E(t), based on the basic SIR model. That is, a person in the susceptible condition will first be exposed before infectious. Compared with SIR, SEIR accords more with reality. Hence, for the total population we can get P(t) = S(t) + E(t) + I(t) + R(t).
   
3. SEIRD \
   In order to stimulate the real Covid-19 situation, we need to include the death population into our model. Therefore, we implement the SEIRD model which takes Death D(t) into consideration and we can get P(t) = S(t) + E(t) + I(t) + R(t) + D(t).

In order to model the interaction throughout people during the pandemics, a regular grid of identical was implemented as the topology during the modeling interaction. In the first stage of the program, Cellular Automata is implemented with the comparmental models above as the simple modeling where each cell represents as people. The neigboring cells provides an interaction for spreading the virus in the system. In the second stage of the model, we build Agent-based Model on top of the grid topology to execite more sophisticated simlutation to study the influence of personal protected equipments and social distancing on the pandemics. 

1. Cellular Automata (CA) \
   A cellular automata is a discrete model of computation studied in automata theory. It consists of a regular grid of cells, and it can be in any dimension. To do the simulation, an initial state will be given to each cell (time t=0). Then, while new generation being created, each cell will be assigned a new state based on a fixed rule from the designer. Eventually, the grid of the cellular automata will show the final result of each cell's status after several iterations.

2. Agent-Based Model (ABM) \
   ABM simulates the actions of the interactions of autonomous agents, environments, and time evolution.  
   - Agents represent an individual or collective entities such as a person or organization. Each agent has its own independent characteristics, deciding agent's behabior, goals, locations in the simulation.
   - Environments are the space where agents exist and interacts with other agents. In ABM, the topological information differs from case by case. In this project, we inplement a grid similar to Cellular Automata as the topology of the interaction, but Network Interaction could also be implemented as environments in ABM.
   - Time contributes the "dynamic" to the simulation. During ABM simulation, it will go through a number of time steps where agents and environments update the states/characteristics. 

### Methods
* Stage One - Cellular Automata
  - Compartmental Models: SIR/SEIR/SEIRD
  - CA Rule:
    - Initially, we randomly assigned the Susceptible status to some grids. 
    - For SIR:
      - Susceptible status will become Infectious based on the infectious rate
      - Infectious status will become Recovered based on the recovered rate
    - For SEIR:
      - Susceptible status will become Exposed based on the infectious rate
      - Exposed status will become Infectious based on the latent diseased rate
      - Infectious status will become Recovered based on the recovered rate
    - For SEIRD:
      - Susceptible status will become Exposed based on the infectious rate
      - Exposed status will become Infectious based on the latent diseased rate
      - Infectious status will become Recovered based on the recovered rate or Died based on the death rate

* Stage Two - Agent-Based Model (Anticipated)
  - Compartmental Models: SEIRD
  - ABM Components: 
      1. Agents
        - Person:
          - Attribute: id (unique), state (0: Susceptibe, 1: Exposed, 2: Infected, 3: Recovered, 4: Dead), grid_location (tuple(x, y)), wear_mask (boolean), vaccinated (boolean), hospitalized (boolean)
        - Family: 
          - Attribute: People (list(id)), grid location (tuple(x, y))
        - Company:
          - Attribute: People (list(id)), grid location (tuple(x, y))

      2. Environments
        - Grid Topology (2D-Square)
          a. House: Where people stay with their family. It is time-dependable
          b. Hospital: Where infectious population with symptoms would be brought to isolation and treatment
          c. Office: Where people would go to work according to their company
          d. Commuting Path: Any potential cells besides a person's house, office, or a hosptial within the grid

      3. Time (Hour-Based) 
        - 19:00 - 07:00 -> Home (At House)
        - 07:00 - 09:00 -> Commute (Random Walk: 1 step/hr) 
        - 09:00 - 17:00 -> Work (At Office)
        - 17:00 - 19:00 -> Commute (Random Walk: 1 step/hr)

  - ABM Rule:
    
    

### Current Results
* Cellular Automata


### Progress/Colaboration
[COVID Simulation Project Github](https://github.gatech.edu/phsu40/6730-Covid-Simulation)

 We managed to store our code through Github and work daily on the project through VSCode's Live-Share extension. In terms of the progress we had accomplished until this checkpoints was to explore various simulation models, such as SIR, SEIR, SEIRS, SEIRS etc.. These models were based on several references, including codes [6] and conceptual ideas [3][4] that helped us constructed these models and classes in Python. Our models were able to plot the Simulation curves, such as SEIR curve through the constants and parameters we input. The displaying curves and plots does match our expectation of a SIR-based models [5] would exhibit. In addition, we factored in attributes such as Death and incubation days [5] to further examine the correctness and possible outcomes to our models. That is to say, we are trying to have a comprehensive understanding what model model we would want to build our agent-based model on for our final project goal. 
 
 During the progress we made for this checkpoint, we also decided details about our agent-based model. We've found a reference model [1] that we could build our ABS (Agent-Based Simulation) on with sereral essential modification. These modifications includes the design pattern of how individuals would interact on a high level and the impact of the personal pretective equipments would have to the pandemic. 

### Division of Labor

### FutureWork:
| Week/Dates    |   Objectives  |
|:-------------:|:------------- |
| Week 1        | right-aligned |
| Week 2        | centered      |
| Week 3        | are neat      |



### Reference: 
 * [1] COVID-ABS: An agent-based model of COVID-19 epidemic to simulate health and economic effects of social distancing interventions: https://reader.elsevier.com/reader/sd/pii/S0960077920304859?token=315C3393A6229C5AB8B7E8566F6E4E5B127349BA76D369BBD3D20C20B63D7040A503CE8FE00D08BE6C459A2C817C57DC&originRegion=us-east-1&originCreation=20210411164718
Source Code: https://github.com/petroniocandido/COVID19_AgentBasedSimulation
 * [2] Modeling and forecasting of COVID-19 using a hybrid dynamic model based on SEIRD with ARIMA corrections: https://www.sciencedirect.com/science/article/pii/S2468042720301032
 * [3]Measuring and Preventing COVID-19 Using the SIR Model and Machine Learning in Smart Health Care: https://www.hindawi.com/journals/jhe/2020/8857346/ 
 * [4] A Simulation of a COVID-19 Epidemic Based on a Deterministic SEIR Model: https://www.frontiersin.org/articles/10.3389/fpubh.2020.00230/full 
 * [5] SEIR and SEIRS models: https://docs.idmod.org/projects/emod-hiv/en/latest/model-seir.html 
 * [6] Simulate Covid-19 in your area with Python — beyond SIR models (Individual-Based-Simulation): https://towardsdatascience.com/model-the-covid-19-epidemic-in-detail-with-python-98f0d13f3a0e 
 * [7] Modeling COVID-19 scenarios for United States (mask no mask, death rate, SEIR): https://www.nature.com/articles/s41591-020-1132-9#Sec7 
 * [8] Python Coronavirus Simulation: https://github.com/paulvangentcom/python_corona_simulation 
 * [9] A model based on cellular automata to estimate the social isolation impact on COVID-19 spreading in Brazil: https://www.sciencedirect.com/science/article/pii/S0169260720316655

### Databases
Novel Corona Virus 2019 Datasets: https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset 
