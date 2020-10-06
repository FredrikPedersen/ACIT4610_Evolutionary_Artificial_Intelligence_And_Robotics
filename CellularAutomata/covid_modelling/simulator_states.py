from pylab import *

import pycx.pycxsimulator as pycx
import covid_modelling.constants as Constants
from typing import List
from covid_modelling.health_state import HealthState
from covid_modelling.person import Person
from covid_modelling.infection import Infection

timeStep: int
stateConfig: ndarray
nextStateConfig: ndarray
people: List[List[Person]]


def initialize():
    global timeStep, stateConfig, nextStateConfig, people

    timeStep = 0

    stateConfig = zeros([Constants.AREA_DIMENSIONS, Constants.AREA_DIMENSIONS], int)
    people = [[Person for i in range(Constants.AREA_DIMENSIONS)] for j in range(Constants.AREA_DIMENSIONS)]     # numpy does not support objects

    for posX in range(Constants.AREA_DIMENSIONS):
        for posY in range(Constants.AREA_DIMENSIONS):

            if random() < Constants.INIT_INFECTION_PROBABILITY:
                state: HealthState = HealthState.Infected
                people[posY][posX] = (Person(state, int(random()*100), Infection()))
            else:
                state: HealthState = HealthState.Healthy
                people[posY][posX] = (Person(state, int(random()*100)))

            stateConfig[posY, posX] = state.value

    nextStateConfig = zeros([Constants.AREA_DIMENSIONS, Constants.AREA_DIMENSIONS])


def observe():
    cla()
    imshow(stateConfig, vmin=0, vmax=len(HealthState), cmap=cm.jet)
    axis('image')
    title('t = ' + str(timeStep))


def update():
    global timeStep, stateConfig, nextStateConfig, people

    timeStep += 1

    for posX in range(Constants.AREA_DIMENSIONS):
        for posY in range(Constants.AREA_DIMENSIONS):

            person: Person = people[posY][posX]
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

            nextStateConfig[posY, posX] = person.get_state().value

    stateConfig, nextStateConfig = nextStateConfig, stateConfig

    if timeStep == 80:
        __calculate_mortality()


# For testing purposes, delete later
def __calculate_mortality():

    entities = 0
    dead = 0
    for row in range(len(people)):
        for column in range(len(people[row])):
            entities += 1
            if people[row][column].get_state() == HealthState.Dead:
                dead += 1

    print(dead / entities)


def __handle_infected_person(person: Person) -> None:
    infection_duration = person.get_infection().get_duration()

    # Currently only old people die according to our model, introduce variables for checking if a person has other
    # Health problems as well.
    if person.get_age() > 60 and random() < Constants.MORTALITY_RATE:
        person.become_dead()
        return

    # An infected person has a chance of recovering after they have been sick for the average duration of COVID-19, and
    # they roll a sufficient random number. Chances of going into recovery becomes higher the longer they are sick.
    elif infection_duration >= Constants.AVERAGE_DURATION \
            and random() < (Constants.RECOVERY_CHANCE + (infection_duration - Constants.INCUBATION_DURATION)/200):
        person.become_recovered()
        return

    person.get_infection().update()


def __handle_healthy_person(person: Person, pos_y: int, pos_x: int) -> None:
    """
    Iterates through the neighbourhood of the current person located at (pos_y, pos_x). If anyone
    in the neighbourhood has the desired state (infected), roll a random number and compare it to the infection rate
    too see if the current cell should be updated.

    :param person: The person we are controlling the neighbourhood of
    :param pos_y: Y-coordinate of the current person
    :param pos_x: X-coordinate of the current person
    """

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            y = (pos_y + dy) % Constants.AREA_DIMENSIONS
            x = (pos_x + dx) % Constants.AREA_DIMENSIONS

            if stateConfig[y, x] == HealthState.Infected.value:

                #TODO THERE IS A BUG HERE WHERE EITHER AN UNINFECTED OR DEAD PERSON IS BEING CHECKED FOR BEING INFECTIOUS
                # The neighbour must be in an infectious phase of the disease to infect someone
                if random() < Constants.INFECTION_RATE and people[y][x].get_infection().get_infectious():
                    person.become_infected()


pycx.GUI().start(func=[initialize, observe, update])