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
    - 
 
3. Study Agent-Based Model (Future Work)
In other words, how could we implement the behavior of wearing masks/being isolated/getting vaccinated to our existing models
    - mask
    - quarantine
    - short term travel
      - https://pubmed.ncbi.nlm.nih.gov/33481956/
    - vaccine
    - social distance 
      - https://www.nature.com/articles/s41598-021-83540-2

### Draft
1. Goal
2. Models Elaboration (SIR/CA/Agent-Based-Model) 
3. Our rules for Cellular Automata
4. Current Analysis/Simulation
5. Progress/Colaboration
6. FutureWork

### Reference: 
* COVID-ABS: An agent-based model of COVID-19 epidemic to simulate health and economic effects of social distancing interventions https://reader.elsevier.com/reader/sd/pii/S0960077920304859?token=315C3393A6229C5AB8B7E8566F6E4E5B127349BA76D369BBD3D20C20B63D7040A503CE8FE00D08BE6C459A2C817C57DC&originRegion=us-east-1&originCreation=20210411164718
Source Code: https://github.com/petroniocandido/COVID19_AgentBasedSimulation
* Modeling and forecasting of COVID-19 using a hybrid dynamic model based on SEIRD with ARIMA corrections:
https://www.sciencedirect.com/science/article/pii/S2468042720301032
