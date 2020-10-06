from pylab import *

import pycx.pycxsimulator as pycx
from covid_modelling.infection_state import InfectionState
from covid_modelling.person import Person

areaDimensions: int = 100
initProb: float = 0.01
infectionRate: float = 0.5
recoveryRate: float = 0.15
mortalityRate: float = 0.02


def initialize():
    global time, stateConfig, nextStateConfig, people

    time = 0

    stateConfig = zeros([areaDimensions, areaDimensions], int)
    people = [[None for i in range(areaDimensions)] for j in range(areaDimensions)]

    for posX in range(areaDimensions):
        for posY in range(areaDimensions):
            if random() < initProb:
                state: InfectionState = InfectionState.Infected
            else:
                state: InfectionState = InfectionState.Healthy

            stateConfig[posY, posX] = state.value
            people[posY][posX] = (Person(state))

    nextStateConfig = zeros([areaDimensions, areaDimensions])


def observe():
    cla()
    imshow(stateConfig, vmin=0, vmax=len(InfectionState), cmap=cm.jet)
    axis('image')
    title('t = ' + str(time))


def update():
    global time, stateConfig, nextStateConfig, people

    time += 1   # Update step

    for posX in range(areaDimensions):
        for posY in range(areaDimensions):

            person: Person = people[posY][posX]

            # If a person is dead, check if it's neighbours are healthy. If they are, regrow this person if we roll
            # a random number lower than the recovery rate.
            if person.get_state() == InfectionState.Recovering:
                if __iterate_neighbourhood(InfectionState.Healthy, posY, posX):
                    person.set_state(InfectionState.Healthy)

            # If a person is healthy, check if any of it's neighbours are infectded. If they are, infect this person if
            # we roll a random number lower than the infection rate.
            elif person.get_state() == InfectionState.Healthy:
                if __iterate_neighbourhood(InfectionState.Infected, posY, posX):
                    person.set_state(InfectionState.Infected)

            # If a person is neither dead nor healthy, make it Recovering.
            else:
                person.set_state(InfectionState.Recovering)

            nextStateConfig[posY, posX] = person.get_state().value

    stateConfig, nextStateConfig = nextStateConfig, stateConfig


def __iterate_neighbourhood(neighbourhood_state: InfectionState, pos_y: int, pos_x: int):
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

    if neighbourhood_state == InfectionState.Infected:
        control_rate = infectionRate
    elif neighbourhood_state == InfectionState.Healthy:
        control_rate = recoveryRate

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if stateConfig[(pos_y + dy) % areaDimensions, (pos_x + dx) % areaDimensions] == neighbourhood_state.value:
                if random() < control_rate:
                    return True
    return False


pycx.GUI().start(func=[initialize, observe, update])