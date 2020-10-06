###Install before running:
pip install wheel
pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
pip install networkx

###Color scheme:
Blue = Healthy

Red = Dead

Green = Infected

Dark Blue = Recovered

###Infectious Periods:

In the simulation, each time step simulates one day.
The average course of the coronavirus after contracting the virus is as follows:
5-6 Days Incubation Period
14 Days with Symptoms

A person is usually infectious a few days before symptom onset, and until they stop
showing symptoms. Thus we base this model on a person being infectious from day 3 of
the infection, until day 20. After day 20 they are considered as recovered.

###Recovered Patients

A recovered patient is in practice not immune to reinfection, but the cases are very rare, and
those that are confirmed didn't show any symptoms and their infectiousness is up for debate.
To make it simple, this simulation will consider a recovered patient as immune.

[Source](https://theconversation.com/coronavirus-reinfection-what-it-actually-means-and-why-you-shouldnt-panic-144965)