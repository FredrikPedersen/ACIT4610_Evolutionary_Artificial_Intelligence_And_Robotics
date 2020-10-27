from typing import List

from pylab import *

import covid_modelling.constants as constants
import covid_modelling.variables as variables
import pycx.pycxsimulator as pycx

from covid_modelling.simulation_adjustment import SimulationAdjustment
from covid_modelling.evolutionaryalgorithm import EvolutionaryAlgorithm
from covid_modelling.preventive_measures import PreventiveMeasures
from covid_modelling.health_state import HealthState
from covid_modelling.person import Person
from covid_modelling.simulation_run import SimulationRun

timeStep: int
dead: int
recovered: int
infected: int
stateConfig: List[List[Person]]
allPeople: List[Person]
previousRuns: List[SimulationRun] = []
adjustments: SimulationAdjustment = SimulationAdjustment()
evolution: EvolutionaryAlgorithm = EvolutionaryAlgorithm()


def initialize() -> None:
    global timeStep, stateConfig, infected, dead, recovered, allPeople
    timeStep = 0
    infected = 0
    dead = 0
    recovered = 0

    # numpy arrays does not support objects, using a standard 2D-array instead
    stateConfig = [[Person for i in range(constants.AREA_DIMENSIONS)] for j in range(constants.AREA_DIMENSIONS)]
    allPeople = []

    for posX in range(constants.AREA_DIMENSIONS):
        for posY in range(constants.AREA_DIMENSIONS):

            person: Person
            if random() < constants.INIT_INFECTION_PROBABILITY:
                person = Person(HealthState.Infected)
                stateConfig[posY][posX] = person
                infected += 1
            else:
                person = Person(HealthState.Healthy)
                stateConfig[posY][posX] = person

            allPeople.append(person)


def observe() -> None:
    health_values: ndarray = __create_health_value_array()
    reproduction_rate: float = round(__calculate_r0(), 2)
    mortality_rate_percent: float = round((dead/infected)*100, 2)

    cla()
    imshow(health_values, vmin=0, vmax=len(HealthState), cmap=cm.jet)
    axis("image")

    title(f"Days: {timeStep} R0: {reproduction_rate} \n"
          f"Total Infected: {infected} Dead: {dead} Recovered: {recovered}\n "
          f"Mortality Rate: {mortality_rate_percent}%\n"
          f"Infection Chance: {round(variables.INFECTION_CHANCE,4)} Mortality Chance: {round(variables.MORTALITY_CHANCE, 4)}")


def update() -> None:
    global timeStep, stateConfig
    timeStep += 1

    for posX in range(constants.AREA_DIMENSIONS):
        for posY in range(constants.AREA_DIMENSIONS):

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
                allPeople.append(person)

            stateConfig[posY][posX] = person

    if timeStep == variables.STEP_LIMIT:
        previousRuns.append(SimulationRun(len(allPeople), dead, infected, __calculate_r0()))
        preventive_measures: PreventiveMeasures = PreventiveMeasures.get_instance()
        preventive_measures.update()



def adjust() -> None:
    if not variables.ADJUSTMENTS_COMPLETE:
        print("ADJUSTING")
        adjustments.adjust_simulation(previousRuns)


def evolve() -> None:
    if variables.ADJUSTMENTS_COMPLETE:
        print("EVOLVING")
        evolution.evolve(previousRuns)

    return


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
    elif infection_duration >= constants.AVERAGE_DURATION:
        if random() < (variables.RECOVERY_CHANCE + (infection_duration - constants.INCUBATION_DURATION) / 200):
            person.become_recovered()
            recovered += 1
            return

    person.get_infection().update()

    if person.get_infection().get_infection_stage() == constants.SYMPTOMS and variables.MANDATORY_ISOLATION:
        person.set_in_isolation(True)


def __handle_healthy_person(person: Person, pos_y: int, pos_x: int) -> None:
    global infected

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            y = (pos_y + dy) % constants.AREA_DIMENSIONS
            x = (pos_x + dx) % constants.AREA_DIMENSIONS

            neighbour: Person = stateConfig[y][x]

            if (neighbour.get_state() == HealthState.Infected) and (not neighbour.get_in_isolation()):

                infection_chance = variables.INFECTION_CHANCE

                if person.get_wearing_mask():
                    infection_chance *= constants.MASK_REDUCTION

                if person.get_social_distancing():
                    infection_chance *= constants.DISTANCING_REDUCTION

                # The neighbour must be in an infectious phase of the disease to infect someone
                if random() < infection_chance and neighbour.get_infection().get_infectious():
                    neighbour.increment_infection_spread()
                    person.become_infected()
                    infected += 1


def __create_health_value_array() -> ndarray:
    global stateConfig
    health_values: ndarray = zeros([constants.AREA_DIMENSIONS, constants.AREA_DIMENSIONS], int)

    for columns in range(len(stateConfig)):
        for rows in range(len(stateConfig[columns])):
            health_values[columns, rows] = stateConfig[columns][rows].get_state().value

    return health_values


def __calculate_r0() -> float:
    infections_spread = 0

    for person in allPeople:
        person_state: HealthState = person.get_state()
        if person_state == HealthState.Infected or person_state == HealthState.Dead or person_state == HealthState.Recovered:
            infections_spread += person.get_infection_spread()

    return infections_spread/infected


pycx.GUI().start(func=[initialize, observe, update, adjust, evolve])
