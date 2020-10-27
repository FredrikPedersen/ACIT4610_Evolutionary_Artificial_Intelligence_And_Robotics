import covid_modelling.constants as constants
import covid_modelling.variables as variables
from typing import List
from covid_modelling.simulation_run import SimulationRun


class EvolutionaryAlgorithm:
    __ADEQUATE_INFECTIONS_DIFFERENCE: int = int(constants.REPORTED_INFECTIONS / 10)
    __ADEQUATE_DEATHS_DIFFERENCE: int = int(constants.REPORTED_DEATHS / 10)

    __number_of_evolutions: int = 0
    __stable_infection: int = 0  # Counter to keep track of if the simulation have been on par with the benchmarks.
    __stable_death: int = 0  # Counter to keep track of if the simulation have been on par with the benchmarks.

    __highest_infection_chance: float = 1
    __lowest_infection_chance: float = 0

    __highest_mortality_chance: float = 1
    __lowest_mortality_chance: float = 0

    def evolve_simulation(self, simulation_runs: List[SimulationRun]) -> None:

        # Simulation is reaching nearly realistic numbers, no need to evolve it any further
        if self.__stable_death >= 5 and self.__stable_infection >= 5:
            variables.STEP_LIMIT = 730
            return

        self.__number_of_evolutions += 1

        previous_simulation: SimulationRun = simulation_runs[len(simulation_runs) - 1]
        previous_simulation_deaths: int = previous_simulation.get_deaths()
        previous_simulation_infected: int = previous_simulation.get_infected()

        if self.__evolve_infection_chance(previous_simulation_infected):
            self.__evolve_mortality_chance(previous_simulation_deaths)

    # evolve_simulation

    def __calculate_benchmark_fitness(self, value: int, benchmark_value: int, absolute=True) -> int:
        if absolute:
            return abs(value - benchmark_value)
        else:
            return value - benchmark_value

    # __calculate_benchmark_fitness

    def __evolve_infection_chance(self, previous_simulation_infected: int) -> bool:

        # By checking whether the infected and death rates are higher or lower than the benchmark values, increase
        # or decrease INFECTION_CHANCE and/or MORTALITY_CHANCE accordingly.
        infection_fitness = self.__calculate_benchmark_fitness(previous_simulation_infected, constants.REPORTED_INFECTIONS, False)

        # In case of some stray simulations, don't change the infection rate if there have been multiple stable runs
        if infection_fitness < -self.__ADEQUATE_INFECTIONS_DIFFERENCE and self.__stable_infection < 5:

            if variables.INFECTION_CHANCE > self.__lowest_mortality_chance:
                self.__lowest_infection_chance = variables.INFECTION_CHANCE

            variables.INFECTION_CHANCE = (self.__lowest_infection_chance + self.__highest_infection_chance) / 2
            self.__stable_infection = 0
            return False

        elif infection_fitness > self.__ADEQUATE_INFECTIONS_DIFFERENCE and self.__stable_infection < 5:

            if variables.INFECTION_CHANCE < self.__highest_infection_chance:
                self.__highest_infection_chance = variables.INFECTION_CHANCE

            variables.INFECTION_CHANCE = (self.__lowest_infection_chance + self.__highest_infection_chance) / 2
            self.__stable_infection = 0
            return False

        self.__stable_infection += 1
        return True

    # __evolve_infection_chance

    def __evolve_mortality_chance(self, previous_simulation_deaths: int) -> bool:

        # The mortality rate is dependent on the infection rate (more infected people, more likely that people die)
        # Changing the mortality chances when the infection rate is not stabled will lead to a lot of unnecessary
        # adjustments, so we only do so when the infection rate is stable.
        mortality_fitness = self.__calculate_benchmark_fitness(previous_simulation_deaths, constants.REPORTED_DEATHS, False)

        if mortality_fitness < -self.__ADEQUATE_DEATHS_DIFFERENCE and self.__stable_death < 5:

            if variables.MORTALITY_CHANCE > self.__lowest_mortality_chance:
                self.__lowest_mortality_chance = variables.MORTALITY_CHANCE

            variables.MORTALITY_CHANCE = (self.__lowest_mortality_chance + self.__highest_mortality_chance) / 2
            self.__stable_death = 0
            return False

        elif mortality_fitness > self.__ADEQUATE_DEATHS_DIFFERENCE and self.__stable_death < 5:

            if variables.MORTALITY_CHANCE < self.__highest_mortality_chance:
                self.__highest_mortality_chance = variables.MORTALITY_CHANCE

            variables.MORTALITY_CHANCE = (self.__lowest_mortality_chance + self.__highest_mortality_chance) / 2
            self.__stable_death = 0
            return False

        self.__stable_death += 1
        return True

    # __evolve_mortality_chance

    def get_number_of_evolutions(self) -> int:
        return self.__number_of_evolutions
