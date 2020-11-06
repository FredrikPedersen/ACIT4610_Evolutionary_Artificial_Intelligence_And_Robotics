from typing import List
import covid_modelling.constants as constants
import covid_modelling.variables as variables
from covid_modelling.results.simulation_run import SimulationRun


class SimulationAdjustment:
    """
    Simulation adjustments is an evolutionary algorithm meant to adjust the INFECTION_CHANCE and MORTALITY_CHANCE
    variables to yield a result as close as possible to real-world numbers of infected and dead.
    """
    __instance = None

    __ADEQUATE_INFECTIONS_DIFFERENCE: int = int(constants.REPORTED_INFECTIONS / 10)
    __ADEQUATE_DEATHS_DIFFERENCE: int = int(constants.REPORTED_DEATHS / 10)

    __highest_infection_chance: float = 0.5
    __lowest_infection_chance: float = 0.1

    __highest_mortality_chance: float = 0.5
    __lowest_mortality_chance: float = 0.01

    @staticmethod
    def get_instance():
        if SimulationAdjustment.__instance is None:
            SimulationAdjustment()

        return SimulationAdjustment.__instance

    def __init__(self):
        if SimulationAdjustment.__instance is not None:
            raise Exception("This is a Singleton class, do not try to instantiate it directly. Use get_instance method!")
        else:
            SimulationAdjustment.__instance = self

    def adjust_simulation(self, simulation_runs: List[SimulationRun]):
        previous_simulation: SimulationRun = simulation_runs[len(simulation_runs) - 1]

        if self.__adjust_infection_chance(previous_simulation) and self.__adjust_mortality_chance(previous_simulation):
            variables.ADJUSTMENTS_ENABLED = False

    # adjust_simulation

    def __calculate_benchmark_fitness(self, value: int, benchmark_value: int, absolute=True) -> int:
        if absolute:
            return abs(value - benchmark_value)
        else:
            return value - benchmark_value

    # __calculate_benchmark_fitness

    def __adjust_infection_chance(self, previous_simulation: SimulationRun) -> bool:

        previous_simulation_infected: int = previous_simulation.get_infected()
        infection_fitness = self.__calculate_benchmark_fitness(previous_simulation_infected, constants.REPORTED_INFECTIONS, False)

        if infection_fitness < -self.__ADEQUATE_INFECTIONS_DIFFERENCE:

            if variables.INFECTION_CHANCE > self.__lowest_mortality_chance:
                self.__lowest_infection_chance = variables.INFECTION_CHANCE

            variables.INFECTION_CHANCE = (self.__lowest_infection_chance + self.__highest_infection_chance) / 2
            return False

        elif infection_fitness > self.__ADEQUATE_INFECTIONS_DIFFERENCE:

            if variables.INFECTION_CHANCE < self.__highest_infection_chance:
                self.__highest_infection_chance = variables.INFECTION_CHANCE

            variables.INFECTION_CHANCE = (self.__lowest_infection_chance + self.__highest_infection_chance) / 2
            return False

        return True

    # __evolve_infection_chance

    def __adjust_mortality_chance(self, previous_simulation: SimulationRun):

        previous_simulation_deaths: int = previous_simulation.get_deaths()
        mortality_fitness = self.__calculate_benchmark_fitness(previous_simulation_deaths, constants.REPORTED_DEATHS, False)

        if mortality_fitness < -self.__ADEQUATE_DEATHS_DIFFERENCE:

            if variables.MORTALITY_CHANCE > self.__lowest_mortality_chance:
                self.__lowest_mortality_chance = variables.MORTALITY_CHANCE

            variables.MORTALITY_CHANCE = (self.__lowest_mortality_chance + self.__highest_mortality_chance) / 2
            return False

        elif mortality_fitness > self.__ADEQUATE_DEATHS_DIFFERENCE:

            if variables.MORTALITY_CHANCE < self.__highest_mortality_chance:
                self.__highest_mortality_chance = variables.MORTALITY_CHANCE

            variables.MORTALITY_CHANCE = (self.__lowest_mortality_chance + self.__highest_mortality_chance) / 2
            return False

        return True

    # __evolve_mortality_chance
