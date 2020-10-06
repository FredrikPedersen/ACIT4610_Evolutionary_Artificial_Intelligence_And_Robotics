from pylab import *

import pycx.pycxsimulator as pycx
from covid_modelling.health_state import HealthState
from covid_modelling.person import Person
from covid_modelling.infection import Infection

areaDimensions: int = 50
initProb: float = 0.01
infectionRate: float = 0.5
mortalityRate: float = 0.02


def initialize():
    global time, stateConfig, nextStateConfig, people

    time = 0

    stateConfig = zeros([areaDimensions, areaDimensions], int)
    people = [[None for i in range(areaDimensions)] for j in range(areaDimensions)]     # numpy does not support objects

    for posX in range(areaDimensions):
        for posY in range(areaDimensions):

            if random() < initProb:
                state: HealthState = HealthState.Infected
                people[posY][posX] = (Person(state, Infection()))
            else:
                state: HealthState = HealthState.Healthy
                people[posY][posX] = (Person(state))

            stateConfig[posY, posX] = state.value

    nextStateConfig = zeros([areaDimensions, areaDimensions])


def observe():
    cla()
    imshow(stateConfig, vmin=0, vmax=len(HealthState), cmap=cm.jet)
    axis('image')
    title('t = ' + str(time))


def update():
    global time, stateConfig, nextStateConfig, people

    time += 1

    for posX in range(areaDimensions):
        for posY in range(areaDimensions):

            person: Person = people[posY][posX]
            current_health_state: HealthState = person.get_state()

            # Dead people stay dead, recovered patients don't contract the disease over again
            if (current_health_state != HealthState.Dead) and (current_health_state != HealthState.Recovered):

                # If a person is healthy, check if any of it's neighbours are infected. If they are, infect this person
                # if we roll a random number lower than the infection rate.
                if current_health_state == HealthState.Healthy:
                    if __handle_healthy_person(HealthState.Infected, posY, posX):
                        person.become_infected()

                # If a person is infected, roll a random number and compare to mortality rate. If the person survives,
                # Make it recovered
                elif current_health_state == HealthState.Infected:
                    if random() < mortalityRate:
                        person.become_dead()
                    else:
                        person.become_recovered()

            nextStateConfig[posY, posX] = person.get_state().value

    stateConfig, nextStateConfig = nextStateConfig, stateConfig


def __handle_healthy_person(neighbourhood_state: HealthState, pos_y: int, pos_x: int):
    """
    Iterates through the neighbourhood of the current cell located at (pos_y, pos_x). If anyone
    in the neighbourhood has the desired state, roll a random number and compare it to the rate belonging
     to the InfectionState (I.e compare the random number to the Infection Rate if we are checking for infected
     neighbours) too see if the current cell should be updated.

    :param neighbourhood_state: The state we want to find out if anyone in the neighbourhood has
    :param pos_y: Y-coordinate of the current cell
    :param pos_x: X-coordinate of the current cell
    :return: True if the cell should be updated, false if not.
    """
    control_rate: float

    if neighbourhood_state == HealthState.Infected:
        control_rate = infectionRate

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if stateConfig[(pos_y + dy) % areaDimensions, (pos_x + dx) % areaDimensions] == neighbourhood_state.value:
                if random() < control_rate:
                    return True
    return False


pycx.GUI().start(func=[initialize, observe, update])