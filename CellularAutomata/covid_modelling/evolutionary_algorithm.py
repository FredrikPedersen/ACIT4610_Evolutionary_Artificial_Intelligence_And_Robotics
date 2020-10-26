import covid_modelling.constants as constants
import covid_modelling.variables as variables
from typing import List
from covid_modelling.simulation_run import SimulationRun

ADEQUATE_INFECTIONS_DIFFERENCE: int = int(constants.REPORTED_INFECTIONS/10)
ADEQUATE_DEATHS_DIFFERENCE: int = int(constants.REPORTED_DEATHS/10)

number_of_evolutions: int = 0
stable_infection: int = 0  # Counter to keep track of if the simulation have been on par with the benchmarks.
stable_death: int = 0  # Counter to keep track of if the simulation have been on par with the benchmarks.


def __calculate_benchmark_fitness(value: int, benchmark_value: int, absolute=True) -> int:
    if absolute:
        return abs(value - benchmark_value)
    else:
        return value - benchmark_value


def evolve_simulation(simulation_runs: List[SimulationRun]) -> None:
    global stable_infection, stable_death, number_of_evolutions

    if stable_death >= 5 and stable_infection >= 5:
        variables.STEP_LIMIT = 1000
        return

    number_of_evolutions += 1

    infection_chance_change: float = variables.INFECTION_CHANCE / 10
    mortality_chance_change: float = variables.MORTALITY_CHANCE / 10

    previous_simulation: SimulationRun = simulation_runs[len(simulation_runs) - 1]
    previous_simulation_deaths: int = previous_simulation.get_deaths()
    previous_simulation_infected: int = previous_simulation.get_infected()

    # By checking whether the infected and death rates are higher or lower than the benchmark values, increase
    # or decrease INFECTION_CHANCE and/or MORTALITY_CHANCE accordingly.
    infection_fitness = __calculate_benchmark_fitness(previous_simulation_infected, constants.REPORTED_INFECTIONS, False)

    # In case of some stray simulations, don't change the infection rate if there have been multiple stable runs
    if infection_fitness < -ADEQUATE_INFECTIONS_DIFFERENCE and stable_infection < 5:
        variables.INFECTION_CHANCE += infection_chance_change
        stable_infection = 0

    elif infection_fitness > ADEQUATE_INFECTIONS_DIFFERENCE and stable_infection < 5:
        variables.INFECTION_CHANCE -= infection_chance_change
        stable_infection = 0

    else:

        stable_infection += 1

        # The mortality rate is dependent on the infection rate (more infected people, more likely that people die)
        # Changing the mortality chances when the infection rate is not stabled will lead to a lot of unnecessary
        # adjustments, so we only do so when the infection rate is stable.
        mortality_fitness = __calculate_benchmark_fitness(previous_simulation_deaths, constants.REPORTED_DEATHS, False)

        if mortality_fitness < -ADEQUATE_DEATHS_DIFFERENCE and stable_death < 5:
            variables.MORTALITY_CHANCE += mortality_chance_change
            stable_death = 0

        elif mortality_fitness > ADEQUATE_DEATHS_DIFFERENCE and stable_death < 5:
            variables.MORTALITY_CHANCE -= mortality_chance_change
            stable_death = 0

        else:
            stable_death += 1
