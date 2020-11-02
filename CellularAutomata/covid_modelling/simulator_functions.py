from typing import List

from pylab import *

import covid_modelling.constants as constants
import covid_modelling.variables as variables
import pycx.pycxsimulator as pycx
from covid_modelling.evolution.scenario_algorithm import evolve as evolveSimulation
from covid_modelling.evolution.fitness_utility import FitnessUtility
from covid_modelling.evolution.preventive_measures import PreventiveMeasures
from covid_modelling.evolution.simulation_adjustment import SimulationAdjustment
from covid_modelling.results.simulation_run import SimulationRun
from covid_modelling.simulation_classes.health_state import HealthState
from covid_modelling.simulation_classes.person import Person

timeStep: int
totalDead: int
totalRecovered: int
totalInfected: int
stateConfig: List[List[Person]]
allPeople: List[Person]
currentRun: SimulationRun
previousRuns: List[SimulationRun] = []
adjustments: SimulationAdjustment = SimulationAdjustment()
fitnessUtility: FitnessUtility = FitnessUtility()


def initialize() -> None:
    global timeStep, stateConfig, totalInfected, totalDead, totalRecovered, allPeople, currentRun
    timeStep = 0
    totalInfected = 0
    totalDead = 0
    totalRecovered = 0
    allPeople = []
    currentRun = SimulationRun(len(allPeople), totalDead, totalInfected)

    # numpy arrays does not support objects, using a standard 2D-array instead
    stateConfig = [[Person for i in range(constants.AREA_DIMENSIONS)] for j in range(constants.AREA_DIMENSIONS)]

    for posX in range(constants.AREA_DIMENSIONS):
        for posY in range(constants.AREA_DIMENSIONS):

            person: Person
            if random() < constants.INIT_INFECTION_PROBABILITY:
                person = Person(HealthState.Infected)
                stateConfig[posY][posX] = person
                totalInfected += 1
            else:
                person = Person(HealthState.Healthy)
                stateConfig[posY][posX] = person

            allPeople.append(person)


def observe() -> None:
    health_values: ndarray = __create_health_value_array()
    mortality_rate_percent: float = round((totalDead / totalInfected) * 100, 2)
    isolation_string: str = "Yes" if variables.MANDATORY_ISOLATION else "No"

    cla()
    imshow(health_values, vmin=0, vmax=len(HealthState), cmap=cm.jet)
    axis("image")

    title(f"Days: {timeStep}\n"
          f"Total Infected: {totalInfected} Mortality Rate: {mortality_rate_percent}% Recovered: {totalRecovered}\n "
          f"Mandatory Isolation: {isolation_string} Using Masks: {variables.PERCENTAGE_USING_MASKS} Social Distancing: {variables.PERCENTAGE_SOCIAL_DISTANCING}")


def update() -> None:
    global timeStep, stateConfig, currentRun
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

    __update_current_run()

    if timeStep == variables.STEP_LIMIT:
        previousRuns.append(currentRun)
        preventive_measures: PreventiveMeasures = PreventiveMeasures.get_instance()
        preventive_measures.update()


def adjust() -> None:
    if variables.ADJUSTMENTS_ENABLED:
        adjustments.adjust_simulation(previousRuns)


def evolve() -> None:
    if not variables.ADJUSTMENTS_ENABLED:
        variables.EVOLUTION_COMPLETE = evolveSimulation()


def __handle_infected_person(person: Person) -> None:
    global totalDead
    global totalRecovered

    infection_duration = person.get_infection().get_duration()

    if person.get_infection().get_lethal():
        person.become_dead()
        totalDead += 1
        return

    # An infected person has a chance of recovering after they have been sick for the average duration of COVID-19, and
    # they roll a sufficient random number. Chances of going into recovery becomes higher the longer they are sick.
    elif infection_duration >= constants.AVERAGE_DURATION:
        if random() < (variables.RECOVERY_CHANCE + (infection_duration - constants.INCUBATION_DURATION) / 200):
            person.become_recovered()
            totalRecovered += 1
            return

    person.get_infection().update()

    if person.get_infection().get_infection_stage() == constants.SYMPTOMS and variables.MANDATORY_ISOLATION:
        person.set_in_isolation(True)


def __handle_healthy_person(person: Person, pos_y: int, pos_x: int) -> None:
    global totalInfected

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
                    totalInfected += 1


def __create_health_value_array() -> ndarray:
    global stateConfig
    health_values: ndarray = zeros([constants.AREA_DIMENSIONS, constants.AREA_DIMENSIONS], int)

    for columns in range(len(stateConfig)):
        for rows in range(len(stateConfig[columns])):
            health_values[columns, rows] = stateConfig[columns][rows].get_state().value

    return health_values


def __update_current_run() -> None:
    global currentRun

    currentRun.set_total_people(len(allPeople))
    currentRun.set_infected(totalInfected)
    currentRun.set_deaths(totalDead)
    currentRun = fitnessUtility.calculate_and_update_fitness(currentRun, timeStep)


pycx.GUI().start(previousRuns, func=[initialize, observe, update, adjust, evolve])
