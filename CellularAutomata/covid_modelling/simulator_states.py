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


def initialize() -> None:
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


def observe() -> None:
    health_values: ndarray = __create_health_value_array()

    cla()
    imshow(health_values, vmin=0, vmax=len(HealthState), cmap=cm.jet)
    axis("image")

    mortality_rate_percent: float = round((dead/infected)*100, 2)
    title(f"Days: {timeStep}\n Total Infected: {infected} Dead: {dead} Recovered: {recovered}\n "
          f"Mortality Rate: {mortality_rate_percent} %")


def update() -> None:
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
    elif infection_duration >= Constants.AVERAGE_DURATION:
        if random() < (Constants.RECOVERY_CHANCE + (infection_duration - Constants.INCUBATION_DURATION) / 200):
            person.become_recovered()
            recovered += 1
            return

    person.get_infection().update()


def __handle_healthy_person(person: Person, pos_y: int, pos_x: int) -> None:
    global infected

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            y = (pos_y + dy) % Constants.AREA_DIMENSIONS
            x = (pos_x + dx) % Constants.AREA_DIMENSIONS

            if stateConfig[y][x].get_state() == HealthState.Infected:

                infection_chance = Constants.INFECTION_CHANCE

                if person.get_wearing_mask():
                    infection_chance *= Constants.MASK_REDUCTION

                if person.get_social_distancing():
                    infection_chance *= Constants.DISTANCING_REDUCTION

                # The neighbour must be in an infectious phase of the disease to infect someone
                if random() < infection_chance and stateConfig[y][x].get_infection().get_infectious():
                    person.become_infected()
                    infected += 1


def __create_health_value_array() -> ndarray:
    global stateConfig
    health_values: ndarray = zeros([Constants.AREA_DIMENSIONS, Constants.AREA_DIMENSIONS], int)

    for columns in range(len(stateConfig)):
        for rows in range(len(stateConfig[columns])):
            health_values[columns, rows] = stateConfig[columns][rows].get_state().value

    return health_values


pycx.GUI().start(func=[initialize, observe, update])
