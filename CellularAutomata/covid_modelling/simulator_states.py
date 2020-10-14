from typing import List

from pylab import *

import covid_modelling.constants as Constants
import pycx.pycxsimulator as pycx
from covid_modelling.health_state import HealthState
from covid_modelling.person import Person

timeStep: int
dead: int
recovered: int
total: int
infected: int
stateConfig: List[List[Person]]


def initialize():
    global timeStep, stateConfig, infected, dead, recovered, total

    timeStep = 0
    infected = 0
    dead = 0
    recovered = 0
    total = 0

    # numpy arrays does not support objects, using a standard 2D-array instead
    stateConfig = [[Person for i in range(Constants.AREA_DIMENSIONS)] for j in range(Constants.AREA_DIMENSIONS)]

    for posX in range(Constants.AREA_DIMENSIONS):
        for posY in range(Constants.AREA_DIMENSIONS):

            if random() < Constants.INIT_INFECTION_PROBABILITY:
                stateConfig[posY][posX] = Person(HealthState.Infected)
                infected += 1
            else:
                stateConfig[posY][posX] = Person(HealthState.Healthy)

            total += 1


def observe():
    health_values: ndarray = __create_health_value_array()

    cla()
    imshow(health_values, vmin=0, vmax=len(HealthState), cmap=cm.jet)
    axis("image")

    mortality_rate: float = round((dead/infected), 3)
    title("Time: " + str(timeStep) + "\n" + " Total Infected: " + str(infected) + " Dead: " + str(dead) + " Recovered: " + str(recovered) + "\n"
          + "Mortality Rate: " + str(mortality_rate))


def update():
    global timeStep, stateConfig, total

    timeStep += 1

    for posX in range(Constants.AREA_DIMENSIONS):
        for posY in range(Constants.AREA_DIMENSIONS):

            person: Person = stateConfig[posY][posX]
            current_health_state: HealthState = person.get_state()

            # Dead people stay dead, recovered patients don't contract the disease over again
            if (current_health_state != HealthState.Dead) and (current_health_state != HealthState.Recovered):

                # If a person is healthy, check if any of it's neighbours are infected. If they are, infect this person
                # if we roll a random number lower than the infection rate.
                if current_health_state == HealthState.Healthy:
                    __handle_healthy_person(person, posY, posX)

                # If a person is infected, roll a random number and compare to mortality rate. If the person survives,
                # Make it recovered
                elif current_health_state == HealthState.Infected:
                    __handle_infected_person(person)

            else:
                #   Replace dead or recovered cells with new ones
                person = Person(HealthState.Healthy)
                total += 1

            stateConfig[posY][posX] = person


def __handle_infected_person(person: Person) -> None:
    global dead
    global recovered

    infection_duration = person.get_infection().get_duration()

    if person.get_infection().get_lethal():
        person.become_dead()
        dead += 1
        return

    # An infected person has a chance of recovering after they have been sick for the average duration of COVID-19, and
    # they roll a sufficient random number. Chances of going into recovery becomes higher the longer they are sick.
    elif infection_duration >= Constants.AVERAGE_DURATION and random() < (Constants.RECOVERY_CHANCE + (infection_duration - Constants.INCUBATION_DURATION)/200):
        person.become_recovered()
        recovered += 1
        return

    person.get_infection().update()


def __handle_healthy_person(person: Person, pos_y: int, pos_x: int) -> None:
    """
    Iterates through the neighbourhood of the current person located at (pos_y, pos_x). If anyone
    in the neighbourhood has the desired state (infected), roll a random number and compare it to the infection rate for
    each infected cell to see if the current cell should be updated.

    :param person: The person we are controlling the neighbourhood of
    :param pos_y: Y-coordinate of the current person
    :param pos_x: X-coordinate of the current person
    """

    global infected

    infection_chance = Constants.INFECTION_CHANCE

    if person.get_wearing_mask():
        infection_chance *= Constants.MASK_REDUCTION

    if person.get_social_distancing():
        infection_chance *= Constants.DISTANCING_REDUCTION

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            y = (pos_y + dy) % Constants.AREA_DIMENSIONS
            x = (pos_x + dx) % Constants.AREA_DIMENSIONS

            if stateConfig[y][x].get_state() == HealthState.Infected:

                # The neighbour must be in an infectious phase of the disease to infect someone
                if random() < infection_chance and stateConfig[y][x].get_infection().get_infectious():
                    person.become_infected()
                    infected += 1


def __create_health_value_array() -> ndarray:
    """
    The PyCX simulator utilizes Pyplot's imshow function to render the grid, and that only accepts an array with integer
    values. This function creates a 2D numpy array with the health_state values from each person in the stateConfig in
    order to render a cells health state graphicly.

    In terms of effectiveness, looping through the entire stateConfig and retrieving the health_state value for every
    person object is abysmal. Look into how to pass stateConfig directly to some Pyplot function if we get the time for
    it.

    :return: 2D ndarray with the health_state values of every person object in stateConfig.
    """
    global stateConfig
    health_values: ndarray = zeros([Constants.AREA_DIMENSIONS, Constants.AREA_DIMENSIONS], int)

    for columns in range(len(stateConfig)):
        for rows in range(len(stateConfig[columns])):
            health_values[columns, rows] = stateConfig[columns][rows].get_state().value

    return health_values


pycx.GUI().start(func=[initialize, observe, update])
