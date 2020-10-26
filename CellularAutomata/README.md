# Install before running:
*pip install wheel*  
*pip install numpy scipy matplotlib ipython jupyter pandas sympy nose*  
*pip install networkx*

# The Simulation

The simulation is trying to make a somewhat realistic model of the spread of COVID-19 utilizing cellular automata for
determining how efficiently the virus is spread from person to person.

## Simulation Classes

In the simulation we have two classes and one Enum class of particular note.
The person and infection classes, and the health_state enum.

### Health_State

The health_state enum class represents a person's health by four states, Healthy, Infected, Recovered or Dead, and have 
linked an integer number to represent each state. I.e Healthy = 1, Infected = 2...

### Infection

The infection class represents a person's infection, and is used to keep track of what stage of infection a person is
in (i.e whether they are infectious or not), how long they have been sick, and if the disease is potentially lethal to 
it's host.  

### Person

The person class represents a person (duh), and is used to keep track of all relevant variables for how the pandemic
will affect a singular person. Currently we keep track of their current health state, age, if they are in a risk group,
if they are utilizing infection preventing measures like social distancing and wearing a mask, and their infection. 
Note that every person object has an infection object tied to them, even if they are not sick, as to avoid None-value
related problems. Their infection will however not start progressing unless the person's health_state is set to INFECTED.

## Simulation Constants

 - **AREA_DIMENSIONS:** The simulation has nxn number of cells/people. AREA_DIMENSIONS = n.  
 - **INIT_INFECTION_PROBABILITY:** This is an arbitrary number used to set the percentage of initially infected people.  
 - **INFECTION_CHANCE:** Chance of a healthy person being infected by an infected one. In the case where a healthy cell 
 has an infected neighbour, this chance is multiplied with the reduction values of the persons registered infection 
 prevention measures (e.g wearing a mask). Then a random number is generated, if that is lower than the resulting 
 infection chance, the healthy cell becomes infected.
 - **MORTALITY_CHANCE:** The chance of a person dying from the virus. In this simulation we only consider people in the
 risk groups of being in mortal danger. If an infected person is in a risk group, the mortality chance is being compared
 to a random number to see if the infection will kill the person.  
 - **MASK_REDUCTION:** How much less of a percentage chance there is to become infected if wearing a face covering mask.
 - **DISTANCING_REDUCTION:** How much less of a percentage chance there is to become infected if practicing social distancing.
 - **MORTAL_RISK_AGE:** Minimum age of a person to be considered in a risk group.
 - **MORTAL_RISK_GROUP_PERCENTAGE:** How much of the (norwegian) population considered to be in a risk group due to health
 conditions. When a person object is initialized, this percentage is compared to a random number to see if the person 
 will be in a risk group.

## Simulation Behaviour

This simulation is based of the PyCX-library's [ca-hostpathogen](https://github.com/hsayama/PyCX/blob/master/ca-hostpathogen.py)
script. Our simulation is by all means a lot more complex than the PyCX sample, but in it's core it still based of the 
same concepts, having an array with configurations being initialized, updated by checking the neighbours of each cell in
the configuration, and finally a Pyplot graph observes the changes in the configuration.  

There have been no changes to the behaviour of the [PyCX simulator](https://github.com/hsayama/PyCX/blob/master/pycxsimulator.py)
which is being used to run the initialize, update and observe functions.

In our version of the simulation, there are still the **three core functions**:
```Python
 initialize() -> None
 update() -> None
 observe() -> None
```

There are also two functions for handling infected and non-infected cells, and one function for extracting the 
health_state integer values for each person, placing them in a separate array which is passed to Pyplot:
```Python
 __handle_healthy_person(person: Person, pos_y: int, pos_x: int) -> None
 __handle_infected_person(person: Person) -> None
 __create_health_value_array() -> ndarray
```

### initialize()
Here the simulation configuration and all other variables are initialized.
The core of the function is creating the **stateConfig** 2D-array containing all the person objects. In the initial 
config there is a percentage of people starting as infected, determined by generating a random number and comparing it 
to the INIT_INFECTION_PROBABILITY constant (random < init_probability results in infected person).

### update()
Increments the timeStep before updating each person object in stateConfig:
 - Dead or Recovered persons are being replaced with new, Healthy people to keep the simulation going.
 - Healthy people are passed to healthy person handler to determine whether they should get infected.
 - Infected people are passed to infected person handler to determine whether they die, recover or remain sick.
 
### observe()
Calls function to create an integer array containing all the health states of the person objects in the stateConfig,
then passes this array to Pyplot.imshow to generate the visual graph. This is also where the info texts (like current
timestep, total infected etc) are set.

With the current values assigned to each state (see health_state.py), pyplot generates the following color scheme:
 - Blue = Healthy
 - Red = Dead
 - Green = Infected
 - Dark Blue = Recovered
 
### __handle_healthy_person(person, pos_y, pos_x)
This function is used to determine whether a healthy person at position (y, x) is to going to become infected.
To determine this, we check the healthy persons neighbourhood (all cells directly adjacent to (y, x)) for infection.
For each infected cell found we calculate the infection chance and compare that to a randomly generated number to determine
whether they get infected (see Simulation Constants - INFECTION_CHANCE).

### __handle_infected_person(person)
When handling an infected person, there are three possible outcomes: they die, they recover or they stay infected.

1. Death:
    - If a person's infection was marked as lethal when initializing the person (see Simulation Constants - MORTALITY_CHANCE)
    the person dies. 
    - Plans are to implement a check to see if the virus symptoms has lasted for at least a week before the 
    person dies, as that would be a more realistic scenario.  

2. Recovery:
    - If a person does not die, we test if they have been sick longer or equal to the average duration of the disease.
    - If so, we take RECOVERY_CHANCE plus the time a person has been having symptoms divided by 200 (200 in this
    case is an arbitrary made up so recovery chances won't be too high) and compare it to a random number. This way, the
    longer a person is sick over the average duration, the higher their chances of recovering.

3. Remain Infected:
    - If a person remains infected, their infection object is updated.
    - This entails that the infection's duration is incremented, and if appropriate, it's infection_stage (Incubation or
    Showing Sympoms) and whether it is infectious or not is updated.

### __create_health_value_array()
The PyCX simulator utilizes Pyplot's imshow function to render the grid, and that only accepts an array with integer
values. This function creates a 2D Numpy array with the health_state values from each person in the stateConfig in
order to render a cells health state graphically.

In terms of effectiveness, looping through the entire stateConfig and retrieving the health_state value for every
person object is abysmal. We will look into how to pass stateConfig directly to some Pyplot function if we get the time 
for it.

# Evolutionary Algorithm

To make sure the simulation is as realistic as possible we have implemented an evolutionary algorithm where the
termination goals are based on the real behaviour of the COVID-19 outbreak in Norway. The algorithm tries to 
figure out the most optimal values for INFECTION_CHANCE and MORTALITY_CHANCE by comparing the results (number of 
infected and dead) of the simulation. These two values are prime targets for evolving the simulation to become more 
accurate as they directly impact the infection and death rates. They are also the only variables NOT based on any real 
research. 

We pulled data on the outbreak from the Norwegian Institute of Public Health on October 18th 2020, and consider March 
2nd 2020 to be the start of the Norwegian outbreak. On step 230 of the simulation (the difference between March 2nd and 
October 18th), the run is terminated. We then assess the fitness of the simulation run and adjust infection and 
mortality constants accordingly. This process repeats after each run until we have an acceptable fitness score. 

### Fitness

The fitness of the simulation is calculated by taking the difference between the simulation's number of infected
and deaths, and their reported real world numbers. A fitness score closer to zero is considered better, as this means 
the simulation is more accurate on a linear scale.

### Evolution

When evolving the simulation, we only take the previous simulation run into consideration. 

First the fitness of the total number of infected is calculated. A value of 0 +/- 200 is considered acceptable.
If the fitness is not acceptable, the INFECTION_CHANCE is changed increased or decreased by 1/10 of it's current value 
based on if it breaks the upper or lower bound.

When an acceptable fitness is achieved for infection values, we move on the death values, as death values are directly 
impacted by the infection values (more infected cells = more chances of cells dying). Changing these before the optimal
infection values are determined would just result in redundant adjustments to MORTALITY_CHANCE. For the mortality rate
fitness, 0 +/- 10 are considered acceptable values.

Due to the somewhat random nature of the simulation (i.e. it is a random value being compared to INFECTION_CHANCE to 
determine whether a healthy cell is infected by a diseased cell), there might be simulation runs where the boundaries of
the acceptable values are breached, even after a value which yields an acceptable fitness is reached. To prevent a
single run with lots of irregularly high random numbers, we added a value to track how many stable runs (runs with 
acceptable fitness values) there has been in a row. If there have been 5 or more stable runs, INFECTION_CHANCE and
MORTALITY_CHANCE won't be changed any further. 

# Research, and how it is reflected in the simulation

### Infectious Periods

In the simulation, each time step simulates one day.
The average course of the coronavirus after contracting the virus is according to our research as follows:
5 Days Incubation Period
14 Days with Symptoms

A person is usually infectious a few days before symptom onset, and until they stop
showing symptoms. Thus we base this model on a person being infectious from day 3 of
the infection, until day 20. After day 20 they are considered as recovered.

### Recovered and Dead Patients

A recovered patient is in practice not immune to reinfection, but the cases are very rare.
Those who are confirmed reinfected didn't show any symptoms, and their infectiousness is up for debate.
To make it simple, this simulation will consider a recovered patient as immune.  
Both dead and recovered patients are thus considered inactive cells, and are replaced by new healthy cells.

### Sources
[Reinfection](https://theconversation.com/coronavirus-reinfection-what-it-actually-means-and-why-you-shouldnt-panic-144965)  
[Mask Reduction Chance](https://www.ucdavis.edu/coronavirus/news/your-mask-cuts-own-risk-65-percent/)  
[Risk Groups](https://forskning.no/sykdommer-virus/hvem-er-egentlig-i-risikogruppen-for-korona/1659901) 
[Virus Progression](https://www.cdc.gov/coronavirus/2019-ncov/hcp/clinical-guidance-management-patients.html)   
[Corona Stats Norway](https://www.fhi.no/en/id/infectious-diseases/coronavirus/daily-reports/daily-reports-COVID19/)  
  
 