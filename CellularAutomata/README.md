# Install before running:
*pip install wheel*  
*pip install numpy scipy matplotlib ipython jupyter pandas sympy nose*  
*pip install networkx*


# The Simulation

The simulation is trying to make a somewhat realistic model of the spread of COVID-19 utilizing cellular automata for
determining how the virus is spread from cell to cell.

## Simulation Classes

In the simulation we have two classes and one Enum class of particular note.
The person and infection classes, and the health_state enum.

### Health_State

The health_state enum class represents a person's health by four states, Healthy, Infected, Recovered or Dead, and have 
linked an integer number to represent each state. I.e Healthy = 1, Infected = 2...

### Infection

The infection class represents a person's infection, and is used to keep track of what stage of infection a person is
in (i.e whether they are infectious), how long they have been sick and if the disease is potentially lethal to it's
host. 

### Person

The person class represents a person (duh), and is used to keep track of all relevant variables for how the pandemic
will affect a singular person. Currently we keep track of their current health state, age, if they are in a risk group,
if they are utilizing infection preventing measures like social distancing and wearing a mask, and their infection. 
Note that every person object has an infection object tid to them, even if they are not sick, as to avoid problems with 
None-values. Their infection will however not start progressing unless the person's health_state is set to INFECTED.


## Simulation Variables

Coming soon!

## Simulation Behaviour

Coming soon!

### Visual Color scheme:
Blue = Healthy

Red = Dead

Green = Infected

Dark Blue = Recovered

## Research, and how it is reflected in the simulation.

### Infectious Periods:

In the simulation, each time step simulates one day.
The average course of the coronavirus after contracting the virus is according to our research as follows:
5-6 Days Incubation Period
14 Days with Symptoms

A person is usually infectious a few days before symptom onset, and until they stop
showing symptoms. Thus we base this model on a person being infectious from day 3 of
the infection, until day 20. After day 20 they are considered as recovered.

### Recovered and Dead Patients

A recovered patient is in practice not immune to reinfection, but the cases are very rare, and
those that are confirmed didn't show any symptoms and their infectiousness is up for debate.
To make it simple, this simulation will consider a recovered patient as immune.  
Both dead and revovered patients are thus considered inactive agents, and are replaced by new healthy cells.

### Sources
[Reinfection](https://theconversation.com/coronavirus-reinfection-what-it-actually-means-and-why-you-shouldnt-panic-144965)  
  
  
  
  
 