# Install before running:
*pip install wheel*  
*pip install numpy scipy matplotlib ipython jupyter pandas sympy nose*  
*pip install networkx*


# The Simulation

The simulation is trying to make a somewhat realistic model of the spread of COVID-19 utilizing cellular automata for
determining how the virus is spread from cell to cell. 

## Classes

In the simulation we have to classes and one Enum class of particular note.
The person and infection class, and the health_state enum.

### Health_State

The health_state enum class represents a person's health by four states, Healthy, Infected, Recovered or Dead, and have 
linked an integer number to represent each state. I.e Healthy = 1, Infected = 2...

### Color scheme:
Blue = Healthy

Red = Dead

Green = Infected

Dark Blue = Recovered

### Infectious Periods:

In the simulation, each time step simulates one day.
The average course of the coronavirus after contracting the virus is as follows:
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
  
  
  
  
 